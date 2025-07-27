import os
import json
import sys
from utils.extractor import extract_outline

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    """Main function to process all PDFs in input directory"""
    try:
        # Ensure input and output directories exist
        if not os.path.exists(INPUT_DIR):
            print(f"Input directory {INPUT_DIR} does not exist")
            sys.exit(1)
            
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Get list of PDF files
        pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in input directory")
            return
        
        print(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF file
        for filename in pdf_files:
            try:
                in_path = os.path.join(INPUT_DIR, filename)
                out_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
                
                print(f"Processing: {filename}")
                
                # Extract outline
                outline_data = extract_outline(in_path)
                
                # Validate output
                if not isinstance(outline_data, dict):
                    print(f"Warning: Invalid output format for {filename}")
                    outline_data = {"title": "", "outline": []}
                
                if "title" not in outline_data or "outline" not in outline_data:
                    print(f"Warning: Missing required fields in output for {filename}")
                    outline_data = {"title": "", "outline": []}
                
                # Write output
                with open(out_path, "w", encoding='utf-8') as f:
                    json.dump(outline_data, f, indent=2, ensure_ascii=False)
                
                print(f"Completed: {filename} -> {len(outline_data.get('outline', []))} headings extracted")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                # Create empty output file to prevent crashes
                out_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
                with open(out_path, "w", encoding='utf-8') as f:
                    json.dump({"title": "", "outline": []}, f, indent=2)
        
        print("Processing completed successfully")
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
