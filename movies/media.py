class Movie():
    """
    Creates a Movie object with many relevant pieces of movie info.
    """

    def __init__(self,
                 why,
                 imdb_id,
                 year_made,
                 rating,
                 movie_length,
                 genre,
                 director,
                 writers,
                 cast,
                 language,
                 country_of_origin,
                 awards,
                 imdb_rating,
                 imdb_votes,
                 movie_title,
                 movie_storyline,
                 poster_image,
                 trailer_youtube):
        self.why = why
        self.imdb_id = imdb_id
        self.year_made = year_made
        self.rating = rating
        self.movie_length = movie_length
        self.genre = genre
        self.director = director
        self.writers = writers
        self.cast = cast
        self.language = language
        self.country_of_origin = country_of_origin
        self.awards = awards
        self.imdb_rating = imdb_rating
        self.imdb_votes = imdb_votes
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
