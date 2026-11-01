import os
import json
import time
from pathlib import Path
import argparse


# =========================
# CONFIGURATION
# =========================

INPUT_PATH = Path("input2.txt")
OUTPUT_DIR = Path("output")

parser = argparse.ArgumentParser()
parser.add_argument("-l", default="eng", required=False)
args = parser.parse_args()
lang = args.l

# =========================
# SAVE OUTPUT
# =========================

def save_texts_to_file(chapter, result):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        OUTPUT_DIR /
        f"chapter_{chapter}.txt"
    )

    output_file.write_text(
        result,
        encoding="utf-8"
    )
    
    return


# =========================
# CHAPTER PROCESSING
# =========================

def main():
    jp_start = "第"
    jp_end = "話"
    start_chapter = 0
    chapter_naskah = """"""
    get_naskah = True

    with INPUT_PATH.open("r", encoding="utf-8-sig") as file:
        for line in file:
            if lang == "eng" and f"chapter {start_chapter}" in line[:10].lower().rstrip():
              get_naskah = True

            elif lang == "jp" and line[0] == jp_start and jp_end in line:
              get_naskah = True
              

            if lang == "eng" and f"chapter {start_chapter + 1}" in line[:10].lower().rstrip():
              save_texts_to_file(
                  start_chapter,
                  chapter_naskah
              )
              start_chapter += 1
              chapter_naskah = """"""

            elif lang == "jp" and line[0] == jp_start and jp_end in line:
              save_texts_to_file(
                  start_chapter,
                  chapter_naskah
              )
              start_chapter += 1
              chapter_naskah = """"""
              
            if line != "\n" and get_naskah:
              chapter_naskah += line

        save_texts_to_file(
            start_chapter,
            chapter_naskah
        )

    print("\nSemua chapter selesai diproses.")


if __name__ == "__main__":
    try:
        main()
    finally:
        print("Gemini client closed.")
