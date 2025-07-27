#!/usr/bin/env python3
"""
Test script for the improved PDF outline extractor
"""
import os
import json
from utils.extractor import extract_outline

def test_file01():
    """Test the extractor on file01.pdf"""
    input_file = "input/file01.pdf"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return
    
    print(f"Testing extractor on {input_file}")
    print("=" * 50)
    
    try:
        # Extract outline
        result = extract_outline(input_file)
        
        # Print results
        print(f"Title: {repr(result.get('title', ''))}")
        print(f"Outline length: {len(result.get('outline', []))}")
        
        if result.get('outline'):
            print("First few outline items:")
            for i, item in enumerate(result['outline'][:3]):
                print(f"  {i+1}. Level: {item.get('level')}, Text: {repr(item.get('text'))}, Page: {item.get('page')}")
        else:
            print("No outline items found")
        
        # Save to output directory
        output_file = "output/file01.json"
        os.makedirs("output", exist_ok=True)
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to {output_file}")
        
        # Check if it matches expected output
        expected_title = "Application form for grant of LTC advance"
        actual_title = result.get('title', '').strip()
        
        if expected_title in actual_title:
            print("✅ Title detection: PASSED")
        else:
            print(f"❌ Title detection: FAILED")
            print(f"   Expected: {repr(expected_title)}")
            print(f"   Got: {repr(actual_title)}")
        
        if len(result.get('outline', [])) == 0:
            print("✅ Outline filtering: PASSED (no form fields as headings)")
        else:
            print(f"❌ Outline filtering: FAILED (found {len(result['outline'])} headings)")
            print("   Form fields should not be treated as headings")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_file01() 