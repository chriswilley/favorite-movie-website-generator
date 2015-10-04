# Favorite Movies Website Generator

Create your own "favorite movies" website quickly and easily! It's even more fun than it sounds!


## Table of contents

* [Installation](#installation)
* [Creating the site](#creating-the-site)
* [The movie list](#the-movie-list)
* [Customizing the header](#customizing-the-header)
* [Creator](#creator)
* [Copyright and license](#copyright-and-license)


## Installation

For starters, you need [Python](https://www.python.org/downloads/). The program was written for Python 2.7, so that's what you should download and install. You may already have Python, especially if you're on a Mac or Linux machine. To check, open a Terminal window (on a Mac, use the Spotlight search and type in "Terminal"; on a PC go to Start > Run and type in "cmd") and type "python" at the prompt. You should get something that looks like this (run on my Mac):

```
Python 2.7.10 (v2.7.10:15c95b7d81dc, May 23 2015, 09:33:12)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Note the version number (2.7.10 in this case). If it starts with "3.", you should download version 2.7. If you have questions about any of this, check Python's [excellent online documentation](https://www.python.org/doc/).

You'll also need [git](http://git-scm.com/download) so that you can clone this project. If you don't have and/or would prefer not to install git, you can download the movies.zip file and extract it into its own folder.


## Creating the site

Once you have the project files, go to a command prompt (instructions above) and type:

```
python entertainment_center.py
```

After the program runs, you'll see a new file called fresh_tomatoes.html in the same folder. The file will also pop open in your web browser.

When you hover over a movie poster with your mouse, you'll see an "info" button (and a "play" button if you included a YouTube trailer URL for the movie). Clicking on "info" will bring up a window that displays a lot of cool information about the movie. This data comes from the awesome [Open Movie Database API](http://omdbapi.com/). And hey, you didn't have to type any of it in! W00t!

If you run the program straight away, you'll see **my** favorite movies (not a bad thing :)). In order to have the page show **your** favorite movies, read on.


## The movie list

The list of movies is contained in a file called "movies.json". You got that file when you git-cloned or unzipped the project. Simply edit this sample file with your own favorite movies.

The parameters in the JSON file are as follows (all parameters are case-sensitive):

Parameter | What it is | Required?
--- | --- | :---:
imdbID | The ID of the movie in IMDb.com. For example, the movie *Akira* is tt0094625. | Y
youtube_trailer | The YouTube URL of the movie's trailer video. | N
why | A short statement about why you love the movie. | N

To get a movie's IMDb ID, search for the movie on [imdb.com](http://imdb.com). When you're viewing a movie's record, the ID will be in the URL.

Make sure to keep the formatting of the movies.json file exactly the same as the sample provided, otherwise the program will not run.


## Customizing the header

You can also change the way the header displays in the HTML file by modifying the profile.json file. As with movies.json, make sure to leave the formatting intact but change the content to fit you. You can add in any of the following pieces of info about you:

* Your name
* Your email address
* The email address you registered at [gravatar](https://secure.gravatar.com/) (and really, why wouldn't you have?) in order to display your photo/gravatar
* Links to your social media profiles at any of the following:
  * Facebook
  * Twitter
  * Github
  * Tumblr
  * Google+
  * Pinterest
  * LinkedIn
  * Instagram


## Creator

This program was built by me, Chris Willey, as part of the Udacity Nanodegree program for [Full Stack Developer](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).


## Copyright and License

Code and documentation copyright 2015 Christopher Willey. Code released under the MIT license.