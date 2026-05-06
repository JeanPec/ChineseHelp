import os
import wave
from dotenv import load_dotenv
from piper import PiperVoice
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from xpinyin import Pinyin
import ollama
import pygame

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPER_MODEL_PATH = os.path.join(BASE_DIR, os.getenv("PIPER_MODEL_PATH"))
NLLB_MODEL_PATH = os.path.join(BASE_DIR, os.getenv("NLLB_MODEL_PATH"))
LLM_MODEL_NAME = os.getenv("model", "qwen2.5:7b")

# Initialize
p = Pinyin()
voice = PiperVoice.load(PIPER_MODEL_PATH)

# Load NLLB Locally
print("Loading translation model...")
tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL_PATH, attn_implementation="sdpa", device_map="auto")

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

def translate_to_chinese(french_word):
    response = ollama.chat(model=LLM_MODEL_NAME, messages=[
        {'role': 'user', 'content': f'Translate "{french_word}" to Simplified Chinese. Only output the characters.'}
    ])
    return response['message']['content'].strip()

def translate_to_chinese_nllb(french_word):
    # 1. Force the source language
    #tokenizer.src_lang = "fra_Latn"
    
    inputs = tokenizer(french_word, return_tensors="pt").to(model.device)
    
    # 2. Use Beam Search (num_beams)
    # This forces the model to look at 5 possible sentences and pick the best one.
    # It prevents it from "tripping" on the first character.

    translated_tokens = model.generate(
        **inputs, 
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("zho_Hans"),
        max_new_tokens=50,
        num_beams=5,          # Checks 5 different versions of the sentence
        repetition_penalty=1.5, # Stops it from repeating single characters
        length_penalty=1.2,    # Gives a slight "bonus" to longer, more accurate words
        no_repeat_ngram_size=2 # Prevents it from getting stuck in a loop
    )
    
    result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return result

def translate_to_chinese_test(english_text):
    inputs = tokenizer(english_text, return_tensors="pt", padding=True)
    
    translated_tokens = model.generate(
        **inputs,
        max_new_tokens=50,
        num_beams=5
    )
    
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

def run(french_word):
    print(f"Translating: {french_word}...")
    
    # 1. Translate to Chinese
    chinese = translate_to_chinese(french_word)
    
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