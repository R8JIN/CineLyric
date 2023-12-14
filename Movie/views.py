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
from .models import MovieQuotes, MovieSearchHistory
from .serializer import MovieSerializer, QuoteSerializer, MovieSearchHistorySerializer
from rest_framework.authtoken.models import Token
from Accounts.models import *
from Accounts.serializer import UserHistorySerializer
from rest_framework import status

# Create your views here.


# request data type {"quote": "<quotation>"} 
# header: 'Authentication: Token $tokenkey'
class MovieSelectionAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #Json To Python Raw data
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        quote = python_data.get('quote')

        #Token Authentication
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

        #Reading module from the pickle
        with open('./finalized_model_1.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([quote])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        score = cosine.reshape(-1)
        max = cosine.argmax()
        print("The cosine similarity score is {0}".format(score[max]))
        
        # threshold value: 0.9
        if score[max]>0.9:
            
            #Serialization
            movie = MovieQuotes.objects.get(id=max+1)
            serializer = MovieSerializer(movie)

            #Save user search in  movie history model
            history = MovieSearchHistory(user_quote=quote, user=user, movie=movie)
            history.save()

            #Save user search in user history model
            user_history = SearchHistory(user=user, user_query=quote, search_id=max+1, search_type="movie")
            print(user_history)
            user_history.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            #Load trained LSTM Model, tokens
            m = load_model('./Defense_lstm_model_III.h5')
            with open('./LSTM_token_model.pkl', 'rb') as f:
                token, max_length = pickle.load(f)

            #LSTM model 
            new_quote_sequence = token.texts_to_sequences([quote])
            padded_sequence = pad_sequences(new_quote_sequence, maxlen=max_length)
            predicted_movie = m.predict(padded_sequence)

            score = predicted_movie.reshape(-1)
            # Decode the predicted movie name
        
            id = np.argmax(predicted_movie, axis=-1)[0]
            print("The lstm score is {0}".format(score[id]))

            #threshold value: 0.3
            if score[id] > 0.5:
                predicted_movie_name = MovieQuotes.objects.get(id=id+1)
                serializer = MovieSerializer(predicted_movie_name)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Your quote is vague to the system"}, status=status.HTTP_404_NOT_FOUND)
        """
            JSON response
            {
                "id": 423,
                "movie": "The Dark Knight",
                "quote": "Why so serious?",
                "type": "movie",
                "year": "2008",
            }
            """

   
class MovieHistoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #Token Authentication
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        history = MovieSearchHistory.objects.filter(user=user)
        if history is not None:
            serializer = MovieSearchHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No Search History"}, status=status.HTTP_404_NOT_FOUND)
        """ Response format
        [
            {
                "id": 2,
                "movie": 64,
                "user": 2,
                "user_quote": "may the force be with you"
            }
        ]""" 