I'll create a comprehensive blog post that incorporates all the font configuration information while maintaining the practical focus and key points about the tools.

# A Developer's Guide to Converting Markdown to PDF in Python

As a developer working with documentation, converting Markdown to PDF is a common requirement. After extensive testing, here's my comprehensive guide to help you choose and configure the right conversion tool for your needs.

## Pandoc: The Production-Grade Converter

Pandoc stands as the most powerful option for professional documentation. While it requires more setup and runs slower, it offers publication-quality output with excellent CJK (Chinese, Japanese, Korean) support.

### Setting Up Pandoc

1. Install Pandoc from https://pandoc.org/installing.html, or via Chocolatey:
```bash
choco install pandoc
```

2. Install MiKTeX (https://miktex.org/download) with these settings:
   - Enable "Install missing packages on the fly"
   - This ensures automatic handling of CJK packages

3. Install the Python wrapper:
```bash
pip install pypandoc
```

### Basic Usage

Here's a starter script with common configurations:

```python
import pypandoc

pypandoc.convert_file(
    'input.md', 
    'pdf', 
    outputfile='output.pdf',
    extra_args=[
        '--pdf-engine=xelatex',
        '-V', 'CJKmainfont=Microsoft YaHei',  
        '-V', 'geometry=margin=0.5in',
        '-V', 'fontsize=11pt',
        '-V', 'papersize=letter'
    ]
)
```

### Advanced Font Configuration

Pandoc's power really shines in its font handling capabilities. Here's how to explore and configure fonts:

1. **Check Available System Fonts**
```powershell
# If fontconfig is installed:
fc-list
# Or PowerShell alternative:
[System.Drawing.FontFamily]::Families | Select-Object Name
```

2. **Comprehensive Font Configuration**
```python
pypandoc.convert_file(
    'input.md',
    'pdf',
    outputfile='output.pdf',
    extra_args=[
        '--pdf-engine=xelatex',
        '-V', 'mainfont=Arial',                    # Main text
        '-V', 'CJKmainfont=SimSun',               # Main CJK
        '-V', 'sansfont=Helvetica',               # Sans-serif
        '-V', 'monofont=Courier New',             # Monospace
        '-V', 'mathfont=XITS Math',               # Math
        '-V', 'CJKsansfont=Noto Sans CJK SC',     # CJK sans
        '-V', 'CJKmonofont=Noto Sans Mono CJK SC' # CJK mono
    ]
)
```

3. **Font Debugging**
Add to your markdown:
```latex
---
header-includes: |
    \usepackage{fontspec}
    \listfiles
---
```

## GitHub-Style with Grip + WeasyPrint

This combination offers a unique workflow advantage:

```python
import grip
import weasyprint

grip.export('input.md', 'temp.html')
weasyprint.HTML('temp.html').write_pdf('output.pdf')
```

What makes this approach special:
- Lightning-fast conversion
- Browser preview capability (`grip file.md` → http://localhost:6419)
- The wide right margin, often seen as a limitation, is actually perfect for document review annotations and editorial comments

## Lighter Alternatives

Several other options exist for simpler needs:

- **mdpdf**: Simple but limited CJK support
- **markdown-pdf**: Uses headless Chrome
- **md2pdf**: WeasyPrint-based solution

## Choosing Your Tool

The decision largely depends on your use case:
- **Publication/Professional Documents**: Use Pandoc. The slower conversion is worth it for the quality and font control.
- **Document Review/Collaboration**: Choose Grip + WeasyPrint. The annotation-friendly margins and quick preview make it ideal.
- **Quick Conversions**: Consider mdpdf or markdown-pdf for simple documents.

## Font Resources

For those diving deep into font configuration:
- XeLaTeX Font Catalogue: https://tug.org/FontCatalogue/
- Fontspec documentation: https://ctan.org/pkg/fontspec
- Pandoc Variables: https://pandoc.org/MANUAL.html#variables-for-latex

Remember that font availability depends on your system installation. Some fonts might require additional LaTeX packages or system fonts.

## Conclusion

While Pandoc and Grip + WeasyPrint stand out as the primary solutions, each tool has its place. Pandoc excels in professional document production with its extensive font control, while Grip + WeasyPrint shines in collaborative workflows with its review-friendly format.

Choose based on your needs: output quality, processing speed, font requirements, and collaboration features. The right tool will make your Markdown to PDF workflow smooth and efficient.

---

*Note: Document conversion tools evolve rapidly. Always check the latest documentation for up-to-date instructions.*

source: https://claude.ai/chat/363733ce-0a5a-48c7-8f6c-c98ab039a4c8