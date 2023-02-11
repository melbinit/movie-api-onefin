# Create your views here.
from typing import Collection
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.serializers import CollectionSerializer, UserSerializer,GetCollectionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Collection, RequestsData
from .get_top_genres import get_top_3_genres

class RegisterUserAPIView(generics.CreateAPIView):
    # For registering new user. Returns an access token.
    permission_classes = (AllowAny,) # Allow any user (authenticated or not) to access this url 
    
    def create(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        resp = {"access_token": str(refresh.access_token)}
        return Response(resp, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_movies(request):
    # get movies from credy. page number can be specified in params.
    page_num = request.GET.get("page", None)
    if page_num:
        movie_url = f'https://demo.credy.in/api/v1/maya/movies?page={page_num}'
    else:
        movie_url = 'https://demo.credy.in/api/v1/maya/movies/'
    try:
        resp = requests.get(movie_url).json()
        return Response(resp, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Request failed."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def collections(request, uuid=None):
    if request.method == 'GET':
        if uuid: # if uuid is passed 
            try:
                collection = Collection.objects.get(uuid=uuid)
                serializer = CollectionSerializer(collection)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        user_collection = Collection.objects.filter(user=request.user)
        favorite_genres = get_top_3_genres(user_collection)
        serializer = GetCollectionSerializer(user_collection, many=True)
        # print(serializer.keys())
        res = {"is_success": True,
               "data": {} }
        res["data"]["collections"] = serializer.data
        res["favourite_genres"] = favorite_genres
        return Response(res, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({"collection_uuid":serializer.data["uuid"]}, status=status.HTTP_201_CREATED)
    
    if request.method == 'PUT':
        try:
            if uuid:
                collection = Collection.objects.get(uuid=uuid)
                serializer = CollectionSerializer(
                    instance=collection, data=request.data)

                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"error":"UUID required." }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        try:
            if uuid:
                collection = Collection.objects.get(uuid=uuid)
                collection.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error":"UUID required." }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_requests_data(request):
    # returns the total count of requests stored in RequestsData model.
    total_requests = RequestsData.objects.all().count()
    return Response({"requests": total_requests}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_requests_data(request):
    # deletes all request logs from RequestData model.
    RequestsData.objects.all().delete()
    return Response(status=status.HTTP_200_OK)
