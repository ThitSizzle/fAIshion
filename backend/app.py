import os
import time
import shutil
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.models.analyzer import analyzeImage
from backend.models.LLMBackend import get_fashion_advice

WATCH_DIR = "data/uploads"
OUT_DIR = "data/processed"

os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def run_ai_pipeline(file_path, gender):
    filename = os.path.basename(file_path)
    print(f"\n [NEW IMAGE]: {filename} (Mode: {gender})")
    
    results = analyzeImage(file_path)
    
    if results.get("error"):
        print(f" Error: {results['error']}")
    else:
        try:
            advice = get_fashion_advice(results, gender=gender)
            print(f"\n✨ [AI {gender.upper()} FASHION ADVICE]:")
            print(advice)
        except Exception as e:
            print(f" LLM ERROR: {e}")

    dest_path = os.path.join(OUT_DIR, filename)
    try:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(file_path, dest_path)
        print(f" Analysis complete. {filename} moved to processed folder.")
        print("-" * 50)
    except Exception as e:
        print(f" CLEANUP ERROR: {e}")

if __name__ == "__main__":
    print(f" fAIshion loading ...")
    
    selected_gender = input("\nEnter target gender for styling (male/female/unisex): ").strip().lower()
    print(f"\n Watching {os.path.abspath(WATCH_DIR)} for {selected_gender} fashion...")

    try:
        while True:
            files = [f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for f in files:
                full_path = os.path.join(WATCH_DIR, f)
                time.sleep(1) 
                run_ai_pipeline(full_path, selected_gender)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 App stopped. Good luck with the HackBU demo!")