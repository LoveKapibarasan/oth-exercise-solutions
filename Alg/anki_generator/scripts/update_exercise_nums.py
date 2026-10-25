import os
import json

def update_sheets():
    json_dir = r"C:\Users\lovek\Documents\EX\Alg\anki_generator\json_cards"
    
    mapping = {
        "ex01.json": ["Exercise 1.1", "Exercise 1.2", "Exercise 1.3"],
        "ex02.json": ["Exercise 2.1", "Exercise 2.2", "Exercise 2.3"],
        "ex03.json": ["Exercise 3.1 a)", "Exercise 3.1 b)", "Exercise 3.2"],
        "ex04.json": ["Exercise 4.2", "Exercise 4.3", "Exercise 4.4"],
        "ex05.json": ["Exercise 5.1", "Exercise 5.2", "Exercise 5.3"],
        "ex06.json": ["Exercise 6.1 (Algorithm)", "Exercise 6.1 (Proof)"],
        "ex07.json": ["Exercise 7.1 (Concept)", "Exercise 7.1 (Implementation)", "Exercise 7.1 (Depth)"],
        "ex08.json": ["Exercise 8.1 a) (Bitboard)", "Exercise 8.1 b) (Negamax AB)", "Exercise 8.1 a) (Win Check)"],
        "ex09.json": ["Exercise 9.1", "Exercise 9.2", "Exercise 9.3 (Modulo 8)", "Exercise 9.3 (Threat Detection)"],
        "ex10.json": ["Exercise 10.1 a)", "Exercise 10.1 b) (Properties)", "Exercise 10.1 b) (Fail-High)", "Exercise 10.1 e)"],
        "ex11.json": ["Exercise 11.1 a)", "Exercise 11.1 b) (Bitfields)", "Exercise 11.1 b) (Pruning)", "Exercise 11.1 d)"],
        "ex12.json": ["Exercise 12.1", "Exercise 12.2 & 12.3", "Exercise 12.4", "Exercise 12.5 & 12.6"],
        "ex13.json": ["Exercise 13.1", "Exercise 13.2", "Exercise 13.3 (Group size identity)", "Exercise 13.3 (Fermat's Little Theorem)"],
        "ex14.json": ["Exercise 14.1", "Exercise 14.2", "Exercise 14.4"],
        "ex15.json": ["Exercise 15.1", "Exercise 15.2", "Exercise 15.3 a)", "Exercise 15.3 b)"]
    }
    
    for filename, new_sheets in mapping.items():
        filepath = os.path.join(json_dir, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename}: not found")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            cards = json.load(f)
            
        if len(cards) != len(new_sheets):
            print(f"Warning: size mismatch for {filename} ({len(cards)} cards, {len(new_sheets)} labels)")
            
        for i in range(min(len(cards), len(new_sheets))):
            cards[i]["sheet"] = new_sheets[i]
            
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
            
        print(f"Updated {filename}")

if __name__ == "__main__":
    update_sheets()
