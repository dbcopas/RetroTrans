import argparse
import os
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
from googletrans import Translator
import glob

# Initialize the translator
translator = Translator()

def translate_text_to_english(text):
    # Translate text to English
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

def process_xml_file(file_path):
    # Open and read the XML file
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    soup = BeautifulSoup(xml_data, 'xml')

    for game in soup.find_all('game'):
        print (f"Processing game: {game.find('name').text}")
        desc = game.find('desc')
        if desc and desc.text:
            try:
                lang = detect(desc.text)
                if lang != 'en':
                    print (f"Detected non-English text: '{desc.text}'")
                    translated_text = translate_text_to_english(desc.text)
                    if translated_text:
                        desc.string.replace_with(translated_text)
                        print(f"Translated to '{translated_text}'")
            except LangDetectException:
                print("Language detection failed, skipping.")
    
    # Save the modified XML back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def find_and_process_xml_files(root_dir):
    # Recursively search for XML files and process them
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                process_xml_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate non-English 'desc' properties of XML files to English.")
    parser.add_argument("root_dir", help="Root directory to search for XML files.")
    
    args = parser.parse_args()
    
    find_and_process_xml_files(args.root_dir)
