from collections import Counter

def get_top_3_genres(queryset): 
    genres = []
    for collection in queryset:
        for movie in collection.movies.all():
            genre_split = movie.genres.split(',')
            genres.extend(genre_split)
    top_3 = Counter(genres).most_common(3)
    return [ genre[0] for genre in top_3]