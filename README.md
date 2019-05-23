# Retrieve Recently Played Songs from Spotify

Light wrapper for getting 20 most recent played songs on spotify and add them to local database

## Running

To run the program use command python apilayer.py which will open a web browser to authenticate Spotify. 
After inputting credentials the page will redirect to a localhost website. 
Copy this link into the terminal which will parse the link for relevant ID and authorization information.

The API wrapper includes functions for retrieving songs as well as their features and analysis from Spotify.
This is all added to a local CouchDB database with credentials placed in a different python file of authentication strings.
