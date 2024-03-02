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
from .models import MovieQuotes, MovieSearchHistory, MovieSynopsis, MovieQuoteOverview, DialogueMovie
from .serializer import MovieSerializer, MovieSearchHistorySerializer, PlotSerializer, MovieQuoteSerializer, DialogueMovieSerializer
from rest_framework.authtoken.models import Token
from Accounts.models import *
from Accounts.serializer import UserHistorySerializer
from rest_framework import status
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .tfidf import TFIDFVectorizer, cosine_similarity as calculate
from .onehotencode import OneHotEncoder
import nltk
# nltk.download('stopwords')
# Create your views here.

# print(Quote.objects.get(id=64))
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
        # print(Quote.objects.get(id=64))
        #Reading module from the pickle
        with open('./finalized_model_1.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([quote])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        score = cosine.reshape(-1)
        max = cosine.argmax()   
        
        # m = load_model('./Defense_lstm_model_III.h5')
        # with open('./LSTM_token_model.pkl', 'rb') as f:
        #     token, max_length = pickle.load(f)

        # #LSTM model 
        # new_quote_sequence = token.texts_to_sequences([quote])
        # padded_sequence = pad_sequences(new_quote_sequence, maxlen=max_length)
        # predicted_movie = m.predict(padded_sequence)

        # score_lstm = predicted_movie.reshape(-1)
        # Decode the predicted movie name
    
        # # id_lstm = np.argmax(predicted_movie, axis=-1)[0]
        # print("The lstm score is {0}".format(score[id]))

        
        user_history = SearchHistory(user=user, user_query=quote, search_type="movie")
        print(user_history)
        user_history.save()

#     Single Response value

        # # threshold value: 0.9
        # if score[max]>0.9:
        #     #Serialization
        #     movie = MovieQuotes.objects.get(id=max+1)
        #     serializer = MovieSerializer(movie)

        #     #Save user search in  movie history model
        #     history = MovieSearchHistory(user_quote=quote, user=user, movie=movie)
        #     history.save()

        #     #Save user search in user history model
        #     user_history = SearchHistory(user=user, user_query=quote, search_type="movie")
        #     print(user_history)
        #     user_history.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        
        # threshold set 0.8
        # Multiple Movie Response


        if score[max] > 0.85:

            print("The cosine similarity score is {0}".format(score[max]))
            index = get_movie_index(score)
            
            
            #Serialization
            # movies = MovieQuotes.objects.filter(pk__in=index)
            # movies = [MovieQuotes.objects.get(id=i) for i in index] # without image
            # serializer = MovieSerializer(movies, many=True)

            
            movies = [MovieQuoteOverview.objects.get(id=i) for i in index] # with image
            print(type(movies))
            serializer = MovieQuoteSerializer(movies, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)          
        else:
            # Load trained LSTM Model, tokens
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

            #threshold value: 0.7
            if score[id] > 0.82:

                index = get_movie_index(score)
                
                # predicted_movie_name = MovieQuotes.objects.filter(pk__in=index)
                
                # predicted_movie_name = [MovieQuotes.objects.get(id=id) for id in index] #Without image
                # serializer = MovieSerializer(predicted_movie_name, many=True)
                predicted_movie_name = [MovieQuoteOverview.objects.get(id=id) for id in index] # With image
                print(type(predicted_movie_name))
                serializer = MovieQuoteSerializer(predicted_movie_name, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Your quote is vague to the system"}, status=status.HTTP_404_NOT_FOUND)
        """
            JSON response
            [{
                "director": "George Lucas",
                "genre": "Action, Adventure, Fantasy",
                "id": 64,
                "imdb_rating": "8.6",
                "metascore": "90.0",
                "movie": "Star Wars",
                "overview": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.",
                "poster_link": "https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX67_CR0,0,67,98_AL_.jpg",
                "quote": "May the Force be with you.",
                "type": "movie",
                "year": 1977,
                "youtube_link": "https://www.youtube.com/watch?v=8Qn_spdM5Zg"
            },]
            """

# JSON REQUEST 
# MEthod POST
# # {'plot': <PLot info>}

class MoviePlotAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        plot = python_data.get('plot')


        #Token Authentication
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

        #Reading module from the pickle
        with open('./movie_synopsis_model_1.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([plot])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        score = cosine.reshape(-1)
        max = cosine.argmax() 

        user_history = SearchHistory(user=user, user_query=plot, search_type="plot")
        print(user_history)
        user_history.save()
        print("The cosine similarity score is {0}".format(score[max]))
        if (score[max] != 0):
            movie = MovieSynopsis.objects.get(id=max+1)
            serializer = PlotSerializer(movie)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response({'message':'Plot of user is vague'}, status=status.HTTP_400_BAD_REQUEST)

# JSON Response
# {
#     'id': 91
#     'imdb_id': "1021092",
#     'plot_synopsis':'sihgdkonfdkfndkfjndjf',
#     'tags': 'Superhero', 'comic',
#     'title': 'Iron Man'
# }


#obsolete for now
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



# sorting score in descending order
def get_movie_index(score):
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



import pickle
# with open("./movie_models/movie_scratch_model_mock_up.pkl", 'rb') as f:
#     vectorizer, document_vectors = pickle.load(f)

with open("./movie_models/movie_module_stemming.pkl", 'rb') as f:
    vectorizer, document_vectors = pickle.load(f)
#Movie Identification using TFIDF and Cosine Similarity
class MovieIdentificationAPI(APIView):
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
        # print(Quote.objects.get(id=64))
        # vectorizer = TFIDFVectorizer(quote)

        input_document = quote
        input_vector = vectorizer.transform(input_document)

        # similarities = [cosine_similarity(input_vector, doc_vector) for doc_vector in document_vectors]
        similarities = []
        for i, doc_vector in enumerate(document_vectors):
            similarity = calculate(input_vector, doc_vector)
            similarities.append((i, similarity))
            
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Print the most similar document

        print(similarities[0:5])
        movie_identified = []
        for i, val in similarities:
            if val != 0:
                movie_identified.append(DialogueMovie.objects.get(id=i+1))
        
        unique_objects_dict = {}
        
        for obj in movie_identified:

            lowercase_name = obj.movie.lower().strip()
            unique_objects_dict[lowercase_name] = obj
        
        unique_objects = list(unique_objects_dict.values())


        if len(movie_identified) == 0:
            return Response({'message': 'Your query was vague to system'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DialogueMovieSerializer(unique_objects[:7], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


with open('./movie_models/defense_movie_recommend_model.pkl', 'rb') as f:
    encoder, encoded_data = pickle.load(f)
# Recommendation using One Hot Encoding and Cosine Similarity
class MovieRecommendationAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #Json To Python Raw data
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        genre = python_data.get('genre')
        id = python_data.get('id')

        id_movie = DialogueMovie.objects.get(id=id)
        # s = set()
        # # s.update(genre.split(','))
        # movie_ob = DialogueMovie.objects.all()
        # movie_genre = [ob.genre for ob in movie_ob]
        #Token Authentication
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

        # genres = set()
        # for item in movie_genre:
        #     genres.update(item.split(','))
        # print(genres)
        

        genre_encoded = encoder.transform(genre)
        print("genre encoded: ", genre_encoded)
        # Perform one-hot encoding
        # encoded_data = []
        # for item in movie_genre:
        #     encoded_data.append(encoder.transform(item))
        print(encoded_data[0])
        similarities = []
        for i, doc in enumerate(encoded_data):
             similarity = calculate(genre_encoded, doc)
             similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        # print(similarities)

        movie_recommend = []
        for i, val in similarities:
            movie_recommend.append(DialogueMovie.objects.get(id=i+1))
        
        unique_objects_dict = {}

        
        for obj in movie_recommend:
            if obj.id == id_movie.id:
                continue
            
            normalized_name = ' '.join(obj.movie.split())
            lowercase_name = normalized_name.lower().strip()
            unique_objects_dict[lowercase_name] = obj



        
        unique_objects = list(unique_objects_dict.values())
        recommend = [u for u in unique_objects if u.year>id_movie.year]
        if len(recommend) == 0:
            return Response({'message': 'Nothing to Recommend'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DialogueMovieSerializer(recommend[0:4], many=True )
        return Response(serializer.data, status=status.HTTP_200_OK)



#DialogueBasedSearchSklearnCosineSimilarity
class DialogueIdentifyMovieAPI(APIView):
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
        # print(Quote.objects.get(id=64))
        #Reading module from the pickle
        with open('./movie_models/movie_vector_module.pkl', 'rb') as f:
            tfidf, dv = pickle.load(f)

        #Preprocessing using tfidf
        input = tfidf.transform([quote])

        #cosine similarity
        cosine = cosine_similarity(input, dv)
        score = cosine.reshape(-1)
        max = cosine.argmax()   
        
        user_history = SearchHistory(user=user, user_query=quote, search_type="movie")
        print(user_history)
        user_history.save()

        if score[max] > 0.6:

            print("The cosine similarity score is {0}".format(score[max]))
            index = get_movie_index(score)
            
           
            movies = [DialogueMovie.objects.get(id=i) for i in index] # with image
            unique_objects_dict = {}
        
            for obj in movies:
                normalized_name = ' '.join(obj.movie.split())
                lowercase_name = normalized_name.lower().strip()
                unique_objects_dict[lowercase_name] = obj
            
            unique_objects = list(unique_objects_dict.values())
            # print(type(movies))
            serializer = DialogueMovieSerializer(unique_objects, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'messsage': 'Your query is vague to system'}, status=status.HTTP_404_NOT_FOUND )





        

def genre_cleaning(genres):
    set_genres = set()
    for item in genres:
        set_genres.update(item.split(','))
    # print(genres)
    cleaned_data = []
    for g in set_genres:
        cleaned_data.append(g.lstrip())
    return cleaned_data