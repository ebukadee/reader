from pdf2image import convert_from_path
from PIL import Image
import os

poppler_path = "C:/Users/steezeless/Desktop/Release-24.08.0-0/poppler-24.08.0/Library/bin"

def split_pdf_pages(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return

    page_number = 1  # Start numbering from page 1

    for page in pages:
        width, height = page.size

        if width > height:  # Only split landscape pages
            # Split into left and right halves
            left_half = page.crop((0, 0, width // 2, height))
            right_half = page.crop((width // 2, 0, width, height))

            # Save left half as current page number
            left_half_path = os.path.join(output_folder, f"page{page_number}.jpg")
            left_half.save(left_half_path)
            print(f"Saved: {left_half_path}")

            # Increment and save right half as next page
            page_number += 1
            right_half_path = os.path.join(output_folder, f"page{page_number}.jpg")
            right_half.save(right_half_path)
            print(f"Saved: {right_half_path}")

            # Increment for the next PDF page
            page_number += 1

        else:  # Keep portrait pages unchanged
            output_path = os.path.join(output_folder, f"page{page_number}.jpg")
            page.save(output_path)
            print(f"Saved: {output_path}")
            page_number += 1

input_folder = "C:/Users/steezeless/Desktop/books/EEE405.1 DR OGBONNA MATERIAL .pdf"  # Replace with your folder path
output_folder = "C:/Users/steezeless/Desktop/oblee"
split_pdf_pages(input_folder, output_folder)
