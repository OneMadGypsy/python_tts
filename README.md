# python_tts
Very basic python bindings for ESpeak and Balcon. My only goal with this script was to homogenize the most obvious and basic features between the 2 engines.


You must provide your own Balcon and/or ESpeak executables, and dependencies. Make sure you place them in the respective folders. These folders must be in the same directory as `tts.py`


Below is every possible thing you can do. Balcon has one more feature than ESpeak ~ pause/resume can be toggled. The only discrepency in attributes between `Balcon` and `ESpeak` are `gap` related. ESpeak only has one form of gap, the pause between words in 10ms units. Balcon has two gaps. The pause after sentences in ms (`sgap`) and the pause after paragraphs in ms (`pgap`).

```python3
import tts

speaker = tts.ESpeak(voice='+f3',pitch=50,speed=175,gap=2,volume=200)
speaker.say("hello world")   #say text
speaker.say("c:/myfile.txt") #read file
print(speaker.reading)       #'is_reading' property, but it's really an `is_process_still_open` property
speaker.stop()               #kill process
speaker.save("hello world")  #save only ~ no speaking
speaker.save("c:/myfile.txt")#save wave from file text
print(speaker.voices)        #list of available voices


speaker = tts.Balcon(voice='Hazel',pitch=2,speed=2,sgap=20,pgap=20,volume=100)
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

If you'd like to add more features to my script or determine the acceptable values:

* [Balcon commands](http://www.cross-plus-a.com/bconsole.htm)
* [ESpeak commands](https://espeak.sourceforge.net/commands.html)
