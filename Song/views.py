from django.shortcuts import render
import io
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pickle
from .songTFIDF import TFIDFVectorizer, cosine_similarity as cosine
from .tfidf import  OneHotEncoder, cosine_similarity as cs
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import   NewTrackLyric, SpotifyMusicLyric
from .serializer import   NewTrackSerializer, SpotifyTrackSerializer
from  rest_framework import status
from rest_framework.authtoken.models import Token
from Accounts.models import SearchHistory, User
# Create your views here.

 # Handle division by zero
import pickle
with open("./mock_up_music_model.pkl", "rb") as f:
    vectorizer = pickle.load(f)
"""
JSON request
{
    "lyric": <input>
}
Authorization: Token <tokenkey>
"""

class SongSelectionAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #Json To Python Raw data
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        lyric = python_data.get('lyric')

        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        with open('./music_models/music_tfidf_module.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([lyric])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        scores = list(cosine.reshape(-1))
        
        max = cosine.argmax()
        # print("The cosine similarity score is {0}".format(scores[max]))

        music_history = SearchHistory(user=user, user_query=lyric,
                                          search_type='music')
        
        music_history.save()
        #Multiple matching scores
        # threshold value: <set the value ranging between 0-1>
        if scores[max]>0.1:
        # song = SongLyric.objects.get(id=max+1)
            # print(scores[max])
            index = get_music_index(scores)
            # song = SongLyric.objects.filter(pk__in = index)
            # songs = [SongLyric.objects.get(id=i) for i in index] #obsolete
            # serializer = SongSerializer(songs, many=True) #obsolete
            music = [SpotifyMusicLyric.objects.get(id=i) for i in index]
        
            new_music = music[0:5]
            serializer = SpotifyTrackSerializer(new_music, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'Your query is very vague'}, status=status.HTTP_404_NOT_FOUND)
 #JSON Response
    """
    [ {
        "album": "A Pentatonix Christmas Deluxe",
        "artist_name": "pentatonix",
        "genre": "[u'a cappella']",
        "id": 654,
        "lyrics": "purai lyrics hunxa hai"        
        "release_date": 2017,
        "spotify_link": "https://open.spotify.com/artist/26AHtbjWKiwYzsoGoUZq53",
        "track_name": "Hallelujah",
        "youtube_link": "https://www.youtube.com/watch?v=LRP8d7hhpoQ"
    },]
    """   

#sorting music index score in descending order
def get_music_index(score):
    list_score = list(score)
    dict = {}
    count = 1
    for ls in list_score:
        if ls!=0 and ls >= 0.1:
            dict[count] = ls
        count = count + 1

    sort_dict = sorted(dict.items(), key=lambda x:x[1], reverse=True)
    print(sort_dict)
    
    index = []
    for keys, value in sort_dict:
        index.append(keys)
    return index




#Genre-based Recommendation

with open("./music_models/music_recommendation_model_mock_up.pkl", "rb") as f:
    encoder , encoded_data = pickle.load(f)

class MusicRecommendationAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        genre = python_data.get('genre')
        # artist = python_data.get('artist_name')
        print(genre)
        id = python_data.get('id')

        track = SpotifyMusicLyric.objects.get(id=id)
        # tracks = TrackLyric.objects.all()
        # documents = [t.genre  for t in tracks]

        genre_encoded = encoder.transform(genre)
        similarities = []
        for i, doc in enumerate(encoded_data):
            similarity = cs(genre_encoded, doc)
            similarities.append((i, similarity))
        # genres = set()
        # print(documents[0:4])
        
        # for item in documents:
        #     genres.update(item.split(','))
        # genre_artist =genre
        # encoder = OneHotEncoder(list(genres))
        # document_encode = [encoder.transform(d) for d in documents]
        # encode_genre = encoder.transform(genre_artist)
        # similarities = []
        # for i, doc in enumerate(document_encode):
        #     similarity = cs(encode_genre, doc)
        #     similarities.append((i, similarity))
        

        similarities.sort(key=lambda x: x[1], reverse=True)
        print(similarities[:10])
        music= []
        for i, scores in similarities:
            # print(i)
            if scores > 0.7:
                music.append(SpotifyMusicLyric.objects.get(id=i+1))

        unique_objects_dict = {}

        
        for obj in music:
            if obj.id == track.id:
                continue
            
            normalized_name = ' '.join(obj.track_name.split())
            lowercase_name = normalized_name.lower().strip()
            unique_objects_dict[lowercase_name] = obj



        
        unique_objects = list(unique_objects_dict.values())
        recommend = [u for u in unique_objects if u.release_date>=track.release_date] #same year 
        if len(recommend) == 0:
            return Response({'message': 'Nothing to Recommend'}, status=status.HTTP_404_NOT_FOUND)
        # music = music[0:5]   
        # print(len(music))
        serializer = SpotifyTrackSerializer(unique_objects[0:8], many=True)
        # print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
       
with open("./music_models/track_model_for_mock_up.pkl", "rb") as f:
    vectorizer, doc_vector = pickle.load(f)


class TrackIdentificationAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #Json To Python Raw data
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        lyric = python_data.get('lyric')

        # track = NewTrackLyric.objects.all()
        # track_lyric = [t.lyrics for t in track]
        # cleaned_lyrics = lyrics_clean(track_lyric)

        # print(cleaned_lyrics[0])
        verse_vector = vectorizer.transform(lyric)

        similarities = []
        for i, doc in enumerate(doc_vector):

            similarity = cs(verse_vector, doc)
            similarities.append((i, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        index, max = similarities[0]
        print(similarities[:10])
        track_identified = []
        for i, scores in similarities:
            # print(i)
            if scores > 0.1:
                track_identified.append(SpotifyMusicLyric.objects.get(id=i+1))
        
        track_identified = track_identified[0:4]
        if len(track_identified) != 0:
            serializer = SpotifyTrackSerializer(track_identified, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Your query is vague'})




def lyrics_clean(track_lyric):
    cleaned_lyrics = []
    for sample in track_lyric:
        if isinstance(sample, str):
            cleaned_lyrics.append(sample.replace('\n', ' '))
        else:
            cleaned_lyrics.append(str(sample))
    return cleaned_lyrics
        

