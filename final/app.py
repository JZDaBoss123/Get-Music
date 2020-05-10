from flask import Flask, redirect, url_for, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
from random import seed

SPOTIFY_CLIENT_ID = "ea9c663491c24f0385d3f6bccc24b0ad"
SPOTIFY_CLIENT_SECRET = "38d10dc3a32d4f18b88a68988fa71931"

client_credentials = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)

app = Flask(__name__)
global_cache = {}  # cache to store POST requests, cannot handle concurrent connections as of now


class Recommendations:
    def __init__(self, mood, genre, energy, num_songs):
        self.mood = mood
        self.genre = genre
        self.energy = energy
        self.num_songs = num_songs

    def generate_recommendations(self):
        '''
        Queries the Spotify API to generate recommendations based on relevant seeds (e.g genre, valence)
            args: none
            ret:
                sp.recommendations(seeds). Result that corresponds to num_songs music recommendations
                with all the relevant data associated with them (e.g artist, album, cover art)
        '''
        valence = self.get_valence()
        tgt_genre = self.genre

        all_genres = sp.recommendation_genre_seeds()

        if self.genre not in all_genres['genres']:
            return sp.recommendations(seed_genres=['pop'], country='US', target_valence=valence,
                                      target_energy=self.energy)
        if self.energy is None:
            return sp.recommendations(seed_genres=[tgt_genre], country="US", target_valence=valence)

        return sp.recommendations(seed_genres=[tgt_genre], country="US", target_valence=valence,
                                  target_energy=self.energy)

    def get_valence(self):
        '''
        creates a song valence (positivity) based on self.mood input.
            args: none
            ret:
                tgt_valence: a double between 0 and 1.
        '''

        tgt_valence = 0
        if self.mood is "excited" or "enthusiastic":
            tgt_valence = 0.9
        if self.mood is "happy":
            tgt_valence = 0.8
        elif self.mood is "romantic":
            tgt_valence = 0.7
        elif self.mood is "nervous":
            tgt_valence = 0.6
        elif self.mood is "indifferent":
            tgt_valence = 0.5
        elif self.mood is "mad":
            tgt_valence = 0.4
        elif self.mood is "sad":
            tgt_valence = 0.2
        elif self.mood is "depressed":
            tgt_valence = 0.1

        return tgt_valence


@app.route('/')
def home():
    '''
    Redirect the user from the root / URL to the /preferences URL
    args: None
    ret:
        The required return by Flask so the user is
        redirected to the /uploads URL
    '''
    return redirect(url_for('starter_page'))


@app.route('/preferences', methods=["GET", "POST"])
def starter_page():
    '''
       Handle GET and POST requests for the /preferences URL.
       GET requests should display the index.html template.
       POST requests should check the validity of the request and
       get the relevant data from the form, and add it to the global_cache.
       Return a redirect when the POST request is handled correctly.
       args: None
       ret:
           The required return by Flask so the user can see the
           HTML template on the GET request and the redirect to the
           appropriate /song url after the POST request.
    '''

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        result = request.form
        if 'genre' and 'mood' and 'energy' not in global_cache:
            global_cache['genre'] = str.lower(result['genreInput'])
            global_cache['mood'] = str.lower(result['moodInput'])
            global_cache['energy'] = str.lower(result['energyInput'])
        else:
            global_cache['genre'] = str.lower(result['genreInput'])
            global_cache['mood'] = str.lower(result['moodInput'])
            global_cache['energy'] = str.lower(result['energyInput'])

    return redirect(url_for('output_song'))


def generate_recommendation():
    '''
        generates recommendations by instantiating the Recommendations class
        and providing inputs such as the tgt_genre, tgt_mood, and tgt_energy from the
        global_cache to generate recommendations/
        args: none
        ret:
            song_artist_dictionary: mapping between songs and their artists
            song_album_dictionary: mapping between songs and their album cover art
    '''
    tgt_genre = global_cache['genre']
    tgt_mood = global_cache['mood']
    tgt_energy = global_cache['energy']

    if tgt_energy is "":
        tgt_energy = None

    recommendations = Recommendations(tgt_mood, tgt_genre, tgt_energy, 10)
    result = recommendations.generate_recommendations()

    song_artist_dictionary = {}
    song_album_dictionary = {}
    if result:
        for track in result['tracks'][: 10]:
            song = track['name']
            artist = track['album']['artists'][0]['name']
            album_cover = track['album']['images'][0]['url']
            song_artist_dictionary[song] = artist
            song_album_dictionary[song] = album_cover

    return song_artist_dictionary, song_album_dictionary


@app.route("/song")
def output_song():
    '''
       Handle GET requests for the /song URL. Uses the recommendations
       from the previous generate_recommendations() function and random number
       generation to "shuffle" recommendations if given the same parameters.
       Includes proper error message ("couldn't find a song, try again!")
       args: None
       ret:
           The required return by Flask to display the rec.html final template
    '''
    song_dictionary, song_album_dictionary = generate_recommendation()

    song_list = list(song_dictionary.keys())
    artist_list = list(song_dictionary.values())
    album_cover_list = list(song_album_dictionary.values())

    seed(1)
    song_index = randint(0, 9)
    if request.method == "GET":
        if song_list is None:
            return render_template("rec.html", songName="couldn't find a song! Try again!")
        if song_list[song_index] is None:
            return render_template("rec.html", songName="couldn't find a song! Try again!")
        else:
            songName = song_list[song_index] + "\n" + "by" + "\n" + "\n" + artist_list[song_index]
            imgName = album_cover_list[song_index]
            return render_template("rec.html", songName=songName, imgName=imgName)


if __name__ == '__main__':
    app.run()
