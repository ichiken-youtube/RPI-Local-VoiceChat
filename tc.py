
from llama_cpp import Llama
import settings

history = [{"role": "system", "content": settings.SYSTEM_PROMPT}]

def chat_with_llama(text,llm,role='user'):
  history.append({"role": "user", "content": text})
  output = llm.create_chat_completion(
    messages=history,
    max_tokens=1024
  )
  response = output["choices"][0]["message"]["content"]
  history.append({"role": "assistant", "content": response})
  print(response)
  return response

def main(model):
  while True:
    print("\nテキストを入力してください。")
    text = input()
    if text.startswith("/quit"):
      print("終了します。")
      break
    response = chat_with_llama(text,model)

if __name__ == "__main__":
  main(Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True))
  exit(0)
