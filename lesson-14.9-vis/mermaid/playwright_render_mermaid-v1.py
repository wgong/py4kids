import asyncio
from playwright.async_api import async_playwright
import click
import os

DEFAULT_MERMAID="mermaid_diagram.mmd"
DEFAULT_IMAGE="mermaid_diagram.png"
DEFAULT_WIDTH=1200
DEFAULT_HEIGHT=800

async def render_mermaid_chart(
            mermaid_code, 
            output_path=DEFAULT_IMAGE,
            viewport_width=DEFAULT_WIDTH, 
            viewport_height=DEFAULT_HEIGHT):
    """
    Renders a Mermaid diagram to a PNG file using Playwright.
    The viewport_width and viewport_height parameters control the browser window size.
    The screenshot will be taken of the rendered SVG, cropping any extra whitespace.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Set the viewport size to control the browser's rendering area
        await page.set_viewport_size({"width": viewport_width, "height": viewport_height})

        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    display: flex;
                    justify-content: center; /* Center the chart horizontally */
                    align-items: center;     /* Center the chart vertically */
                    height: 100vh;
                    background-color: white;
                }}
            </style>
        </head>
        <body>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <div id="mermaid-chart" class="mermaid">
                {mermaid_code}
            </div>
            <script>
                // Initialize Mermaid after the content is loaded
                document.addEventListener("DOMContentLoaded", () => {{
                    mermaid.initialize({{ startOnLoad: true }});
                }});
            </script>
        </body>
        </html>
        """
        await page.set_content(html_content)
        
        # Wait for the SVG to be rendered
        await page.wait_for_selector(".mermaid > svg")
        
        # Take a screenshot of just the SVG element to automatically crop whitespace
        await page.locator(".mermaid > svg").screenshot(path=output_path)
        
        await browser.close()

@click.command()
@click.option('-i', '--input-mermaid', default=DEFAULT_MERMAID, help='The path to the input file containing Mermaid code.')
@click.option('-o', '--output-image', help='The name of the output image file. Defaults to the input filename with a .png extension.')
@click.option('-W', '--img-width', default=1200, type=int, help='The width of the viewport for rendering.')
@click.option('-H', '--img-height', default=800, type=int, help='The height of the viewport for rendering.')
def main(input_mermaid, output_image, img_width, img_height):
    """
    Renders a Mermaid diagram from a file to a PNG image.
    """
    try:
        if not os.path.exists(input_mermaid):
            click.echo(f"Error: The file '{input_mermaid}' does not exist.")
            return

        with open(input_mermaid, 'r', encoding="utf-8") as f:
            mermaid_code = f.read()

    except Exception as e:
        click.echo(f"An error occurred while reading the file: {e}")
        return
    
    # If output_image is not provided, derive it from input_mermaid
    if output_image is None:
        base_name, _ = os.path.splitext(input_mermaid)
        output_image = f"{base_name}.png"    

    asyncio.run(render_mermaid_chart(
        mermaid_code=mermaid_code,
        output_path=output_image,
        viewport_width=img_width,
        viewport_height=img_height
    ))

if __name__ == "__main__":
    main()
