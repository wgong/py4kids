"""
https://claude.ai/chat/64371ba7-5283-498b-8b08-2c1f7f9a6e23

Key improvements made:

- Added Click CLI with options for output file, input folder, and page title
- Added support for multiple image types (.png, .jpg, .jpeg, .gif)
- Added error handling for missing folders and no images
- Added feedback messages about gallery creation
- Added a gallery info section showing total images and generation time
- Made image paths dynamic based on input folder
- Added docstring with usage information


# Get help
$ python gallery.py --help

# Specify all options
$ python gallery-v3.1.py -o q_computing.html -i "images" -t "Quantum Computing"


"""

from datetime import datetime
from pathlib import Path
import click

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}

@click.command()
@click.option('-o', '--output', 'output_file', 
              default='gallery.html',
              help='Output HTML filename')
@click.option('-i', '--input', 'input_folder',
              default='images',
              help='Input folder containing images')
@click.option('-t', '--title', 'page_title',
              default='Image Gallery',
              help='HTML page title')
def create_image_gallery(output_file, input_folder, page_title):
    """Generate an HTML gallery from images in a folder.
    
    Supports image types: .png, .jpg, .jpeg, .gif
    """
    # Get input directory and verify it exists
    images_dir = Path(input_folder)
    if not images_dir.exists():
        raise click.BadParameter(f"Input folder '{input_folder}' does not exist")
    
    # Get all supported image files with their creation times
    image_files = []
    for ext in SUPPORTED_EXTENSIONS:
        for file in images_dir.glob(f'*{ext}'):
            mod_time = file.stat().st_mtime
            image_files.append((file.name, mod_time))
    
    if not image_files:
        raise click.BadParameter(f"No supported image files found in '{input_folder}'")
    
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
                position: relative;
            }
            .image-container {
                background: white;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                cursor: pointer;
                position: relative;
                transition: all 0.3s ease;  /* Smooth transition for all properties */
            }
            .image-container:hover {
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);  /* Deeper shadow on hover */
                transform: translateY(-2px);  /* Slight lift effect */
            }
            .image-container img {
                max-width: 100%;
                height: auto;
                transition: transform 0.3s ease;
            }
            .image-container:hover img {
                transform: scale(1.05);  /* Slightly enlarge image on hover */
            }            
            .timestamp {
                margin-top: 10px;
                color: #666;
                font-size: 0.5em;
            }
            #zoom-view {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1000;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                width: 90vw;
                height: 90vh;
            }
            #zoom-view img {
                width: auto;
                height: auto;
                max-width: 100%;
                max-height: calc(90vh - 100px); /* Account for padding and nav buttons */
                display: block;
                margin: 0 auto;
            }
            .overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                z-index: 999;
            }
            .nav-buttons {
                display: flex;
                justify-content: center;
                gap: 20px;  /* Increased gap */
                margin-top: 20px;
                position: fixed;  /* Fixed position */
                bottom: 40px;    /* Position from bottom */
                left: 50%;
                transform: translateX(-50%);
                z-index: 1001;   /* Above the zoom view */
            }
            .nav-button {
                padding: 12px 24px;  /* Larger buttons */
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 18px;    /* Larger font */
                transition: all 0.3s ease;
                opacity: 0.9;
            }
            .nav-button:hover {
                background-color: #45a049;
                transform: scale(1.1);
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                opacity: 1;
            }
            .nav-button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
            .gallery-info {
                color: #666;
                font-size: 0.8em;
                margin-top: 10px;
                text-align: center;
            }
        </style>
    </head>
    """
    html_content += f"""
    <body>
        <h1>{page_title}</h1>
        <div class="gallery">
    """
    
    # Add images to HTML
    for filename, creation_time in image_files:
        timestamp = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        html_content += f"""
            <div class="image-container" onclick="showZoom('{filename}')">
                <img src="{input_folder}/{filename}" alt="{filename}">
                <div class="timestamp">ts: {timestamp}</div>
            </div>
        """
    
    # Add zoom view container with navigation
    html_content += f"""
        </div>
        <div class="gallery-info">
            Total images: {len(image_files)} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        <div class="overlay" id="overlay" onclick="hideZoom()"></div>
        <div id="zoom-view">
            <img id="zoom-image" src="" alt="Zoomed image">
            <div class="nav-buttons">
                <button class="nav-button" onclick="navigateImage('first')">&lt;&lt;</button>
                <button class="nav-button" onclick="navigateImage('prev')">&lt;</button>
                <button class="nav-button" onclick="navigateImage('next')">&gt;</button>
                <button class="nav-button" onclick="navigateImage('last')">&gt;&gt;</button>
            </div>
        </div>
        
        <script>
            let currentImageIndex = 0;
            const imageFolder = '{input_folder}';
            const images = [
    """
    
    # Add image filenames as JavaScript array
    for filename, _ in image_files:
        html_content += f"'{filename}',"
    
    html_content += """
            ];
            
            function showZoom(filename) {
                currentImageIndex = images.indexOf(filename);
                // Set image source first, then show the view
                const zoomView = document.getElementById('zoom-view');
                const zoomImage = document.getElementById('zoom-image');
                zoomImage.src = 'images/' + images[currentImageIndex];
                
                // Show the zoom view and overlay
                zoomView.style.display = 'flex';
                document.getElementById('overlay').style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
            
            function hideZoom() {
                document.getElementById('zoom-view').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            function updateZoomImage() {
                const zoomImage = document.getElementById('zoom-image');
                zoomImage.src = 'images/' + images[currentImageIndex];
            }
            
            function navigateImage(direction) {
                switch(direction) {
                    case 'first':
                        currentImageIndex = 0;
                        break;
                    case 'prev':
                        currentImageIndex = Math.max(0, currentImageIndex - 1);
                        break;
                    case 'next':
                        currentImageIndex = Math.min(images.length - 1, currentImageIndex + 1);
                        break;
                    case 'last':
                        currentImageIndex = images.length - 1;
                        break;
                }
                updateZoomImage();
            }
            
            // Close on escape key
            document.addEventListener('keydown', function(event) {
                switch(event.key) {
                    case 'Escape':
                        hideZoom();
                        break;
                    case 'ArrowLeft':
                        navigateImage('prev');
                        break;
                    case 'ArrowRight':
                        navigateImage('next');
                        break;
                    case 'Home':
                        navigateImage('first');
                        break;
                    case 'End':
                        navigateImage('last');
                        break;
                }
            });
        </script>
    </body>
    </html>
    """
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        click.echo(f"Gallery created successfully: {output_file}")
        click.echo(f"Found {len(image_files)} images in {input_folder}")
    except Exception as e:
        raise click.ClickException(f"Error writing to file: {e}")

if __name__ == "__main__":
    create_image_gallery()