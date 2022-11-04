# python_tts
Very basic python bindings for ESpeak and Balcon


In the same directory as `tts.py`, you must have Balcon and/or ESpeak in a `balcon` and/or `espeak` directory (respectively).


usage:

```python3
import tts

speaker = tts.ESpeak(voice='+f3',pitch=50,speed=175,draw=2)
speaker.say("hello world")
print(speaker.voices)

speaker = tts.Balcon(voice='Hazel',pitch=2,speed=2,draw=20)
speaker.say("hello world")
print(speaker.voices)
```

The `.say` method accepts either the text to speak or the filepath of a document to read.

You can save the speech to `.wav` by either calling `.save(text_or_filepath)` or `.say(text_or_filepath, True)`. This will name the `wav` with the current timestamp, and save in a `tts` directory that is created in whatever path `os.getcwd()` returns.

Balcon has a `.toggle` method that can pause/resume speech

* [Balcon commands](http://www.cross-plus-a.com/bconsole.htm)
* [ESpeak commands](https://espeak.sourceforge.net/commands.html)
