import os
import wave
from dotenv import load_dotenv
from piper import PiperVoice
from xpinyin import Pinyin
import ollama
import pygame

load_dotenv()

# Configuration - You can use os.environ to keep these out of your code
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Get the relative path from the .env file (e.g., "models/zh_CN-huayan-medium.onnx")
MODEL_RELATIVE_PATH = os.getenv("PIPER_MODEL_PATH")

# 3. Join them together
MODEL_PATH = os.path.join(BASE_DIR, MODEL_RELATIVE_PATH)
MODEL_NAME = os.getenv("model", "qwen2.5:7b")

# Initialize
p = Pinyin()
voice = PiperVoice.load(MODEL_PATH)

def generate_audio(chinese_text, output_file):
    output_file = "output.wav"
    
    # Open the wave file with the required settings
    # Piper models usually default to 22050Hz, 1 channel, 16-bit
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050) # Use the sample rate expected by your model
        
        # This will write the header and the audio data correctly
        voice.synthesize_wav(chinese_text, wav_file)
        
    print(f"Audio generated: {output_file}")

def play_audio(output_file):
    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pass

def run(french_word):
    print(f"Translating: {french_word}...")
    
    # 1. Translate
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'user', 'content': f'Translate "{french_word}" to Simplified Chinese. Only output the characters.'}
    ])
    chinese = response['message']['content'].strip()
    
    # 2. Pinyin
    pinyin_result = p.get_pinyin(chinese, tone_marks='marks')
    
    print(f"Character: {chinese}")
    print(f"Pinyin: {pinyin_result}")
    
    generate_audio(chinese, "output.wav")
    play_audio("output.wav")

if __name__ == "__main__":
    import sys
    word = sys.argv[1] if len(sys.argv) > 1 else "pomme"
    run(word)