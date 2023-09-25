import speech_recognition as sr
import pyttsx3
import pywhatkit
import spotifyAPIFunctions


listener = sr.Recognizer()#initialize the speech recognizer
response = pyttsx3.init()#initialize the speaker 
voices = response.getProperty('voices')
response.setProperty('voice', voices[0].id)#set the voice to male english for speaking


def talk(text):
    response.say(text)
    response.runAndWait()


def take_command():
    command=""
    try:
        with sr.Microphone() as source:
            
            listener.adjust_for_ambient_noise(source)
            talk('I am listening')
            print("start speaking:")
            audio = listener.listen(source)
            command = listener.recognize_google(audio,language = "en-US")
            command = command.lower()
            if 'spotify' in command:
                command = command.replace('spotify ', '')
    except:
        pass
    return command


def run_player():
    data = {'artist':'','songName':''}
    command = take_command()
    print(command)
    if 'play' in command: #if user said play
        if len(command) > 4:#if the user only said play then play current song
            playIdx = command.index('play')
            byIdx = None
            try: #check if user specified an artist
                byIdx = command.index('by')
            except:
                byIdx=None
            if(byIdx==None):#were just going to grab the song if artist not specified
                song = command[playIdx+4]
            else:#grab artist and the song name othewise
                song = command[playIdx+4:byIdx]
                artist = command[byIdx+2:]
                data['artist']=artist
            data['songName']=song   
            
        flag = spotifyAPIFunctions.callSpotifyAPI('play',data)#call functions that interact with spotify API
        if(flag):#if song was found then say song being played
            if(byIdx==None):
                song = command[playIdx+4]
                talk('now playing' + song)
        
            else:
                song = command[playIdx+4:byIdx]
                artist = command[byIdx+2:]
                talk('now playing' + song + "by" + artist)
        elif(flag==False):#othewise let user know that song could not be found
            talk('I could not find that song')
    elif 'pause' in command:#if the user said pause then pause current song playing
        spotifyAPIFunctions.callSpotifyAPI('pause',data)

run_player()
