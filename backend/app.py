import os
import time
import shutil
import sys

# This tells Python to look in the project root so it can find the 'backend' folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import YOUR specific functions from your files
from backend.models.analyzer import analyzeImage
from backend.models.LLMBackend import get_fashion_advice

# 1. SETUP FOLDERS
WATCH_DIR = "data/uploads"
OUT_DIR = "data/processed"

# Create folders if they don't exist
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def run_ai_pipeline(file_path):
    filename = os.path.basename(file_path)
    print(f"\n📸 [NEW IMAGE]: {filename}")
    print("-" * 50)

    # 2. THE EYES: Run your partner's MediaPipe Analyzer
    print("👀 Analyzing body proportions...")
    results = analyzeImage(file_path)

    if results.get("error"):
        print(f"❌ ANALYZER ERROR: {results['error']}")
        return

    print(f"✅ Shape: {results['bodyShape']}")
    print(f"✅ Ratio: {results['ratio']}")

    # 3. THE BRAIN: Run your GitHub/Llama LLM
    print("🧠 Consulting the AI Stylist...")
    try:
        # This calls the function in your LLMBackend.py
        advice = get_fashion_advice(results)
        print("\n✨ [AI FASHION ADVICE]:")
        print(advice)
        print("-" * 50)
    except Exception as e:
        print(f"❌ LLM ERROR: {str(e)}")

    # 4. CLEANUP: Move to processed so it doesn't re-run
    dest_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(dest_path):
        os.remove(dest_path)
        
    shutil.move(file_path, dest_path)
    print(f"📁 Analysis complete. File moved to: {OUT_DIR}\n")

if __name__ == "__main__":
    print(f"🚀 CHUDS FASHION AI IS ACTIVE")
    print(f"📥 Drop images into: {os.path.abspath(WATCH_DIR)}")
    print("⌨️  Press Ctrl+C to stop.")

    try:
        while True:
            # Check for images every second
            files = [f for f in os.listdir(WATCH_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for f in files:
                full_path = os.path.join(WATCH_DIR, f)
                time.sleep(0.5) # Wait for file to finish copying/dropping
                run_ai_pipeline(full_path)
            
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n👋 App stopped. Good luck with the HackBU demo!")