from whisper_mic import WhisperMic
from llama_cpp import Llama
import settings
from error_hider import noalsaerr
import os
import sys
import contextlib

llm = Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True)
with contextlib.redirect_stdout(open(os.devnull, 'w')):
  mic = WhisperMic(model="medium")
history = [{"role": "system", "content": "You are helpful assistant."}]

@contextlib.contextmanager
def suppress_output():
  # os.devnullをファイルディスクリプタとして開く
  devnull_fd = os.open(os.devnull, os.O_WRONLY)
  
  # 標準出力と標準エラーをos.devnullにリダイレクト
  old_stdout_fd = sys.stdout.fileno()
  old_stderr_fd = sys.stderr.fileno()
  
  os.dup2(devnull_fd, old_stdout_fd)
  os.dup2(devnull_fd, old_stderr_fd)
  
  try:
    # リダイレクトされた状態で処理を実行
    yield
  finally:
    # リダイレクトを元に戻す
    os.dup2(old_stdout_fd, sys.stdout.fileno())
    os.dup2(old_stderr_fd, sys.stderr.fileno())
    os.close(devnull_fd)

def transcribe_audio():
  print("話してください...")
  #with suppress_stdout(): #noalsaerr():
  with suppress_output():
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
