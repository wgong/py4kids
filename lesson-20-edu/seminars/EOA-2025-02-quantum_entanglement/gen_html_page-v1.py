
from datetime import datetime
from pathlib import Path

FILE_HTML = 'quantum_computing.html'
FOLDER_IMAGE = 'images'
PAGE_TITLE = "Quantum Computing"

def create_image_gallery():
    # Get current directory and images folder
    images_dir = Path(FOLDER_IMAGE)
    
    # Get all PNG files with their creation times
    image_files = []
    for file in images_dir.glob('*.png'):
        mod_time = file.stat().st_mtime
        image_files.append((file.name, mod_time))
    
    # Sort by creation time
    image_files.sort(key=lambda x: x[1])
    
    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f0f0f0;
            }
            .gallery {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .image-container {
                background: white;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            img {
                max-width: 100%;
                height: auto;
            }
            .timestamp {
                margin-top: 10px;
                color: #666;
                font-size: 0.5em;
            }
        </style>
    </head>
    """
    html_content += f"""
    <body>
        <h1>{PAGE_TITLE}</h1>
        <div class="gallery">
    """
    
    # Add images to HTML
    for filename, creation_time in image_files:
        timestamp = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        html_content += f"""
            <div class="image-container">
                <img src="images/{filename}" alt="{filename}">
                <div class="timestamp">ts: {timestamp}</div>
            </div>
        """
    
    # Close HTML tags
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(FILE_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    create_image_gallery()