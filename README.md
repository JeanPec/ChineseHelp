# ChineseHelp

A French-to-Chinese translator with text-to-speech and pinyin generation. Translate French words to Simplified Chinese, hear the pronunciation, and see the pinyin romanization.

## Features

- **Translation**: French → Simplified Chinese using Ollama LLM
- **Text-to-Speech**: Chinese audio pronunciation using Piper TTS
- **Pinyin Generation**: Romanized pronunciation guides for Chinese characters
- **Auto-playback**: Audio plays automatically after generation

## Requirements

- Python 3.12+
- Ollama running locally (default: `http://localhost:11434`)
- Piper TTS model (Chinese): `zh_CN-huayan-medium.onnx`

## Installation

1. **Clone and setup**:

   ```bash
   git clone <repo>
   cd ChineseHelp
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download Piper model**:

   ```bash
   mkdir -p models
   cd models
   wget https://huggingface.co/rhasspy/piper-voices/resolve/main/zh_CN/zh_CN-huayan-medium.onnx
   cd ..
   ```

4. **Configure environment**:
   Create a `.env` file:

   ```
   PIPER_MODEL_PATH=models/zh_CN-huayan-medium.onnx
   model=qwen2.5:7b
   ```

5. **Start Ollama**:
   ```bash
   ollama serve
   # In another terminal:
   ollama pull qwen2.5:7b
   ```

## Usage

```bash
python3 app.py "Je bois du thé"
```

**Output**:

```
Translating: Je bois du thé...
Character: 我喝茶
Pinyin: wǒ hēchá
Audio generated: output.wav
[Audio plays automatically]
```

## How It Works

1. **Translate** - French input is sent to Ollama (LLM) for translation to Simplified Chinese
2. **Analyze** - Pinyin module generates romanized pronunciation
3. **Synthesize** - Piper TTS converts Chinese text to audio (WAV)
4. **Play** - Pygame mixer plays the audio automatically

## Architecture

```
French Input
    ↓
Ollama (LLM Translation)
    ↓
Piper (Text-to-Speech)
    ↓
Pygame (Audio Playback)
    ↓
Output (Character + Pinyin + Audio)
```

## Troubleshooting

- **No audio**: Ensure pygame is installed and speakers are enabled
- **Translation fails**: Check Ollama is running and model is downloaded
- **Model not found**: Verify `PIPER_MODEL_PATH` in `.env` is correct

## Dependencies

- `ollama` - LLM translation
- `piper-tts` - Text-to-speech synthesis
- `xpinyin` - Pinyin generation
- `pygame` - Audio playback
- `python-dotenv` - Environment configuration
