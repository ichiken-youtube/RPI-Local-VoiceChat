import subprocess

def speack_ojtalk(text, voice="f"):
  open_jtalk = ['open_jtalk']
  mecab_dict = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
  if voice == "f":
    # 女性音声
    htsvoice = ['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
  else:
    # 男性音声
    htsvoice = ['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
  # 音声スピード
  speed = ['-r','1.0']
  outwav = ['-ow','test.wav']
  cmd = open_jtalk+mecab_dict+htsvoice+speed+outwav
  c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
  c.stdin.write(text.encode('utf-8'))
  c.stdin.close()
  c.wait()
  aplay = ['aplay','-q','test.wav']#,'-Dhw:0,0']
  wr = subprocess.Popen(aplay)


def main():
  # 読み上げてほしい文章を入力
  text = "隣の客はよく柿食う客だ"
  # voice=に男性か女性の音声を指定する
  speack_ojtalk(text, voice="f")


if __name__ == '__main__':
  main()
