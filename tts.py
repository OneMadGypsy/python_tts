import re, os, subprocess, time
from dataclasses import dataclass, asdict, field

#basic text filtering
PAUSE_RE     = re.compile(r'[\-]{2,}')
STRIPTAGS_RE = re.compile(r'<.+?>')
GRAMMAR_RE   = re.compile(r'[^\w\n ,!?();\-\.]', re.I)

#main paths
CWD          = os.getcwd()
TTSDIR       = '\\'.join(__file__.split('\\')[:-1])
TTSSAVE      = os.path.join(CWD, 'tts_wav')

if not os.path.isdir(TTSSAVE): os.mkdir(TTSSAVE) #create if necessary


@dataclass #base TTS object
class TTS:
    voice  :str = '' 
    pitch  :int = 0  
    speed  :int = 0  
    volume :int = 100
    
    @property
    def asdict(self) -> dict:
        return asdict(self)
        
    def __post_init__(self):
        self._sp = None  #subprocess
        
    @property
    def reading(self) -> bool:
        return (self._sp and (self._sp.poll() is None))
        
    def stop(self):
        if self.reading: self._sp.kill()

    def save(self, data):
        self.say(data, True)
        
    def say(self, data:str, towav:bool=False) -> None:
        raise NotImplementedError('TTS.say: method must be overwritten in a subclass')
            
    def _prepare(self, data:str, towav:bool=False) -> str:
        self.stop()
        
        self._isfile = os.path.isdir('\\'.join(data.split('\\')[:-1]))
        
        if not self._isfile:
            data =  PAUSE_RE.sub('.', GRAMMAR_RE.sub('', STRIPTAGS_RE.sub('', data)))
            
        towav = ('','-w')[towav]
        path  = '' if not towav else os.path.join(TTSSAVE, f'tts_{int(time.time())}.wav')
        src   = ('-t','-f')[self._isfile]
            
        return data, towav, path, src
        
         

#ESPEAK
#espeak has no built-in method for pause/resume and making one isn't worth it


ESPEAKPATH  = os.path.join(TTSDIR    , 'espeak')
ESPEAKEXE   = os.path.join(ESPEAKPATH, 'espeak')
ESPEAKVOICE = re.compile(r'!v\\([\w]+)')


@dataclass
class ESpeak(TTS):
    gap :int = 0
    
    @property #get available voices as a list by parsing stdout
    def voices(self):
        cmd = (ESPEAKEXE, '--voices=variant')
        return sorted(m.group(1) for m in ESPEAKVOICE.finditer(subprocess.check_output(cmd).decode('utf8')))

    def say(self, data:str, towav:bool=False):
        data, towav, path, src = self._prepare(data, towav)
        
        if self._isfile: data = f'{src}{data}'
        
        data = data if not towav else towav, path, data
        
        self._sp = subprocess.Popen(
            (ESPEAKEXE, '-m',        #-m is parse SSML or XML, mostly IGNORE HTML, plain text will still work
             f'--path={ESPEAKPATH}', #parent of espeak-data folder
             '-v', f'{self.voice}' , #set voice +m1-7 +f1-4
             '-s', f'{self.speed}' , #set speed in words-per-minute 
             '-p', f'{self.pitch}' , #adjust pitch 0 to 99
             '-g', f'{self.gap}'   , #pause between words in units of 10ms
             '-a', f'{self.volume}', #set amplitude 0 to 200
             *data)
        )


#BALCON
#balcon can have more commands fed in after it has been opened
#pause, resume and stop are built in


BALCONPATH = os.path.join(TTSDIR    , 'balcon')
BALCONEXE  = os.path.join(BALCONPATH, 'balcon')


@dataclass
class Balcon(TTS):
    sgap   :int = 0  #length of pause after paragraph (ms)
    pgap   :int = 0  #length of pause after paragraph (ms)
    
    @property #get available voices as a list by parsing stdout
    def voices(self) -> list[str]:
        cmd    = (BALCONEXE, '-l')
        data   = subprocess.check_output(cmd).decode('utf8').split(':')[1].strip()
        return sorted(name.strip() for name in data.split('\n'))
        
    #balcon pause/resume cmd
    def toggle(self):
        if self.reading: 
            subprocess.Popen((BALCONEXE, '-pr')) #pause/resume
    
    #balcon stop cmd    
    def stop(self):
        if self.reading: 
            subprocess.Popen((BALCONEXE, '-ka')) #kill active
            
    # `data` can be text or a file path
    def say(self, data:str, towav:bool=False):
        data, towav, path, src = self._prepare(data, towav)
        
        self._sp = subprocess.Popen(
            (BALCONEXE, 
             src  , data            , 
             '-n' , self.voice      , #sets the voice
             '-s' , f'{self.speed}' , #set speed -10 to 10
             '-p' , f'{self.pitch}' , #adjust pitch -10 to 10
             '-e' , f'{self.sgap}'  , #pause between sentences in ms
             '-a' , f'{self.pgap}'  , #pause between paragraphs in ms
             '-v' , f'{self.volume}', #volume 0 to 100
             towav, path) 
        )
