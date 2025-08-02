import os
import re
import click
from pathlib import Path

def collect_slides():
    # Get all HTML files in the current directory
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # Filter files that match the pattern <3 digits>-<slide-name>.html
    pattern = re.compile(r'^(\d{3})-(.+)\.html$')
    slides = []
    
    for file in html_files:
        match = pattern.match(file)
        if match:
            slide_num = int(match.group(1))
            slide_name = match.group(2)
            slides.append((slide_num, slide_name, file))
    
    # Sort slides by their number
    slides.sort(key=lambda x: x[0])
    
    return slides

def generate_navigation_html(slides, title="AI Slides"):
    # Create the main HTML content
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML_TITLE</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
        }
        .sidebar {
            width: 250px;
            background-color: #f1f1f1;
            padding: 20px;
            overflow-y: auto;
            border-right: 1px solid #ddd;
        }
        .main-content {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        .slide-content {
            flex-grow: 1;
            border: 1px solid #ddd;
            padding: 20px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .navigation {
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .nav-button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .nav-button:hover {
            background-color: #45a049;
        }
        .toc-item {
            margin-bottom: 8px;
            cursor: pointer;
            padding: 5px;
            border-radius: 3px;
        }
        .toc-item:hover {
            background-color: #ddd;
        }
        .toc-item.active {
            background-color: #4CAF50;
            color: white;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Table of Contents</h2>
        <div class="toc-list">
"""

    # Add table of contents items
    for i, (slide_num, slide_name, file) in enumerate(slides):
        html_content += f'            <div class="toc-item" data-slide="{i}" data-file="{file}">{slide_num}: {slide_name}</div>\n'

    html_content += """
        </div>
    </div>
    <div class="main-content">
        <div class="slide-content">
            <iframe id="slide-frame" src=""></iframe>
        </div>
        <div class="navigation">
            <button class="nav-button" id="first-slide"><<</button>
            <button class="nav-button" id="prev-slide"><</button>
            <button class="nav-button" id="next-slide">></button>
            <button class="nav-button" id="last-slide">>></button>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const slides = [
"""

    # Add slide files to JavaScript array
    for i, (slide_num, slide_name, file) in enumerate(slides):
        if i > 0:
            html_content += ",\n"
        html_content += f'                "{file}"'

    html_content += """
            ];
            
            let currentSlide = 0;
            const slideFrame = document.getElementById('slide-frame');
            const tocItems = document.querySelectorAll('.toc-item');
            
            // Function to load a slide
            function loadSlide(index) {
                if (index >= 0 && index < slides.length) {
                    currentSlide = index;
                    slideFrame.src = slides[index];
                    
                    // Update active TOC item
                    tocItems.forEach(item => {
                        item.classList.remove('active');
                        if (parseInt(item.dataset.slide) === index) {
                            item.classList.add('active');
                        }
                    });
                }
            }
            
            // Load the first slide
            loadSlide(0);
            
            // Add click event to TOC items
            tocItems.forEach(item => {
                item.addEventListener('click', function() {
                    const slideIndex = parseInt(this.dataset.slide);
                    loadSlide(slideIndex);
                });
            });
            
            // Navigation button event listeners
            document.getElementById('first-slide').addEventListener('click', function() {
                loadSlide(0);
            });
            
            document.getElementById('prev-slide').addEventListener('click', function() {
                loadSlide(currentSlide - 1);
            });
            
            document.getElementById('next-slide').addEventListener('click', function() {
                loadSlide(currentSlide + 1);
            });
            
            document.getElementById('last-slide').addEventListener('click', function() {
                loadSlide(slides.length - 1);
            });
        });
    </script>
</body>
</html>
"""

    return html_content.replace("HTML_TITLE", title)
# 
@click.command()
@click.option('--title', default="AI Slides", help='HTML page title')
@click.option('--out-html', default='index_prefect.html', help='Output HTML file name')
def main(title, out_html):
    """Generate a navigation HTML page for presentation slides."""
    slides = collect_slides()
    if not slides:
        click.echo("No slides found with the naming convention <3 digits>-<slide-name>.html", err=True)
        return
    
    navigation_html = generate_navigation_html(slides, title=title)
    
    # Write the navigation HTML to a file
    with open(out_html, 'w') as f:
        f.write(navigation_html)
    
    click.echo(f"Navigation HTML created successfully with {len(slides)} slides.")
    click.echo(f"Output saved to: {out_html}")

if __name__ == "__main__":
    main()