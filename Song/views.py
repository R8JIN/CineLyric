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

        #Reading module from the pickle
        with open('D:/CineLyric/song_model_2.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([lyric])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        score = cosine.reshape(-1)
        max = cosine.argmax()
        print("The cosine similarity score is {0}".format(score[max]))

        # threshold value: 0.9
    
        song = SongLyric.objects.get(id=max+1)
        print(song)
        serializer = SongSerializer(song)
        return Response(serializer.data)