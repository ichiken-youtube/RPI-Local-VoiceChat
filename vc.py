from whisper_mic import WhisperMic
from llama_cpp import Llama
import settings
import os
import contextlib
import subprocess
import re
import time
import gpiozero
import tc

mic = WhisperMic(model="small")
history = [{"role": "system", "content": "あなたはRaspberry Piの上で動作してるスマートホームアシスタントです。\
あなたはGPIOを制御することができます。ユーザから要求があった場合は、制御を実行します。\
コマンドを生成することで、GPIOが制御されます。コマンドは以下の構文です。\
/GPIO \{出力番号\} \{状態\}\
「出力A」が出力番号0、「出力B」が出力番号1に対応しています。\
音声認識の都合上、文字が誤認される場合がありますが、コマンドを解釈するうえで読みが似ている場合、また、意味が近い語は同一と解釈してください。\
状態は0,1のみ入力可能です。0がオフ、1がオンです。\
操作をする場合は、コマンドのみを生成して他の文は生成しないでください。\
実行が完了したのち、システムから返ってくるメッセージの内容を判断して、成功/不成功を日本語の文章として報告してください。"}]

pin_outA = gpiozero.DigitalOutputDevice(pin=20)
pin_outB = gpiozero.DigitalOutputDevice(pin=21)

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
  if text == "": 
    return
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

def command_parser(command):
  args=command.split(' ', 3)[:3]
  print(args)
  if args[0]=="/GPIO":
    if args[1]=="0":
      if args[2]=="0":
        pin_outA.off()
        print("info:出力Aをオフにしました。")
        return "info:出力Aをオフにしました。"
      elif args[2]=="1":
        pin_outA.on()
        print("info:出力Aをオンにしました。")
        return "info:出力Aをオンにしました。"
      else:
        return "error:状態指定に不正があります。0,1以外の状態を指定してください。"
    elif args[1]=="1":
      if args[2]=="0":
        pin_outB.off()
        return "info:出力Bをオフにしました。"
      elif args[2]=="1":
        pin_outB.on()
        return "info:出力Bをオンにしました。"
      else:
        return "error:状態指定に不正があります。0,1以外の状態を指定してください。"
    else:
      return "error:GPIOポート指定が不正です。"
  else:
    return "error:コマンドが不正です。"
  

def transcribe_audio():
  print("\n\n話してください...")
  #with suppress_stdout(): #noalsaerr():
  with suppress_output():
    print("これは表示されないはず")
    result = mic.listen()

  print(">>>", result)
  return result

def main():
  while True:
    text = transcribe_audio()
    if any(word in text.lower() for word in ["exit", "quit", "終了","赤い魔法"]):
      print("終了します。")
      break
    
    response = tc.chat_with_llama(text,history)

    for line  in response.splitlines():
      if line.startswith("/GPIO"):
        result=command_parser(line)
        response = tc.chat_with_llama(result,history,role="system")
        break

    for line in re.split('[。\n]', response):
      if line != "":
        speack_ojtalk(line, voice=settings.VOICE)
    print("\r発話中...完了")

if __name__ == "__main__":
  main()
  exit(0)
