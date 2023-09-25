import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def checkCurrentDevice(sp,device_ID):
    playback = sp.current_playback() #get the current playback 
    return(playback != None and playback['device']['id']==device_ID)

    
def transferPlayback(sp,device_ID):
    sp.transfer_playback(device_id=device_ID)


def pausePlayback(sp):
    sp.pause_playback()


def findItem(sp,data):
    first = True
    type = 'track' #the type of item to return, for this project is track
    queryString = "" #

    if(data['songName']!=''):#if songname is not filled then nothing to play
        queryString+="track:\""+data['songName']+"\""#add the songname as the track to search
        if(data['artist']!=''):
            queryString+="+artist:\""+data['artist']+"\""#if the artist was said by the user then will also use that as a search param
        
        tracks = sp.search(queryString,limit=1,type=type)#search for the track said by the user, limit is 1 since we only play the first result returned
        if(tracks['tracks']['total']==0):
            return None
        else:
            songID = tracks['tracks']['items'][0]['uri']#grab the song URI from the returned array 
            return songID


def play(sp,songID): 
    playback = sp.current_playback()#get what is currently playing 
    if(playback!=None):#if there is something currently playing
        if(songID==playback['item']['uri'] and playback['is_playing']==False):#if it is the same song
            sp.start_playback()#play song
        elif(playback['is_playing']==True):
            pausePlayback(sp)
            sp.start_playback(uris=[songID])
    else:#if nothing currently playing then play the passed song
        sp.start_playback(uris=[songID])

def resumePlayback(sp):#resume the song that is currently paused
    sp.start_playback()


def callSpotifyAPI(action,data):
    device_ID = "98bb0735e28656bac098d927d410c3138a4b5bca" #device ID of the raspberry PI

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="9fe021b24a6a437dae1144e135c0bb7d",
    client_secret = "d54215d8d0714a22b20aa5e15d0e079f",
    redirect_uri="http://localhost/",
    scope="streaming,user-library-read,user-modify-playback-state,user-read-currently-playing,user-read-playback-state"))#authenticate with podium API to be able to make calls to API
    
    if(not checkCurrentDevice(sp,device_ID)):#check if the current playback device is the raspberry PI
       transferPlayback(sp,device_ID)#if it is not then transfer it to the raspberry PI
    if(action=='play' and (data['songName']!='' or data['artist']!='')):#if the user has specified play with song data then find and play the song
        songID = findItem(sp,data)
        if(songID==None):
            return False
        else:
            play(sp,songID)
            return True
    elif(action=='play'):#if no song data then resume playback
        resumePlayback(sp)
    elif action=='pause':#if user said pause then pause the current playback
        pausePlayback(sp)
            
