from whisper_mic import WhisperMic

mic = WhisperMic(model="medium")
while True:
  result = mic.listen()
  print(result)