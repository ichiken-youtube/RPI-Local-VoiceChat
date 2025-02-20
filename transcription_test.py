from whisper_mic import WhisperMic

mic = WhisperMic(model="medium")
result = mic.listen()
print(result)