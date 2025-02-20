# RPI-Local-VoiceChat
## Setup
```bash
sudo apt install portaudio19-dev
pip install whisper-mic
CMAKE_ARGS="-DLLAMA_VULKAN=on" python3 -m pip install --no-cache-dir --upgrade --force-reinstall --verbose llama-cpp-python
```