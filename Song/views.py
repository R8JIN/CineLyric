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
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import SongLyric
from .serializer import SongSerializer
from  rest_framework import status
from rest_framework.authtoken.models import Token
from Accounts.models import SearchHistory, User
# Create your views here.
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
        #Reading module from the pickle
        with open('D:/CineLyric/song_model_2.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([lyric])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        scores = list(cosine.reshape(-1))
        
        max = cosine.argmax()
        print("The cosine similarity score is {0}".format(scores[max]))

        music_history = SearchHistory(user=user, user_query=lyric,
                                          search_type='music')
        music_history.save()
        #Multiple matching scores
        # threshold value: <set the value ranging between 0-1>
        if scores[max]>0.5:
        # song = SongLyric.objects.get(id=max+1)
            index = get_music_index(scores)
            # song = SongLyric.objects.filter(pk__in = index)
            songs = [SongLyric.objects.get(id=i) for i in index]

            print(songs)
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'Your query is very vague'}, status=status.HTTP_404_NOT_FOUND)
    

#sorting music index score in descending order
def get_music_index(score):
    list_score = list(score)
    dict = {}
    count = 1
    for ls in list_score:
        if ls!=0 and ls > 0.2:
            dict[count] = ls
        count = count + 1

    sort_dict = sorted(dict.items(), key=lambda x:x[1], reverse=True)
    print(sort_dict)
    
    index = []
    for keys, value in sort_dict:
        index.append(keys)
    return index