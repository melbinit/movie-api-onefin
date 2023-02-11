from rest_framework import serializers
from .models import Collection, Movie, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}
    
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        exclude = ["user"]

    def create(self, validated_data):
        movies = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)
        movie_list = []
        for movie in movies:
            new, _ = Movie.objects.get_or_create(**movie)
            movie_list.append(new)
        collection.movies.set(movie_list)
        return collection

    def update(self, instance, validated_data):
        if "title" in validated_data:
            instance.title = validated_data.get('title')
        if "description" in validated_data:
            instance.description = validated_data.get('description')
        if "movies" in validated_data:
            movies = validated_data.get('movies')
            if len(movies) > 0:
                movie_list = []
                for movie in movies:
                    new_movie, _ = Movie.objects.get_or_create(**movie)
                    movie_list.append(new_movie)
                instance.movies.set(movie_list)
        instance.save()
        return instance

class GetCollectionSerializer(serializers.ModelSerializer):

     class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description')