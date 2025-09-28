import click
import os
import sys
import subprocess
import shutil
from pathlib import Path
from md2docx_python.src.md2docx_python import markdown_to_word
from md2docx_python.src.docx2md_python import word_to_markdown

try:
    import pypandoc
    PYPANDOC_AVAILABLE = True
except ImportError:
    PYPANDOC_AVAILABLE = False

try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False

def md_to_docx(markdown_file: str, word_file: str):
    """Converts a Markdown (.md) file to a Word (.docx) file."""
    try:
        markdown_to_word(markdown_file, word_file)
        print(f"✅ Successfully converted '{markdown_file}' to '{word_file}'")
    except Exception as e:
        print(f"❌ Error during MD to DOCX conversion: {e}")
        sys.exit(1)

def docx_to_md(word_file: str, markdown_file: str):
    """Converts a Word (.docx) file to a Markdown (.md) file."""
    try:
        word_to_markdown(word_file, markdown_file)
        print(f"✅ Successfully converted '{word_file}' to '{markdown_file}'")
    except Exception as e:
        print(f"❌ Error during DOCX to MD conversion: {e}")
        sys.exit(1)

def pandoc_convert(input_file: str, output_file: str, engine: str = "pypandoc", number_sections: bool = False):
    """Convert using Pandoc (via pypandoc or system pandoc)."""
    extra_args = []
    if number_sections:
        extra_args.append('--number-sections')

    if engine == "pypandoc" and PYPANDOC_AVAILABLE:
        try:
            pypandoc.convert_file(input_file, 'docx' if output_file.endswith('.docx') else 'md',
                                outputfile=output_file, extra_args=extra_args)
            print(f"✅ Successfully converted '{input_file}' to '{output_file}' using pypandoc")
        except Exception as e:
            print(f"❌ Error during pypandoc conversion: {e}")
            sys.exit(1)
    else:
        # Use system pandoc
        if not shutil.which('pandoc'):
            print(f"❌ Pandoc not found in system PATH. Please install pandoc or use another engine.")
            sys.exit(1)

        cmd = ['pandoc', input_file, '-o', output_file] + extra_args
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Successfully converted '{input_file}' to '{output_file}' using system pandoc")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during pandoc conversion: {e.stderr}")
            sys.exit(1)

def markitdown_convert(input_file: str, output_file: str):
    """Convert using MarkItDown (DOCX to MD only)."""
    if not MARKITDOWN_AVAILABLE:
        print(f"❌ MarkItDown not available. Install with: pip install 'markitdown[all]'")
        sys.exit(1)

    if not input_file.endswith('.docx'):
        print(f"❌ MarkItDown only supports DOCX to MD conversion")
        sys.exit(1)

    try:
        md_converter = MarkItDown()
        result = md_converter.convert(input_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.text_content)

        print(f"✅ Successfully converted '{input_file}' to '{output_file}' using MarkItDown")
    except Exception as e:
        print(f"❌ Error during MarkItDown conversion: {e}")
        sys.exit(1)

def detect_file_type(file_path: str) -> str:
    """Detect file type based on extension."""
    suffix = Path(file_path).suffix.lower()
    if suffix == '.md':
        return 'markdown'
    elif suffix == '.docx':
        return 'docx'
    else:
        raise click.BadParameter(f"Unsupported file type: {suffix}. Only .md and .docx files are supported.")

def auto_generate_output_path(input_path: str) -> str:
    """Auto-generate output path based on input file type."""
    path = Path(input_path)
    if path.suffix.lower() == '.md':
        return str(path.with_suffix('.docx'))
    elif path.suffix.lower() == '.docx':
        return str(path.with_suffix('.md'))
    else:
        raise click.BadParameter(f"Cannot auto-generate output for file type: {path.suffix}")

@click.command()
@click.option('--in', 'input_file', required=True, type=click.Path(exists=True, readable=True),
              help='Input file path (.md or .docx)')
@click.option('--out', 'output_file', type=click.Path(),
              help='Output file path (optional - will auto-generate if not provided)')
@click.option('--engine', type=click.Choice(['md2docx', 'pandoc', 'pypandoc', 'markitdown']),
              default='md2docx', help='Conversion engine to use (default: md2docx)')
@click.option('--number-sections', is_flag=True,
              help='Enable automatic section numbering (pandoc only)')
@click.help_option('--help', '-h')
def convert(input_file: str, output_file: str, engine: str, number_sections: bool):
    """
    Convert between Markdown (.md) and Word (.docx) files using various engines.

    The tool automatically detects the input file type and converts accordingly:
    - .md files are converted to .docx
    - .docx files are converted to .md

    Available engines:
    - md2docx: Original md2docx-python library (default)
    - pandoc/pypandoc: Pandoc conversion with advanced features
    - markitdown: Microsoft MarkItDown (DOCX to MD only)

    Examples:
        python docx-md.py --in document.docx --out document.md
        python docx-md.py --in document.md --out document.docx --engine pandoc
        python docx-md.py --in document.docx --engine markitdown
        python docx-md.py --in document.md --engine pandoc --number-sections
    """
    # Validate input file exists
    if not os.path.exists(input_file):
        click.echo(f"❌ Input file does not exist: {input_file}", err=True)
        sys.exit(1)

    # Auto-generate output path if not provided
    if not output_file:
        output_file = auto_generate_output_path(input_file)
        click.echo(f"📁 Auto-generated output path: {output_file}")

    # Detect input and output file types
    input_type = detect_file_type(input_file)
    output_type = detect_file_type(output_file)

    # Validate conversion direction
    if input_type == output_type:
        click.echo(f"❌ Input and output files have the same type ({input_type}). No conversion needed.", err=True)
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        click.echo(f"📁 Created output directory: {output_dir}")

    # Validate engine compatibility
    if engine == 'markitdown' and input_type != 'docx':
        click.echo(f"❌ MarkItDown only supports DOCX to MD conversion", err=True)
        sys.exit(1)

    if number_sections and engine not in ['pandoc', 'pypandoc']:
        click.echo(f"❌ Section numbering only supported with pandoc engines", err=True)
        sys.exit(1)

    # Perform conversion
    click.echo(f"🔄 Converting {input_type} to {output_type} using {engine}...")

    if engine in ['pandoc', 'pypandoc']:
        pandoc_convert(input_file, output_file, engine, number_sections)
    elif engine == 'markitdown':
        markitdown_convert(input_file, output_file)
    elif engine == 'md2docx':
        if input_type == 'markdown' and output_type == 'docx':
            md_to_docx(input_file, output_file)
        elif input_type == 'docx' and output_type == 'markdown':
            docx_to_md(input_file, output_file)
        else:
            click.echo(f"❌ Unsupported conversion: {input_type} to {output_type}", err=True)
            sys.exit(1)
    else:
        click.echo(f"❌ Unknown engine: {engine}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    convert()