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
                position: relative;
            }
            .image-container {
                background: white;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                cursor: pointer;
                position: relative;
            }
            .image-container img {
                max-width: 100%;
                height: auto;
                transition: transform 0.3s ease;
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
                width: 90vw;  /* Changed from max-width to width */
                height: 90vh; /* Changed from max-height to height */
                display: flex;  /* Added flex display */
                flex-direction: column; /* Stack image and buttons vertically */
                justify-content: center; /* Center content vertically */
            }
            #zoom-view img {
                max-width: 90vw;  /* Increased from previous value */
                max-height: 80vh; /* Increased from previous value */
                object-fit: contain;
                margin: auto;     /* Center the image */
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
                gap: 10px;
                margin-top: 15px;
            }
            .nav-button {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            .nav-button:hover {
                background-color: #45a049;
            }
            .nav-button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
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
            <div class="image-container" onclick="showZoom('{filename}')">
                <img src="images/{filename}" alt="{filename}">
                <div class="timestamp">ts: {timestamp}</div>
            </div>
        """
    
    # Add zoom view container with navigation
    html_content += """
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
            const images = [
    """
    
    # Add image filenames as JavaScript array
    for filename, _ in image_files:
        html_content += f"'{filename}',"
    
    html_content += """
            ];
            
            function showZoom(filename) {
                currentImageIndex = images.indexOf(filename);
                updateZoomImage();
                document.getElementById('zoom-view').style.display = 'block';
                document.getElementById('overlay').style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
            
            function hideZoom() {
                document.getElementById('zoom-view').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            function updateZoomImage() {
                document.getElementById('zoom-image').src = 'images/' + images[currentImageIndex];
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
    with open(FILE_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    create_image_gallery()