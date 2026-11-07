import os
import json
import time
from pathlib import Path
import translators as ts

# =========================
# CONFIGURATION
# =========================

_ = ts.preaccelerate_and_speedtest()  # Optional. Caching sessions in advance, which can help improve access speed.

FOLDER_PATH = Path("input")
OUTPUT_DIR = Path("output")
SETTINGS_PATH = Path("settings.json")

# =========================
# LOAD SETTINGS
# =========================

while True:
    print("\n===== source language =====")
    print("1. English")
    print("2. Japanese")
    print("3. Korean")

    pilihan = input("insert 1/2/3: ")

    if pilihan == "1":
        source_language = "en"
        break

    elif pilihan == "2":
        source_language = "ja"
        break

    elif pilihan == "3":
        source_language = "ko"
        break

    else:
        print("invalid choice, please try again.")

LANGUAGES = {
    "en": "Inggris",
    "ja": "Jepang",
    "ko": "Korean",
    "id": "Indonesia"
}

if source_language not in LANGUAGES:
    raise ValueError("settings.json: language harus 'en', 'ja', 'ko' untuk mentranslate atau 'id' untuk menyunting naskah yang sudah ditranslate.")

# =========================
# TRANSLATION
# =========================

def translate_gratis(title, pt, text):
    """Kirim satu naskah ke Gemini dan kembalikan hasil JSON."""

    global source_language
    # if not text.strip():
    #     return {
    #         "translated_text": "",
    #         "note": ""
    #     }
    
    for attempt in range(1, 3):
        try:
            translated = ts.translate_text(text, translator='google', from_language=source_language, to_language='id')  # Optional. Using translators library for translation.
            return {
                "translated_text": translated,
                "note": ""
            }
        except Exception as exc:
            print(
                f"{title} pt {pt}: request gagal "
                f"(percobaan {attempt}/2): {exc}"
            )

            if attempt == 2:
                raise

            time.sleep(attempt * 3)
    
    return {
        "translated_text": translated + " failed",
        "note": "Terjadi kesalahan saat menerjemahkan."
    }

# =========================
# SAVE OUTPUT
# =========================

def save_texts_to_file(title, pt, result):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        OUTPUT_DIR /
        f"{title}_pt_{pt}.txt"
    )

    # Simpan hanya naskah terjemahan ke file TXT.
    output_file.write_text(
        result["translated_text"],
        encoding="utf-8"
    )

    # Simpan respons lengkap, termasuk note, sebagai JSON.
    json_file = output_file.with_suffix(".json")

    json_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"{title} pt {pt} saved to {output_file}")
    print(f"Response JSON saved to {json_file}")

    if result["note"]:
        print(f"Note: {result['note']}")

# =========================
# CHAPTER PROCESSING
# =========================

def do_translate(title, pt, text):
    print(f"\nTranslating {title} pt {pt}...")
    result = translate_gratis(title, pt, text)
    save_texts_to_file(title, pt, result)
    
    time.sleep(20)  # Delay to avoid rate limits or server overload

def main():
    global settings
    naskah = """"""
    
    print(f"Source language: {LANGUAGES[source_language]}")
    
    end_eng = ["\"", ".", "”"]
    end_jpn = ["︒", "。", "」", "﹂", ".", "…", "？"] # , "─", "﹄", "』"
    max_chars = 2500 if source_language == "ja" else 4000

    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".txt"):
            txt_path = os.path.join(FOLDER_PATH, filename)
    
            with open(txt_path, "r", encoding="utf-8") as file:
                pt = 1
                total = 0 
                for line in file:
                    if len(line) < 2:
                        continue
                        
                    # new
                    total += len(line)
                    naskah += line
        
                    if total >= max_chars:
                        if source_language == "ko" and line[-2] in end_eng:
                            print(f"\nReached max input chars ({total}). translating...")
                            do_translate(filename, pt, naskah)
                            naskah = """"""
                            total = 0
                            pt += 1 
                            
                        if source_language == "ja" and line[-2] in end_jpn:
                            print(f"\nReached max input chars ({total}). translating...")
                            do_translate(filename, pt, naskah)
                            naskah = """"""
                            total = 0
                            pt += 1 
                            
                        elif source_language == "en" and line[-2] in end_eng:
                            print(f"\nReached max input chars ({total}). translating...")
                            do_translate(filename, pt, naskah)
                            naskah = """"""
                            total = 0
                            pt += 1
                            
                print(f"\nReached max input chars ({total}). translating...")
                do_translate(filename, pt, naskah)
                naskah = """"""
                total = 0
                pt += 1 
            
    
            print(f"Nama file: {filename}")
            
            print("=" * 50)
        else:
            print(f"txt file not detected")
            
    print("\nSemua chapter selesai diproses.")


if __name__ == "__main__":
    main()
