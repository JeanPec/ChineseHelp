```python?code_reference&code_event_index=1
markdown_content = """# Project: French-to-Chinese AI Voice Assistant

This document provides the context, architecture, and requirements for building an AI-powered voice translation device.

## Overview
The goal is to build a standalone hardware device that captures French voice input, translates it to Simplified Chinese, displays the characters and Pinyin, and speaks the Chinese translation aloud.

## System Architecture
The system uses a **Client-Server architecture** to balance processing power:
- **Server (Desktop):** Runs `Ollama` (LLM) for high-speed translation.
- **Client (Raspberry Pi):** Runs `Piper` (TTS), handles Microphone input, and manages the GUI (Screen).



## Software Stack
### 1. Requirements (`requirements.txt`)
```

````text?code_stdout&code_event_index=1
File generated successfully.

```text
ollama
xpinyin
piper-tts
python-dotenv
speech_recognition
PyAudio
````

### 2. Software Logic

- **Audio Capture:** `speech_recognition` package for listening.
- **LLM Interaction:** `ollama` Python client to translate French to Chinese.
- **Text Processing:** `xpinyin` to generate Pinyin.
- **TTS Engine:** `piper-tts` (using `PiperVoice.synthesize_wav`) to generate audio from text.
- **GUI:** `Tkinter` (or a web-based Flask/FastAPI interface) to display text/Pinyin.

## Hardware Requirements

| Component        | Purpose         | Specification                       |
| :--------------- | :-------------- | :---------------------------------- |
| **Raspberry Pi** | Main Processing | Pi 4 (4GB+) or Pi 5                 |
| **Microphone**   | Audio Input     | USB Mic or I2S Microphone HAT       |
| **Display**      | UI Output       | 5" or 7" HDMI Touchscreen           |
| **Speaker**      | Audio Output    | 3.5mm jack speaker or USB/Bluetooth |
| **Power**        | Stability       | Official Raspberry Pi Power Supply  |

## Development Steps

### Phase 1: Software Development (Desktop)

1. Set up `.env` with `PIPER_MODEL_PATH` (relative to project root).
2. Develop `app.py` using `PiperVoice` native API (not CLI `exec`).
3. Ensure `zh_CN-huayan-medium.onnx` and `zh_CN-huayan-medium.onnx.json` are in the `models/` directory.

### Phase 2: Hardware Setup (Raspberry Pi)

1. Install Raspberry Pi OS (Bookworm).
2. Install system-level dependencies (`apt install python3-pyaudio espeak-ng`).
3. Clone project and install `pip` dependencies.
4. Configure Kiosk mode for the touchscreen display.

### Phase 3: Integration

1. Configure `API_URL` in `.env` to point to the Desktop's local network IP.
2. Ensure Ollama is configured to listen on the local network (set `OLLAMA_HOST=0.0.0.0`).
3. Connect Microphone and Speaker; test audio output with a standard wave file.
   """

with open("project_context.md", "w") as f:
f.write(markdown_content)
print("File generated successfully.")

```
Your project context file is ready. You can now copy this file content into any LLM to quickly get them up to speed on your project architecture, requirements, and hardware needs.

[file-tag: code-generated-file-0-1777935016567881639]

The context document includes:
* **System Architecture:** A high-level overview of how the Desktop (Ollama) and Raspberry Pi (Piper) interact.
* **Software Stack:** A clean list of dependencies and the logic flow.
* **Hardware Requirements:** A table covering the specific hardware parts you'll need to purchase.
* **Development Phases:** A step-by-step roadmap from software prototyping to physical device integration.

Good luck with your Raspberry Pi build! This is a great way to combine software engineering with hardware tinkering.
```
