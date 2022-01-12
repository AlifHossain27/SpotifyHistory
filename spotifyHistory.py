import os
import json
import requests
from datetime import date
from refresh import Refresh

user_id = os.getenv("USER")
playlist_id = os.getenv("PLAYLIST_ID")

class SpotifyHistory:
    def __init__(self):
        self.user_id = user_id
        self.playlist_id = playlist_id
        self.tracks = ""
        self.token = ""

    def find_songs(self):
        print("Finding recently played songs...")

        query = "https://api.spotify.com/v1/me/player/recently-played"

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.token)},
                                         params={"limit":20})
        response_json= response.json()
        
        for i in response_json["items"]:
            self.tracks += i["track"]["uri"] + ","
        self.tracks = self.tracks[:-1]
        self.add_history()


    def add_history(self):
        print("Adding to History...")

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlist_id)

        response = requests.put(query,headers={"Content-Type":"application/json","Authorization":"Bearer {}".format(self.token)},params={"uris":self.tracks})
        

    def call_refresh(self):
        print("Refreshing token...")

        refreshCaller = Refresh()
        self.token = refreshCaller.refreshing()
        self.find_songs()


if __name__=="__main__":
    history=SpotifyHistory()
    history.call_refresh()