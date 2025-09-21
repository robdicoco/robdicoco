#!/usr/bin/env python3
"""
Script to extract text content from ProfileA.pdf and save as JSON
"""

import json
import sys
import os

def extract_pdf_content(pdf_path):
    """Extract text content from PDF file"""
    try:
        import pypdf
        
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            text_content = ""
            
            # Extract text from all pages
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text_content += f"--- Page {page_num + 1} ---\n"
                text_content += page_text + "\n\n"
            
            return {
                "filename": os.path.basename(pdf_path),
                "total_pages": len(reader.pages),
                "content": text_content.strip(),
                "extraction_status": "success"
            }
            
    except ImportError:
        return {
            "filename": os.path.basename(pdf_path),
            "error": "PyPDF library not installed",
            "extraction_status": "failed"
        }
    except Exception as e:
        return {
            "filename": os.path.basename(pdf_path),
            "error": str(e),
            "extraction_status": "failed"
        }

def main():
    pdf_file = "ProfileA.pdf"
    output_file = "profile_content.json"
    
    if not os.path.exists(pdf_file):
        print(f"Error: {pdf_file} not found")
        sys.exit(1)
    
    print(f"Extracting content from {pdf_file}...")
    
    # Extract content
    result = extract_pdf_content(pdf_file)
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    if result["extraction_status"] == "success":
        print(f"✅ Successfully extracted content from {pdf_file}")
        print(f"📄 Total pages: {result['total_pages']}")
        print(f"💾 Content saved to: {output_file}")
        
        # Show preview of content
        content_preview = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
        print(f"\n📋 Content preview:\n{content_preview}")
    else:
        print(f"❌ Failed to extract content: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
