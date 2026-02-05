#!/usr/bin/env python3
"""
Image Format Converter CLI

Convert images between different formats using PIL/Pillow.
Supports batch conversion for folders and single file conversion.
"""

import click
from pathlib import Path
from PIL import Image
import sys
from typing import List, Optional


def convert_image(input_path: Path, output_path: Path, target_format: str) -> bool:
    """
    Convert a single image to target format.

    Args:
        input_path: Path to input image
        output_path: Path to output image
        target_format: Target format (e.g., 'png', 'jpg')

    Returns:
        True if successful, False otherwise
    """
    try:
        # Special handling for SVG (requires cairosvg)
        if input_path.suffix.lower() in ['.svg', '.svgz']:
            try:
                import cairosvg

                # Convert SVG to target format
                if target_format.lower() == 'png':
                    cairosvg.svg2png(url=str(input_path), write_to=str(output_path))
                elif target_format.lower() == 'pdf':
                    cairosvg.svg2pdf(url=str(input_path), write_to=str(output_path))
                elif target_format.lower() in ['jpg', 'jpeg']:
                    # SVG to JPEG requires intermediate PNG
                    import io
                    png_data = cairosvg.svg2png(url=str(input_path))
                    img = Image.open(io.BytesIO(png_data))
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Create white background for transparency
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    img.save(output_path, target_format.upper())
                else:
                    click.echo(f"⚠️  Warning: Unsupported SVG conversion to {target_format}", err=True)
                    return False

                return True
            except ImportError:
                click.echo("⚠️  Warning: cairosvg not installed. Install with: pip install cairosvg", err=True)
                click.echo("   Attempting fallback conversion with PIL (may not work for SVG)...", err=True)

        # Standard image conversion using PIL
        with Image.open(input_path) as img:
            # Handle transparency for formats that don't support it
            if target_format.lower() in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Convert and save
            img.save(output_path, target_format.upper())

        return True

    except Exception as e:
        click.echo(f"❌ Error converting {input_path.name}: {str(e)}", err=True)
        return False


def find_images(input_path: Path, src_format: Optional[str] = None) -> List[Path]:
    """
    Find all images in the given path.

    Args:
        input_path: Path to file or directory
        src_format: Source format to filter (e.g., 'svg', 'png')

    Returns:
        List of image file paths
    """
    if input_path.is_file():
        return [input_path]

    # Search for images in directory
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.svgz']

    if src_format:
        # Filter by source format
        src_ext = f".{src_format.lower()}" if not src_format.startswith('.') else src_format.lower()
        images = list(input_path.glob(f"**/*{src_ext}"))
    else:
        # Find all images
        images = []
        for ext in image_extensions:
            images.extend(input_path.glob(f"**/*{ext}"))

    return sorted(images)


@click.command()
@click.option(
    '--input', '-i',
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help='Input file or folder path'
)
@click.option(
    '--src_fmt', '-s',
    default=None,
    type=str,
    help='Source format filter (e.g., svg, png). If not specified, converts all images.'
)
@click.option(
    '--tgt_fmt', '-t',
    required=True,
    type=str,
    help='Target format (e.g., png, jpg, webp, pdf)'
)
@click.option(
    '--output', '-o',
    default=None,
    type=click.Path(path_type=Path),
    help='Output folder (default: same as input with "_converted" suffix)'
)
@click.option(
    '--overwrite',
    is_flag=True,
    default=False,
    help='Overwrite existing files'
)
@click.option(
    '--recursive/--no-recursive',
    default=True,
    help='Process subdirectories recursively (default: True)'
)
def convert(input: Path, src_fmt: Optional[str], tgt_fmt: str, output: Optional[Path],
            overwrite: bool, recursive: bool):
    """
    Convert images between different formats.

    Examples:

        # Convert all SVG files in a folder to PNG
        python convert_img.py --input ./images --src_fmt svg --tgt_fmt png

        # Convert a single image
        python convert_img.py --input ./logo.svg --tgt_fmt png

        # Convert all images in folder to JPEG
        python convert_img.py --input ./images --tgt_fmt jpg

        # Specify custom output folder
        python convert_img.py --input ./images --src_fmt png --tgt_fmt webp --output ./webp_images
    """

    # Validate target format
    supported_formats = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'pdf', 'ico']
    if tgt_fmt.lower() not in supported_formats:
        click.echo(f"❌ Unsupported target format: {tgt_fmt}", err=True)
        click.echo(f"   Supported formats: {', '.join(supported_formats)}", err=True)
        sys.exit(1)

    # Find all images
    click.echo(f"🔍 Searching for images in: {input}")
    images = find_images(input, src_fmt)

    if not images:
        click.echo(f"⚠️  No images found matching criteria", err=True)
        sys.exit(1)

    click.echo(f"📁 Found {len(images)} image(s) to convert")

    # Determine output directory
    if output is None:
        if input.is_file():
            output_dir = input.parent / f"{input.parent.name}_converted"
        else:
            output_dir = input.parent / f"{input.name}_converted"
        output = output_dir

    output.mkdir(parents=True, exist_ok=True)
    click.echo(f"📂 Output directory: {output}")

    # Convert images
    success_count = 0
    skip_count = 0
    error_count = 0

    with click.progressbar(images, label='Converting images') as bar:
        for img_path in bar:
            # Calculate relative path for maintaining directory structure
            if input.is_file():
                relative_path = img_path.name
            else:
                try:
                    relative_path = img_path.relative_to(input)
                except ValueError:
                    relative_path = img_path.name

            # Create output path
            output_file = output / relative_path.parent / f"{img_path.stem}.{tgt_fmt.lower()}"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Check if output already exists
            if output_file.exists() and not overwrite:
                skip_count += 1
                continue

            # Convert image
            if convert_image(img_path, output_file, tgt_fmt):
                success_count += 1
            else:
                error_count += 1

    # Summary
    click.echo("\n" + "=" * 50)
    click.echo("📊 Conversion Summary")
    click.echo("=" * 50)
    click.echo(f"✅ Successfully converted: {success_count}")
    if skip_count > 0:
        click.echo(f"⏭️  Skipped (already exists): {skip_count}")
    if error_count > 0:
        click.echo(f"❌ Failed: {error_count}")
    click.echo(f"📁 Output location: {output.absolute()}")

    if error_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    convert()
