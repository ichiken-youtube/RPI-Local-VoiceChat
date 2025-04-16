# RPI-Local-VoiceChat
## Setup
venvで仮想環境を作るのが良いかもしれません。  
```bash
sudo apt install portaudio19-dev
pip install whisper-mic
CMAKE_ARGS="-DLLAMA_VULKAN=on" pip install llama-cpp-python
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

#これが有効だとスマートホームモードになる
SMART_HOME=False
```