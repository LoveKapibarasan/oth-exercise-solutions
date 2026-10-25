import os
import json

def validate():
    json_dir = "C:\\Users\\lovek\\Documents\\EX\\Alg\\anki_generator\\json_cards"
    for file in sorted(os.listdir(json_dir)):
        if file.endswith(".json"):
            file_path = os.path.join(json_dir, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json.load(f)
                print(f"VALID: {file}")
            except Exception as e:
                print(f"INVALID: {file} - {e}")

if __name__ == "__main__":
    validate()
