import hashlib
import json
import os
import re
import urllib
import webbrowser


"""
 fresh_tomatoes.py
 =================
 This module takes a list of Movie objects and builds a standalone HTML page,
 then opens a browser tab with the resulting page.
"""

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>My Favorite Movies</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {{
            padding-top: 80px;
        }}
        .navbar-nav > li > a {{
            padding: 0px;
        }}
        .navbar-nav > li > a > img {{
            padding-top: 5px;
            padding-bottom: 0px;
            padding-right: 15px;
        }}
        .navbar-nav > li > .dropdown-menu {{
            margin-top: {dropdown_padding};
        }}
        .navbar-inverse {{
            background-image: none;
        }}
        #trailer .modal-dialog {{
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }}
        .hanging-close {{
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }}
        #trailer-video {{
            width: 100%;
            height: 100%;
        }}
        .modal-header {{
            background-color: #288DF7;
            color: #FFF;
        }}
        .movie-tile {{
            margin-bottom: 20px;
            padding-top: 20px;
            position: relative;
        }}
        .movie-tile-overlay {{
            visibility: hidden;
            position: absolute;
            height: 100%;
            width: 100%;
            opacity: 0;
            background: rgba(255,255,255,0);
            transition: background, opacity 350ms ease-in;
        }}
        .movie-tile-overlay span {{
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50%;
            width: 100%;
            margin: auto;
            left: -15px;
            font-size: 5rem;
        }}
        .movie-tile-overlay span i:hover {{
            cursor: pointer;
        }}
        .movie-tile:hover .movie-tile-overlay {{
            visibility: visible;
            cursor: default;
            opacity: 1;
            background: rgba(255,255,255,0.8);
        }}
        .scale-media {{
            padding-bottom: 56.25%;
            position: relative;
        }}
        .scale-media iframe {{
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }}
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {{
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        }});
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.play-button', function (event) {{
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {{
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }}));
        }});
        // Clicking the "info" button displays a modal with the movie data in it
        $(document).on('click', '.info-button', function (event) {{
            $('#info').find('#why').html($(this).data('why'));
            $('#info').find('#title').text($(this).data('title'));
            $('#info').find('#imdb-rating').text($(this).data('rating'));
            $('#info').find('#plot').text($(this).data('plot'));
            $('#info').find('#genre').text($(this).data('genre'));
            $('#info').find('#director').text($(this).data('director'));
            $('#info').find('#writers').text($(this).data('writers'));
            $('#info').find('#cast').text($(this).data('cast'));
            $('#info').find('#awards').text($(this).data('awards'));
            $('#info').find('#language').text($(this).data('language'));
            $('#info').find('#country').text($(this).data('country'));
            $('#info').find('#runtime').text($(this).data('runtime'));
        }});
        // Animate in the movies when the page loads
        $(document).ready(function () {{
          $('.movie-tile').hide().first().show("fast", function showNext() {{
            $(this).next("div").show("fast", showNext);
          }});
        }});
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Movie Info Modal -->
    <div class="modal" id="info">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title" id="title"></h2>
          </div>
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="modal-body">
            <span id="why"></span>
            <p><strong>IMDb Rating:</strong><br />
            <span id="imdb-rating"></span></p>
            <p><strong>Synopsis:</strong><br />
            <span id="plot"></span></p>
            <p><strong>Directed by:</strong><br />
            <span id="director"></span></p>
            <p><strong>Written by:</strong><br />
            <span id="writers"></span></p>
            <p><strong>Cast:</strong><br />
            <span id="cast"></span></p>
            <p><strong>Awards:</strong><br />
            <span id="awards"></span></p>
            <p><strong>Genre:</strong><br />
            <span id="genre"></span></p>
            <p><strong>Language:</strong><br />
            <span id="language"></span></p>
            <p><strong>Country of origin:</strong><br />
            <span id="country"></span></p>
            <p><strong>Runtime:</strong><br />
            <span id="runtime"></span></p>
          </div>
          <div class="modal-footer">
            <em>Movie info courtesy of the OMDb API (<a href="http://omdbapi.com/">http://omdbapi.com/</a>)</em>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="#">My favorite movies{author}</a>
        </div>
          <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{profile_image}</a>
              <ul class="dropdown-menu">
                {about_dropdown}
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center">
    <div class="movie-tile-overlay text-center"><span><i class="fa fa-info-circle info-button" title="View Movie Info" data-toggle="modal" data-target="#info" data-why="{why}" data-title="{movie_title} ({year_made})" data-plot="{storyline}" data-genre="{genre}" data-rating="{imdb_rating}/10 from {imdb_votes} votes" data-runtime="{runtime}" data-director="{director}" data-writers="{writers}" data-cast="{actors}" data-language="{language}" data-country="{country}" data-awards="{awards}"></i>{play_button}</span></div>
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)
        # Format 'why' statement as a Bootstrap blockquote, if present
        if (movie.why != ""):
            the_why = "<blockquote>" + movie.why + "</blockquote>"
        else:
            the_why = ""

        # Generate movie trailer play button if a YouTube URL
        # is present in the Movie object. Otherwise don't.
        if trailer_youtube_id:
            play_button = '&nbsp;&nbsp;<i class="fa fa-play-circle '
            play_button += 'play-button" title="Watch Trailer" data-'
            play_button += 'trailer-youtube-id="' + trailer_youtube_id
            play_button += '" data-toggle="modal" data-target="#trailer"></i>'
        else:
            play_button = ""

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            why=the_why,
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            storyline=movie.storyline,
            genre=movie.genre,
            year_made=movie.year_made,
            imdb_rating=movie.imdb_rating,
            imdb_votes=movie.imdb_votes,
            runtime=movie.movie_length,
            director=movie.director,
            writers=movie.writers,
            actors=movie.cast,
            language=movie.language,
            country=movie.country_of_origin,
            awards=movie.awards,
            play_button=play_button
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Build the custom navbar using info from profile.json, if present.
    author = ""
    profile_image = ""
    about_dropdown = ""
    dropdown_padding = "5px"
    has_profile_info = 0
    try:
        with open('profile.json') as profile_file:
            profile = json.load(profile_file)
            if ('name' in profile):
                author = " by: " + profile['name']

            # Add in a profile image from gravatar and social media links
            # in a dropdown menu on the right side of the navbar.
            if ('gravatar_email' in profile and
                    profile['gravatar_email'] != ""):
                email = profile['gravatar_email']
                size = 40
                gravatar_url = "http://www.gravatar.com/avatar/"
                gravatar_url += hashlib.md5(email.lower()).hexdigest() + "?"
                gravatar_url += urllib.urlencode({'s': str(size)})
                profile_image = '<img src="' + gravatar_url + '" />'
            else:
                profile_image = '<span class="navbar-brand">About Me</span>'
                dropdown_padding = "20px"

            if ('email' in profile and
                    profile['email'] != ""):
                about_dropdown += '<li><a href="mailto:' + profile['email']
                about_dropdown += '" target="new"><i class="fa fa-envelope '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Spam Me</a></li>'
                has_profile_info = 1
            if ('facebook' in profile and
                    profile['facebook'] != ""):
                about_dropdown += '<li><a href="' + profile['facebook']
                about_dropdown += '" target="new"><i class="fa fa-facebook '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;The '
                about_dropdown += 'Facebook</a></li>'
                has_profile_info = 1
            if ('twitter' in profile and
                    profile['twitter'] != ""):
                about_dropdown += '<li><a href="' + profile['twitter']
                about_dropdown += '" target="new"><i class="fa fa-twitter '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Make With The '
                about_dropdown += 'Tweets</a></li>'
                has_profile_info = 1
            if ('github' in profile and
                    profile['github'] != ""):
                about_dropdown += '<li><a href="' + profile['github']
                about_dropdown += '" target="new"><i class="fa fa-github '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Git \'er Done '
                about_dropdown += 'Hub</a></li>'
                has_profile_info = 1
            if ('linkedin' in profile and
                    profile['linkedin'] != ""):
                about_dropdown += '<li><a href="' + profile['linkedin']
                about_dropdown += '" target="new"><i class="fa fa-linkedin '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Link Me In '
                about_dropdown += '</a></li>'
                has_profile_info = 1
            if ('tumblr' in profile and
                    profile['tumblr'] != ""):
                about_dropdown += '<li><a href="' + profile['tumblr']
                about_dropdown += '" target="new"><i class="fa fa-tumblr '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Tumblr Dry Low '
                about_dropdown += '</a></li>'
                has_profile_info = 1
            if ('instagram' in profile and
                    profile['instagram'] != ""):
                about_dropdown += '<li><a href="' + profile['instagram']
                about_dropdown += '" target="new"><i class="fa fa-instagram '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Watch Your '
                about_dropdown += 'Instagrammar</a></li>'
                has_profile_info = 1
            if ('google+' in profile and
                    profile['google+'] != ""):
                about_dropdown += '<li><a href="' + profile['google+']
                about_dropdown += '" target="new"><i class="fa fa-google-plus '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Plus Google '
                about_dropdown += '</a></li>'
                has_profile_info = 1
            if ('pinterest' in profile and
                    profile['pinterest'] != ""):
                about_dropdown += '<li><a href="' + profile['pinterest']
                about_dropdown += '" target="new"><i class="fa fa-pinterest '
                about_dropdown += 'fa-fw"></i>&nbsp;&nbsp;Put a Pin In That '
                about_dropdown += '</a></li>'
                has_profile_info = 1
    except (IOError, ValueError):
        pass

    # If there's no social media info, don't display the dropdown menu.
    if (has_profile_info == 0):
        profile_image = ""

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        author=author,
        profile_image=profile_image,
        about_dropdown=about_dropdown
    )
    # Minor adjustment to CSS depending on whether there's
    # a profile image or not.
    head_content = main_page_head.format(
        dropdown_padding=dropdown_padding
    )

    # Output the file
    output_file.write(head_content + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
