from django.shortcuts import render
import io
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pickle
from .tfidf import TFIDFVectorizer, CountVectorizer, OneHotEncoder, cosine_similarity as cs
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import SongLyric, MusicLyric, BillBoardLyric, TrackLyric
from .serializer import SongSerializer, MusicSerializer, TrackSerializer
from  rest_framework import status
from rest_framework.authtoken.models import Token
from Accounts.models import SearchHistory, User
# Create your views here.

 # Handle division by zero

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
        with open('./ramro_song_model.pkl', 'rb') as f:
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
            music = [TrackLyric.objects.get(id=i) for i in index]
        
            new_music = music
            serializer = TrackSerializer(new_music, many=True)
            
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

        track = TrackLyric.objects.get(id=id)
        tracks = TrackLyric.objects.all()
        documents = [t.genre  for t in tracks]
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
        
        vectorizer = CountVectorizer(documents)
        tf_genre = vectorizer.transform(genre)
        document_genre =[vectorizer.transform(doc) for doc in documents]

            # print(tf_genre)
        similarities = []
        for i, doc in enumerate(document_genre):
            similarity = cs(tf_genre, doc)
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        print(similarities[:10])
        music= []
        for i, scores in similarities:
            # print(i)
            if scores > 0.7:
                music.append(TrackLyric.objects.get(id=i))


        # music = music[0:5]   
        # print(len(music))
        serializer = TrackSerializer(music, many=True)
        # print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
       
 

