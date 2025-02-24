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
    
    # Get all supported image files
    image_files = []
    for ext in SUPPORTED_EXTENSIONS:
        for file in images_dir.glob(f'*{ext}'):
            mod_time = file.stat().st_mtime
            image_files.append((file.name, mod_time))
    
    if not image_files:
        raise click.BadParameter(f"No supported image files found in '{input_folder}'")
    
    # Sort by creation time
    image_files.sort(key=lambda x: x[1])
    
    # Generate HTML content with enhanced CSS
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Gallery</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .image-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .image-container img {
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 3px;
                transition: transform 0.3s ease;
            }
            .timestamp {
                margin-top: 10px;
                color: #666;
                font-size: 0.8em;
            }
            #zoom-view {
                display: none;          /* Only this display property */
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
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            #zoom-view img {
                width: auto;
                height: auto;
                max-width: 100%;
                max-height: calc(80vh - 160px); /* Leave space for info and buttons */
                display: block;
            }
            .image-info {
                width: 100%;
                text-align: center;
                margin: 15px 0;
                color: #333;
            }
            .counter {
                color: #666;
                font-size: 0.9em;
            }
            .loading {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 20px;
                border-radius: 10px;
                z-index: 1001;
                display: none;
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
                width: 100%;           /* Take full width */
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 15px;
                position: relative;    /* Position relative to zoom-view */
                bottom: 0;            /* Align to bottom */
            }
            .nav-button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            .nav-button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
            .nav-button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
            @media (max-width: 768px) {
                .gallery {
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                }
                .nav-buttons {
                    gap: 10px;
                }
                .nav-button {
                    padding: 8px 16px;
                    font-size: 14px;
                }
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
                <img src="{input_folder}/{filename}" alt="{filename}" loading="lazy">
                <div class="timestamp">ts: {timestamp}</div>
            </div>
        """
    
    # Add zoom view container with enhanced features
    html_content += f"""
        </div>
        <div class="loading" id="loading">Loading...</div>
        <div class="overlay" id="overlay" onclick="hideZoom()"></div>
        <div id="zoom-view">
            <img id="zoom-image" src="" alt="Zoomed image" onload="hideLoading()" onerror="hideLoading()">
            <div class="image-info">
                <div id="image-name"></div>
                <div class="counter" id="counter"></div>
            </div>
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
            
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            function updateImageInfo() {
                const counter = document.getElementById('counter');
                const imageName = document.getElementById('image-name');
                counter.textContent = `Image ${currentImageIndex + 1} of ${images.length}`;
                imageName.textContent = images[currentImageIndex];
            }
            
            function showZoom(filename) {
                currentImageIndex = images.indexOf(filename);
                const zoomView = document.getElementById('zoom-view');
                // Set image source first
                document.getElementById('zoom-image').src = imageFolder + '/' + images[currentImageIndex];
                updateImageInfo();
                // Show elements with correct display properties
                zoomView.style.display = 'flex';  // Use flex when showing
                document.getElementById('overlay').style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
            
            function hideZoom() {
                document.getElementById('zoom-view').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            function updateZoomImage() {
                showLoading();
                const zoomImage = document.getElementById('zoom-image');
                zoomImage.src = imageFolder + '/' + images[currentImageIndex];
                updateImageInfo();
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