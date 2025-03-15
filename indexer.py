import os

def create_image_html(folder, output_folder):
    images = [f for f in os.listdir(folder) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    images.sort()
    
    folder_name = os.path.basename(folder).replace('_', ' ')
    total_pages = (len(images) + 5) // 6
    
    for page_num in range(total_pages):
        page_images = images[page_num * 6 : (page_num + 1) * 6]
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{folder_name} - Page {page_num + 1}</title>
        </head>
        <body>
            <h1>{folder_name}</h1>
            <div>
        """
        for img in page_images:
            html_content += f'<a href="{img}"><img src="{img}" width="150"></a> '
        
        html_content += "<br><br>"
        if page_num > 0:
            html_content += f'<a href="page_{page_num}.html">Previous</a> '
        if page_num < total_pages - 1:
            html_content += f'<a href="page_{page_num + 2}.html">Next</a>'
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(os.path.join(output_folder, f'page_{page_num + 1}.html'), 'w') as f:
            f.write(html_content)

def generate_galleries(main_folder):
    index_links = []
    for sub_folder in sorted(os.listdir(main_folder)):
        full_path = os.path.join(main_folder, sub_folder)
        if os.path.isdir(full_path):
            output_folder = os.path.join(full_path, "html")
            os.makedirs(output_folder, exist_ok=True)
            create_image_html(full_path, output_folder)
            index_links.append(f'<li><a href="{sub_folder}/page_1.html">{sub_folder.replace("_", " ")}</a></li>')
    
    with open(os.path.join(main_folder, 'index.html'), 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Galleries</title>
        </head>
        <body>
            <h1>Available Galleries</h1>
            <ul>
        """ + "\n".join(index_links) + """
            </ul>
        </body>
        </html>
        """)
    print("Generated index.html")

if __name__ == '__main__':
    main_folder = "./pages"  # Set to the folder containing image folders
    generate_galleries(main_folder)
