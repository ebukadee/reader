from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import os

poppler_path = "C:/Users/steezeless/Desktop/Release-24.08.0-0/poppler-24.08.0/Library/bin"

def pdf_to_jpeg_with_enhancements(pdf_path, output_dir):
    try:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, page in enumerate(pages, start=1):
        output_file = os.path.join(output_dir, f'page_{i}.jpg')

        enhanced_image = enhance_image(page)

        try:
            enhanced_image.save(output_file, 'JPEG', optimize=True, quality=40, progressive=True)
            print(f'Saved: {output_file}')
        except Exception as e:
            print(f"Error saving image: {e}")

def enhance_image(img, new_width=600):
    img = img.convert('RGB')

    # Resize while maintaining aspect ratio
    w_percent = new_width / float(img.width)
    new_height = int(float(img.height) * w_percent)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Enhance
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.3)

    return img

if __name__ == '__main__':
    pdf_path = "../books/Chapter 3_Energy Story_EEE 403.1.pdf"
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0].replace(" ", "_")  # Make it filename-safe
    image_output_dir = f"pages/{pdf_name}"

    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)

    pdf_to_jpeg_with_enhancements(pdf_path, image_output_dir)
