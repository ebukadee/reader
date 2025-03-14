from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import os

poppler_path = "C:/Users/steezeless/Desktop/Release-24.08.0-0/poppler-24.08.0/Library/bin"

def pdf_to_jpeg_with_enhancements(pdf_path, output_dir):
    try:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"Error converting PDF {pdf_path}: {e}")
        return None

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, page in enumerate(pages, start=1):
        output_file = os.path.join(output_dir, f'page_{i}.jpg')
        enhanced_image = enhance_image(page)
        try:
            enhanced_image.save(output_file, 'JPEG', optimize=True, quality=100, progressive=True)
            print(f'Saved: {output_file}')
        except Exception as e:
            print(f"Error saving image: {e}")
    
    return output_dir  # Return directory for index.html update

def enhance_image(img, new_width=470):
    img = img.convert('RGB')
    w_percent = new_width / float(img.width)
    new_height = int(float(img.height) * w_percent)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    # img = ImageEnhance.Sharpness(img).enhance(1.2)
    # img = ImageEnhance.Brightness(img).enhance(1.3)
    # img = ImageEnhance.Contrast(img).enhance(1.2)
    return img

def update_index_html(output_dirs):
    index_path = "index.html"
    links = []
    for folder in output_dirs:
        first_image = os.listdir(folder)[0] if os.listdir(folder) else None
        if first_image:
            folder_name = os.path.basename(folder)
            link = f'<li><a href="./{folder}/{first_image}">{folder_name}</a></li>'
            links.append(link)
    
    with open(index_path, "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Read PDFs</title>
        </head>
        <body>
            <div>
                <ul>
        """ + "\n".join(links) + """
                </ul>
            </div>
        </body>
        </html>
        """)
    print("Updated index.html")

def process_pdfs(pdf_folder_or_file):
    output_dirs = []
    if os.path.isdir(pdf_folder_or_file):
        for file in os.listdir(pdf_folder_or_file):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder_or_file, file)
                pdf_name = os.path.splitext(file)[0].replace(" ", "_")
                image_output_dir = os.path.join("pages", pdf_name)
                result = pdf_to_jpeg_with_enhancements(pdf_path, image_output_dir)
                if result:
                    output_dirs.append(result)
    elif os.path.isfile(pdf_folder_or_file) and pdf_folder_or_file.endswith(".pdf"):
        pdf_name = os.path.splitext(os.path.basename(pdf_folder_or_file))[0].replace(" ", "_")
        image_output_dir = os.path.join("pages", pdf_name)
        result = pdf_to_jpeg_with_enhancements(pdf_folder_or_file, image_output_dir)
        if result:
            output_dirs.append(result)
    
    if output_dirs:
        update_index_html(output_dirs)

if __name__ == '__main__':
    pdf_folder_or_file = "C:/Users/steezeless/Desktop/books/ass and ans/ENG 401 ASSIGNMENT AND ANSWERS.pdf"
    process_pdfs(pdf_folder_or_file)
