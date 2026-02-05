#!/usr/bin/env python3
"""
PDF to Markdown Converter CLI

Convert PDF documents to Markdown format using Docling.
Preserves document structure, tables, and formatting.
"""

import click
from pathlib import Path
import sys
from typing import Optional


def convert_pdf_to_markdown(pdf_path: Path, output_path: Path) -> bool:
    """
    Convert a PDF file to Markdown format using Docling.

    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output Markdown file

    Returns:
        True if successful, False otherwise
    """
    try:
        from docling.document_converter import DocumentConverter

        click.echo(f"📖 Reading PDF: {pdf_path.name}")

        # Initialize converter
        converter = DocumentConverter()

        # Convert PDF to document format
        with click.progressbar(length=100, label='Converting PDF') as bar:
            result = converter.convert(str(pdf_path))
            bar.update(50)

            # Export to Markdown
            markdown_content = result.document.export_to_markdown()
            bar.update(50)

        # Write markdown to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content, encoding='utf-8')

        click.echo(f"✅ Successfully converted to: {output_path}")
        click.echo(f"📊 Output size: {len(markdown_content)} characters")

        return True

    except ImportError:
        click.echo("❌ Error: Docling library not installed", err=True)
        click.echo("   Install with: pip install docling", err=True)
        return False
    except Exception as e:
        click.echo(f"❌ Error converting PDF: {str(e)}", err=True)
        return False


@click.command()
@click.option(
    '--input', '-i',
    'input_file',
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help='Input PDF file path'
)
@click.option(
    '--output', '-o',
    'output_file',
    default=None,
    type=click.Path(path_type=Path),
    help='Output Markdown file path (default: same name with .md extension)'
)
@click.option(
    '--overwrite',
    is_flag=True,
    default=False,
    help='Overwrite existing output file'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    default=False,
    help='Show detailed conversion information'
)
def convert(input_file: Path, output_file: Optional[Path], overwrite: bool, verbose: bool):
    """
    Convert PDF documents to Markdown format.

    This tool uses Docling to extract content from PDF files and convert them
    to clean, well-formatted Markdown. It preserves document structure, tables,
    lists, and text formatting.

    Examples:

        # Convert a single PDF (output: document.md)
        python convert_pdf2md.py --input document.pdf

        # Specify custom output path
        python convert_pdf2md.py --input document.pdf --output notes.md

        # Overwrite existing file
        python convert_pdf2md.py -i document.pdf -o output.md --overwrite

        # Verbose output
        python convert_pdf2md.py -i document.pdf -v
    """

    # Validate input file
    if not input_file.suffix.lower() == '.pdf':
        click.echo(f"❌ Error: Input file must be a PDF (got: {input_file.suffix})", err=True)
        sys.exit(1)

    # Determine output path
    if output_file is None:
        output_file = input_file.with_suffix('.md')
        if verbose:
            click.echo(f"📝 Using default output: {output_file}")

    # Check if output exists
    if output_file.exists() and not overwrite:
        click.echo(f"⚠️  Output file already exists: {output_file}", err=True)
        click.echo("   Use --overwrite to replace it", err=True)
        sys.exit(1)

    # Display conversion info
    click.echo("=" * 60)
    click.echo("📄 PDF to Markdown Converter")
    click.echo("=" * 60)
    click.echo(f"Input:  {input_file.absolute()}")
    click.echo(f"Output: {output_file.absolute()}")

    if verbose:
        file_size = input_file.stat().st_size
        click.echo(f"Size:   {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    click.echo("-" * 60)

    # Convert PDF to Markdown
    success = convert_pdf_to_markdown(input_file, output_file)

    # Summary
    click.echo("=" * 60)
    if success:
        click.echo("✅ Conversion completed successfully!")

        if verbose:
            # Show preview of output
            content = output_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            click.echo(f"\n📋 Preview (first 10 lines):")
            click.echo("-" * 60)
            for line in lines[:10]:
                click.echo(line)
            if len(lines) > 10:
                click.echo(f"... ({len(lines) - 10} more lines)")

        sys.exit(0)
    else:
        click.echo("❌ Conversion failed")
        sys.exit(1)


if __name__ == '__main__':
    convert()
