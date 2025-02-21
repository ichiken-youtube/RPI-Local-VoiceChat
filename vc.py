from whisper_mic import WhisperMic
from llama_cpp import Llama
import settings
from error_hider import noalsaerr
import os
import contextlib

llm = Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True)
with contextlib.redirect_stdout(open(os.devnull, 'w')):
  mic = WhisperMic(model="medium")
history = [{"role": "system", "content": "You are helpful assistant."}]

def transcribe_audio():
  print("話してください...")
  with open(os.devnull, 'w') as f: #noalsaerr():
    with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
      result = mic.listen()
  #text = result["text"]
  print(">>>", result)
  return result

def chat_with_llama(text):
  history.append({"role": "user", "content": text})
  output = llm.create_chat_completion(
    messages=history,
    max_tokens=256
  )
  response = output["choices"][0]["message"]["content"]
  history.append({"role": "assistant", "content": response})
  print(response)
  return response

def main():
  while True:
    text = transcribe_audio()
    if text.lower() in ["exit", "quit", "終了"]:
      print("終了します。")
      break
    response = chat_with_llama(text)

if __name__ == "__main__":
  main()
