from PIL import Image, ImageEnhance
import os

def enhance_and_compress_images(input_folder, new_width=500, quality=80):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(input_folder, filename)

            try:
                img = Image.open(input_path).convert('RGB')

                # Resize while maintaining aspect ratio
                w_percent = new_width / float(img.width)
                new_height = int(float(img.height) * w_percent)
                img = img.resize((new_width, new_height), Image.LANCZOS)

                # img = ImageEnhance.Sharpness(img).enhance(1.1)  # Sharpen
                # img = ImageEnhance.Brightness(img).enhance(1.2)  # Brighten
                # img = ImageEnhance.Contrast(img).enhance(1.3)  # Increase contrast

                # Save with compression
                img.save(output_path, 'JPEG', optimize=True, quality=quality, progressive=True)

                print(f"Processed and saved: {output_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
input_folder = "C:/Users/steezeless/Desktop/reader/pages/EEE_405"  # Change to your folder containing images
enhance_and_compress_images(input_folder)
