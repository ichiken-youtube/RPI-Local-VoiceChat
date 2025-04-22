# RPI-Local-VoiceChat
## ボイスチャット
LLMと音声会話をするためのプログラムです。  
マイク入力された音声の文字起こしにはWhisper-mic、音声合成にはOpenJTalk、音声の再生にはaplayを使用しています。
### セットアップ
venvで仮想環境を作るのが良いかもしれません。  
後ほどGPIOを使用するため、```--system-site-packages```オプションが必要です。
```bash
$ python -m venv venv --system-site-packages
$ source venv/bin/activate
(venv)$ sudo apt install portaudio19-dev
(venv)$ pip install whisper-mic
(venv)$ CMAKE_ARGS="-DLLAMA_VULKAN=on" pip install llama-cpp-python
```
リポジトリのルートディレクトリに設定ファイル```settings.py```を作成して、以下の内容を書き込んでください。
```Python
#gguf形式モデルのファイルの場所(相対パス可)
MODEL_PATH="./models/hogehoge.gguf"

#nglオプションに渡す数値。GPUに展開するレイヤ数
NGL=41

#システムプロンプト
SYSTEM_PROMPT="あなたは好きな惣菜発表AIです。発言の後に、必ずランダムな惣菜の名前を言います。例えば肉じゃがなどです。"

#f:女性声 m:男性声
VOICE="f"

#これが有効だとスマートホームモードになる。その場合、システムプロンプトは無効になる
SMART_HOME=False
```

## スマートホームアシスタント
本プログラムでは、家電(照明)に見立てたLEDをRaspberry PiのGPIOに接続し、音声操作によってそれらを制御します。  
LEDは2つ制御することができ、それぞれ「1階」、「2階」と呼称します。
### セットアップ
settings.pyに、```SMART_HOME=True```の設定を書き込んでください。  
LEDをそれぞれGPIO20,21に接続してください。
## 実行
```bash
(venv)$ python vc.py
```