
from llama_cpp import Llama
import settings
import os
import contextlib

llm = Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True)
history = [{"role": "system", "content": "あなたは公安6課で開発されたAIです。開発コードネームはP-2501です。"}]


def chat_with_llama(text,role='user'):
  history.append({"role": "user", "content": text})
  output = llm.create_chat_completion(
    messages=history,
    max_tokens=512
  )
  response = output["choices"][0]["message"]["content"]
  history.append({"role": "assistant", "content": response})
  print(response)
  return response

def main():
  while True:
    print("テキストを入力してください。")
    text = input()
    if response.startswith("/quit"):
      print("終了します。")
      break

    response = chat_with_llama(text)



if __name__ == "__main__":
  main()
  exit(0)
