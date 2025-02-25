from whisper_mic import WhisperMic
from llama_cpp import Llama
import settings
import os
import contextlib
import subprocess
import re
import time

llm = Llama(settings.MODEL_PATH, n_gpu_layers=settings.NGL, use_vulkan=True)
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

#https://nekonogorogoro.com/raspberrypi_openjtalk_python/
def speack_ojtalk(text, voice="f"):
  open_jtalk = ['open_jtalk']
  mecab_dict = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
  if voice == "f":
    # 女性音声
    htsvoice = ['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
  elif voice == "miku":
    #初音ミクボイス
    #https://karaage.hatenadiary.jp/entry/2016/07/22/073000
    htsvoice = ['-m','/usr/share/hts-voice/Miku/Miku-Type-b.htsvoice']
  else:
    # 男性音声
    htsvoice = ['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']

  # 音声スピード
  speed = ['-r','1.0']
  outwav = ['-ow','out.wav']
  cmd = open_jtalk+mecab_dict+htsvoice+speed+outwav
  c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
  c.stdin.write(text.encode('utf-8'))
  c.stdin.close()
  c.wait()
  aplay = ['aplay','-q','out.wav']
  process = subprocess.Popen(aplay)
  guruguru = ['/','-','\\']
  cnt = 0
  while process.poll() is None:
    print("\r発話中...%s"%guruguru[cnt%3],end='')
    time.sleep(1)
    cnt+=1


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
      speack_ojtalk("終了します。", voice=settings.VOICE)
      break
    response = chat_with_llama(text)
    for line in response.splitlines():
      speack_ojtalk(line, voice=settings.VOICE)
    print("\r発話中...完了")

if __name__ == "__main__":
  main()
