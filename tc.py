
from llama_cpp import Llama
import settings

llm=Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True, n_threads=4)

def chat_with_llama(text,history,role='user'):
  history.append({"role": role, "content": text})
  output = llm.create_chat_completion(
    messages=history,
    max_tokens=1024
  )
  response = output["choices"][0]["message"]["content"]
  history.append({"role": "assistant", "content": response})
  print(response)
  return response

def main():
  history = [{"role": "system", "content": settings.SYSTEM_PROMPT}]
  while True:
    print("\nテキストを入力してください。")
    text = input()
    if text.startswith("/quit"):
      print("終了します。")
      break
    response = chat_with_llama(text,history)

if __name__ == "__main__":
  main()
  exit(0)
