#rom whisper_mic import WhisperMic
from llama_cpp import Llama
import settings

llm = Llama(settings.MODEL_PATH,n_gpu_layers=24)
#mic = WhisperMic(model="medium")
history = []

def transcribe_audio():
  print("話してください...")
  result = input()#mic.listen()
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