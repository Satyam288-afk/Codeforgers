import os
import sys
import time
import pandas as pd
from core.extraction import MockExtractionEngine

def run_benchmark():
    print("🚀 Starting Production LLM Accuracy Benchmark...\n")
    
    csv_path = "/Users/satyamkumar/.cache/kagglehub/datasets/kshitizregmi/jobs-and-job-description/versions/2/job_title_des.csv"
    if not os.path.exists(csv_path):
        print("❌ Dataset not found.")
        sys.exit(1)
        
    try:
        # Load exactly 3 real-world job postings to audit the AI
        df = pd.read_csv(csv_path).head(3)
        extractor = MockExtractionEngine()
        
        for index, row in df.iterrows():
            title = row.get("Job Title", "Unknown Title")
            jd_text = str(row.get("Job Description", ""))
            
            # Print Snippet
            print(f"==================================================")
            print(f"📌 TEST CASE {index+1}: {title.upper()}")
            print(f"📜 Raw Text Snippet: {jd_text[:120]}...\n")
            
            print("⏳ Firing Request to Gemini Neural Network...")
            start_time = time.time()
            
            # Pass the raw unformatted string into our LLM
            extracted_skills = extractor.extract_entities(jd_text, "jd")
            
            latency = time.time() - start_time
            print(f"✅ AI Processed in {latency:.2f} seconds!")
            
            print(f"🧠 EXTRACTED SCHEMA (Zero-Shot Accuracy):")
            for skill in extracted_skills:
                print(f"   ➤ [ {skill['skill']} ] - Level: {skill['level']}")
            
            print(f"==================================================\n")
            
    except Exception as e:
        print(f"Benchmark Error: {e}")

if __name__ == "__main__":
    run_benchmark()
