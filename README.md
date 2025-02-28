# RPI-Local-VoiceChat
## Setup
venvで仮想環境を作るのが良いかもしれません。  
```bash
sudo apt install portaudio19-dev
pip install whisper-mic
CMAKE_ARGS="-DLLAMA_VULKAN=on" pip install llama-cpp-python
```