from whisper_mic import WhisperMic
from llama_cpp import Llama
import settings
import os
import sys
import contextlib

llm = Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True)
with contextlib.redirect_stdout(open(os.devnull, 'w')):
  mic = WhisperMic(model="medium")
history = [{"role": "system", "content": "You are helpful assistant."}]

@contextlib.contextmanager
def suppress_output():
  # /dev/nullをファイルディスクリプタとして開く
  null_fd = os.open(os.devnull, os.O_RDWR)
    
  # 現在の標準出力と標準エラー出力のファイルディスクリプタを保存
  save_stdout_fd = os.dup(1)  # 1は標準出力
  save_stderr_fd = os.dup(2)  # 2は標準エラー出力
    
  # 標準出力と標準エラー出力を/dev/nullにリダイレクト
  os.dup2(null_fd, 1)  # 標準出力を/dev/nullにリダイレクト
  os.dup2(null_fd, 2)  # 標準エラー出力を/dev/nullにリダイレクト
  
  try:
    # リダイレクトされた状態で処理を実行
    yield
  finally:
    # 標準出力と標準エラー出力を元に戻す
    os.dup2(save_stdout_fd, 1)
    os.dup2(save_stderr_fd, 2)
    
    # 使用したファイルディスクリプタを閉じる
    os.close(null_fd)
    os.close(save_stdout_fd)
    os.close(save_stderr_fd)

def transcribe_audio():
  print("\n\n話してください...")
  #with suppress_stdout(): #noalsaerr():
  with suppress_output():
    print("これは表示されないはず")
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
