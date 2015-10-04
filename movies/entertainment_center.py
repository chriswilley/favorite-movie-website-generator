import fresh_tomatoes
import json
import media
import sys
import urllib


"""
 entertainment_center.py
 =======================
 This module reads a list of movies from a json file (named movies.json)
 and creates a standalone HTML page that can be shared or placed on a web
 server for viewing. Allowed parameters in movies.json are:

    +--------------------------------------------------------------+
    | *imdbID             The ID of the movie (e.g.: tt0094625)    |
    | youtube_trailer     A YouTube URL for the movie trailer      |
    | why                 A statement about why you like the movie |
    +--------------------------------------------------------------+
        * required

 Movie data is compiled from the Open Movie Database (OMDb) API
 (http://omdbapi.com).

 The HTML page may be further customized by creating another JSON file
 called profile.json. Specific information in this file will make adjustments
 to the page header navbar (such as adding a profile image from gravatar
 and providing links to your social media profiles).

 See README.md for installation and other instructions.
"""

# Start by opening the movies file, which must be named movies.json and
# be in the current folder.
try:
    with open('movies.json') as movie_file:
        movie_list = json.load(movie_file)
except IOError:
    # JSON file is not present; exit
    sys.exit('Movie file not found!')
except ValueError:
    # JSON file is formatted incorrectly; exit
    err_msg = "The movie file is not formatted properly. "
    err_msg += "Try http://jsonlint.com/ to see what might be wrong."
    sys.exit(err_msg)

movies = []

# Print a simple status message to the screen
sys.stdout.write("Generating movies web page...")
sys.stdout.flush()

for idx, movie in enumerate(movie_list):
    # Iterate through the movies in the JSON file and build
    # a list of Movie objects to send to fresh_tomatoes.py
    #
    # Increment the status message
    sys.stdout.write('.')
    sys.stdout.flush()

    if movie_list[idx]['imdbID']:
        # Build the API URL
        omdb_url = "http://www.omdbapi.com/?i="
        omdb_url += movie_list[idx]['imdbID']
        omdb_url += "&plot=short&r=json"

        # Call the OMDb API and parse the JSON data in the response
        movie_json = urllib.urlopen(omdb_url)
        movie_obj = json.load(movie_json)

        if (movie_obj['Response'] == "True"):
            # If a movie is found (i.e.: the imdbID was valid), create
            # a Movie object from the data. Otherwise don't.
            why = ""
            try:
                why = movie_list[idx]['why']
            except KeyError:
                pass
            youtube = movie_list[idx]['youtube_trailer'] or ""

            this_movie = media.Movie(
                why,
                movie_obj['imdbID'],
                movie_obj['Year'],
                movie_obj['Rated'],
                movie_obj['Runtime'],
                movie_obj['Genre'],
                movie_obj['Director'].encode('utf-8'),
                movie_obj['Writer'].encode('utf-8'),
                movie_obj['Actors'].encode('utf-8'),
                movie_obj['Language'],
                movie_obj['Country'],
                movie_obj['Awards'].encode('utf-8'),
                movie_obj['imdbRating'],
                movie_obj['imdbVotes'],
                movie_obj['Title'],
                movie_obj['Plot'].encode('utf-8'),
                movie_obj['Poster'],
                youtube)
            movies.append(this_movie)

# Sort the list of Movie objects by title
movies = sorted(movies, key=lambda movie: movie.title)

sys.stdout.write('\nDone! Launching browser...\n')
sys.stdout.flush()

# Pass the list to fresh_tomatoes.py to create the HTML file
fresh_tomatoes.open_movies_page(movies)
