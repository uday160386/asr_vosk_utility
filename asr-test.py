import wave
import sys

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from vosk import Model, KaldiRecognizer

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    sys.exit(1)

model = Model(lang="en-us")

asr_rec = KaldiRecognizer(model, wf.getframerate())
asr_rec.SetWords(True)
asr_rec.SetPartialWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if asr_rec.AcceptWaveform(data):
        print(asr_rec.Result())
    else:
        print(asr_rec.PartialResult())

print(asr_rec.FinalResult())