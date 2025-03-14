from pdf2image import convert_from_path
from PIL import Image
import os

poppler_path = "C:/Users/steezeless/Desktop/Release-24.08.0-0/poppler-24.08.0/Library/bin"

def split_pdf_pages(pdf_path, output_folder, max_width, max_height, quality=90):
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

            # Resize left half
            left_half.thumbnail((max_width, max_height), Image.LANCZOS)
            left_half_path = os.path.join(output_folder, f"page{page_number}.jpg")
            left_half.save(left_half_path, 'JPEG', optimize=True, quality=quality, progressive=True)
            print(f"Saved: {left_half_path}")

            # Increment and resize right half
            page_number += 1
            right_half.thumbnail((max_width, max_height), Image.LANCZOS)
            right_half_path = os.path.join(output_folder, f"page{page_number}.jpg")
            right_half.save(right_half_path, 'JPEG', optimize=True, quality=quality, progressive=True)
            print(f"Saved: {right_half_path}")

            # Increment for the next PDF page
            page_number += 1

        else:  # Keep portrait pages unchanged
            page.thumbnail((max_width, max_height), Image.LANCZOS)
            output_path = os.path.join(output_folder, f"page{page_number}.jpg")
            page.save(output_path, 'JPEG', optimize=True, quality=quality, progressive=True)
            print(f"Saved: {output_path}")
            page_number += 1

input_folder = "C:/Users/steezeless/Desktop/books/EEE 404.1 DR OGBONNA MATERIAL .pdf"  # Replace with your folder path
output_folder = "C:/Users/steezeless/Desktop/oblee"
max_width = 600  # Replace with your desired max width
max_height = 800  # Replace with your desired max height
split_pdf_pages(input_folder, output_folder, max_width, max_height)