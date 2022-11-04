# python_tts
Very basic python bindings for ESpeak and Balcon. My only goal with this script was to homogenize the most obvious and basic features between the 2 engines.


You must provide your own Balcon and/or ESpeak executables, and dependencies. Make sure you place them in the respective folders. These folders must be in the same directory as `tts.py`


Below is every possible thing you can do. Balcon has one more feature than ESpeak ~ pause/resume can be toggled.

```python3
import tts

speaker = tts.ESpeak(voice='+f3',pitch=50,speed=175,draw=2,volume=200)
speaker.say("hello world")   #say text
speaker.say("c:/myfile.txt") #read file
print(speaker.reading)       #currently reading
speaker.stop()               #kill process
speaker.save("hello world")  #save only ~ no speaking
speaker.save("c:/myfile.txt")#save wave from file text
print(speaker.voices)        #list of available voices


speaker = tts.Balcon(voice='Hazel',pitch=2,speed=2,draw=20,volume=100)
speaker.say("hello world")   #say text
speaker.say("c:/myfile.txt") #read file
speaker.toggle()             #pause
speaker.toggle()             #resume
print(speaker.reading)       #currently reading
speaker.stop()               #kill process
speaker.save("hello world")  #save only ~ no speaking
speaker.save("c:/myfile.txt")#save wave from file text
print(speaker.voices)        #list of available voices
```


You can save the speech to `.wav` by either calling `.save(text_or_filepath)` or `.say(text_or_filepath, True)`. This will name the `wav` with the current timestamp, and save in a `tts_wav` directory that is created in whatever path `os.getcwd()` returns.

Both `Balcon` and `ESpeak` classes extend `TTS`. I think I made `TTS` generic enough to be easily extended for other tts command line engines.

Below are the "docs" for Balcon and Espeak commands, if you'd like to add more features to my script.

* [Balcon commands](http://www.cross-plus-a.com/bconsole.htm)
* [ESpeak commands](https://espeak.sourceforge.net/commands.html)
