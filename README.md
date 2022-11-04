# python_tts
Very basic python bindings for ESpeak and Balcon


You must have Balcon and/or ESpeak in a `balcon` and/or `espeak` directory (respectively), in the same directory as `tts.py`.


usage:
```
import tts

speaker = tts.ESpeak(voice='+f3',pitch=50,speed=175,draw=2)
speaker.say("hello world")
print(speaker.voices)

speaker = tts.Balcon(voice='Hazel',pitch=2,speed=2,draw=20)
speaker.say("hello world")
print(speaker.voices)
```
