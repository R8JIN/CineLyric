import io
from django.shortcuts import render
from .serializer import AccountSerializer, LoginSerializer, UserHistorySerializer, BookmarkSerializer
from rest_framework.parsers import JSONParser
from .models import User, SearchHistory, Bookmark
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from Song.models import TrackLyric, NewTrackLyric
from Movie.models import Quotation, DialogueMovie

# Create your views here.


#JSON Format
"""  
    {
        'username': 'omen'
        'password': 'password'
    }
"""
#Registration 
class RegistrationAPI(APIView):
    def post(self, request, format=None):
        account = request.data

        #Serialization
        serializer = AccountSerializer(data=account, )
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Account Registered"}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Account not registered'}, status=status.HTTP_400_BAD_REQUEST)
    

    
#Json response format
"""{
    "status": 200,
    "message": "success",
    "data": {
        "Token": "f11609400dbdb0be5fe708ca727f3ee2d67aab7f"
    }
}"""

#Json request format
"""
{
    "username": <your-username>
    "password": <your-password>
}
"""
#Login
class LoginAPI(APIView): 
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
                #retrieve after serialization validation
                username = serializer.validated_data["username"]
                password = serializer.validated_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    #We are reterving the token for authenticated user.
                    token = Token.objects.get(user=user)
                    response = {
                            "status": status.HTTP_200_OK,
                            "message": "success",
                            "data": {
                                    "Token" : token.key
                                    }
                            }
                    return Response(response, status = status.HTTP_200_OK)
                else :
                    response = {
                            "status": status.HTTP_401_UNAUTHORIZED,
                            "message": "Invalid Email or Password",
                            }
                    return Response(response, status = status.HTTP_401_UNAUTHORIZED)
        response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": serializer.errors
                }
        return Response(response, status = status.HTTP_400_BAD_REQUEST)



class SearchHistoryAPI(APIView):
     permission_classes =[IsAuthenticated]
     def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        
        user_history = SearchHistory.objects.filter(user=user).order_by('datetime')
        if user_history is not None:
            serializer = UserHistorySerializer(user_history, many=True)
            return Response(serializer.data)
        return Response({"message": "Your search is empty"})
        
        #GET method with token.
        #API Response for Search History API
        """[
            {
            "datetime": "2023-12-14T11:09:04.049982Z",
            "id": 1,
            "search_type": "movie",
            "user": 2,
            "user_query": "may the force be with you"
            }
        ]"""






"""
Request for Bookmark
{
    "id" : 1,
    "type" : movie
}
"""

class BookmarkAPI(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        bid = python_data.get('id')
        type = python_data.get('type')
        
        b = Bookmark.objects.filter(bid=bid, type=type, user=user).first()
        
        if b is None:
            if type == "music":
                music = NewTrackLyric.objects.get(id=bid)
                bookmark = Bookmark(user=user, bid=bid, type=type, title=music.track_name)
                bookmark.save()
                serializer = BookmarkSerializer(bookmark)
                return Response([{"message": "Bookmarked"}, serializer.data])
            elif type == "movie":
                movie = DialogueMovie.objects.get(id=bid)
                bookmark = Bookmark(user=user, bid=bid, type=type, title=movie.movie)
                bookmark.save()
                serializer = BookmarkSerializer(bookmark)
                return Response([{"message": "Bookmarked"}, serializer.data])
            
            """"
[
    {
        "message": "Bookmarked"
    },
    {
        "bid": 400,
        "datetime": "2024-02-27T10:04:23.172534Z",
        "id": 8,
        "image_link": null,
        "title": "Bam",
        "type": "music",
        "user": 3
    }
]
            """
        return Response({'message':"Already bookmarked"})

    def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        
        bookmark = Bookmark.objects.filter(user=user).order_by('-datetime')
        if bookmark is not None:
            serializer = BookmarkSerializer(bookmark, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Your search is empty"})
    """
    [
    {
        "bid": 400,
        "datetime": "2024-02-26T13:28:20.996135Z",
        "id": 7,
        "image_link": null,
        "title": "Harry Potter and the Order of the Phoenix",
        "type": "movie",
        "user": 3
    },
    {
        "bid": 2,
        "datetime": "2024-02-26T13:28:03.479056Z",
        "id": 6,
        "image_link": null,
        "title": "Dracula",
        "type": "movie",
        "user": 3
    }
    ]"""
    """
Request for DELETE Bookmark
{
    "id" : 1,

}
"""
    def delete(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        bid = python_data.get('id')

        b = Bookmark.objects.filter(id=bid, user=user).first()
        if b is not None:
            b.delete()
            return Response({"message": "Bookmark Deleted"})
        return Response({"message":"No item to delete"}, status=status.HTTP_404_NOT_FOUND)
    

class BookmarkDetail(APIView):
    def get(self, view):
        pass