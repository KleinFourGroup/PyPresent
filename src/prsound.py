import pyaudio
import wave
import os.path

def initSoundStream(FORMAT = pyaudio.paInt16, CHANNELS = 2, CHUNK = 4096, RATE = 44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=11)
    return p, stream

def cleanSoundStream(p, stream):
    stream.stop_stream()
    stream.close()
    p.terminate()
    
def writeSound(p, fout, buf, CHANNELS=2, FORMAT=pyaudio.paInt16, RATE=44100):
    wf = wave.open(os.path.join("assets", fout), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(buf))
    wf.close()
