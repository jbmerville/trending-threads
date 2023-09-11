# Clé API: AIzaSyCRiXARDTHf7AzujKIRNo4uEQlEswhD34Y

# Importing necessary libraries
import requests
import os

def translate_text(text, target_language):
    """
    Translates the given text into the target language using Google Translate API.
    """
    url = "https://translation.googleapis.com/language/translate/v2"
    api_key = "AIzaSyCRiXARDTHf7AzujKIRNo4uEQlEswhD34Y"
    data = {
        "q": text,
        "target": target_language,
        "key": api_key
    }
    response = requests.post(url, data=data)
    translated_text = response.json()["data"]["translations"][0]["translatedText"]
    return translated_text

def get_language_code(language_name):
    """
    Maps common language names to their respective codes.
    """
    # A simple mapping of language names to codes. Extend this as needed.
    language_map = {
        "spanish": "es",
        "french": "fr",
        "german": "de",
        # ... add more mappings as needed
    }
    return language_map.get(language_name.lower(), language_name)

def main():
    """
    Main function to read from a file, translate its content, and print the translated text.
    """
    base_directory = "C:\\Users\\Toune\\iCloudDrive\\Documents\\Code\\Thread"
    file_name = input("Enter the name of the text file (e.g., 'sample.txt'): ")
    full_path = os.path.join(base_directory, file_name)
    
    # Check if file exists
    if not os.path.exists(full_path):
        print(f"Error: File '{file_name}' not found in the directory '{base_directory}'.")
        return

    target_language = input("Enter the target language or its code (e.g., 'Spanish' or 'es'): ")
    target_language_code = get_language_code(target_language)

    with open(full_path, 'r') as file:
        content = file.read()

    translated_content = translate_text(content, target_language_code)
    print("\nTranslated Content:\n")
    print(translated_content)

if __name__ == "__main__":
    main()
