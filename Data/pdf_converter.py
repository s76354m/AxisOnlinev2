import PyPDF2
import os
from pathlib import Path

def pdf_to_text(pdf_path, output_path=None):
    """
    Convert PDF to text file
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path for output text file. 
                                   If None, uses same name as PDF with .txt extension
    
    Returns:
        str: Path to the output text file
    """
    try:
        # Create output path if not provided
        if output_path is None:
            output_path = str(Path(pdf_path).with_suffix('.txt'))
            
        # Open PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n\n'
            
            # Write text to output file
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
                
        print(f"Successfully converted {pdf_path} to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return None

if __name__ == "__main__":
    # Use absolute path
    pdf_file = Path(r"C:\Users\xbows\OneDrive\Desktop\Dad\SwarmV2\Data\Axis Program Management_Unformatted detailed.pdf")
    
    # Verify if file exists before converting
    if not pdf_file.exists():
        print(f"Error: File not found at {pdf_file}")
    else:
        # Convert PDF to text
        output_file = pdf_to_text(str(pdf_file))