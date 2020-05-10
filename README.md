# cis192FinalProject
Jonathan Zein and Akshay Sharma

Akshay Sharma PennKey: aksharma

Jonathan Zein PennKey: jzein

# Description
Multi-page web app that uses HTML/CSS/Python to provide music recommendations to users by making requests to the Spotify API. Uses Flask for relevant webpage routing and template rendering, and the open-source Spotipy library to handle requests made to the Spotify API. 

# Dependencies and Instructions
In order to run this app locally, install the following packages to your virtual environment:

``` pip install spotipy ```

``` pip install flask ```


Upon running the server, you will be redirected to the app's main page where you can input your favorite genre, 
an adjective that describes your current mood, and a decimal between 0 and 1 (e.g 0.8, 0.7) that corresponds to how energetic you want your music to be. 
Click submit, and the app will redirect you to a page that displays your song recommendation, accompanied by some cool album cover art!


# Limitations
There are a couple of relevant limitations which should be noted. 

First, there's only some mood adjectives that work as of now. The following are the mood adjectives that will work:

["excited", "enthusiastic", "happy", "romantic", "mad", "sad", "depressed", "nervous", "indifferent"]


Second, the Spotify API only has a finite list of genres that can be queried. In theory, this list should be pretty 
expansive but if a genre provided on the webpage's form isn't in that list, then the application automatically 
queries the api with the default genre being "pop".




