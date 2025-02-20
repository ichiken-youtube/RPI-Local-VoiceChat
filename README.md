# RPI-Local-VoiceChat
## Setup
```bash
pip install git+https://github.com/openai/whisper.git
CMAKE_ARGS="-DLLAMA_VULKAN=on" python3 -m pip install --no-cache-dir --upgrade --force-reinstall --verbose llama-cpp-python
```