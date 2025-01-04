Here are some popular Python libraries for converting Markdown to PDF:

## Using `pandoc` (most feature-rich but requires system installation):

Note: requires system install, but most capable with publication quality, slow to run, 

Here are the detailed installation steps:

1. Install Pandoc system package:
   - Windows: Download installer from https://pandoc.org/installing.html
   - Or use Chocolatey: `choco install pandoc`
   - Verify installation: `pandoc --version`

2. Install LaTeX distribution:
   - For Windows, MiKTeX is recommended: https://miktex.org/download
   - During MiKTeX installation:
     - Choose "Install missing packages on the fly = Yes"
     - This will auto-download CJK packages when needed
   - Verify installation: `pdflatex --version`

3. Install pypandoc:
```bash
pip install pypandoc
```

4. Test the installation:
```python
import pypandoc

# Basic test
pypandoc.convert_file(
    'input.md', 
    'pdf', 
    outputfile='output.pdf',
    extra_args=[
        '--pdf-engine=xelatex',
        '-V', 'CJKmainfont=SimSun',     # other CJK fonts: Microsoft YaHei KaiTi SimHei
        '-V', 'geometry=margin=0.5in',  # adjust margins
        '-V', 'fontsize=11pt',          # change font size
        '-V', 'papersize=letter',       # set paper size        

    ]
)
```


5. (Optional) check for MiKTeX updates
```
miktex-update.exe --update-setup
```
Follow MikTex Console update

### explore and verify available fonts for use with pandoc and XeLaTeX:

1. **Check System Fonts (Windows)**
```powershell
fc-list          # If you have fontconfig installed
# Or use PowerShell
[System.Drawing.FontFamily]::Families | Select-Object Name
```

2. **Check Available Fonts in XeLaTeX**
Create a test file `fonttest.tex`:
```latex
\documentclass{article}
\usepackage{fontspec}
\begin{document}
Currently installed fonts:
\directlua{
  fonts = fonts or { }
  for _,v in ipairs(fontloader.get_font_list()) do
    tex.print(v.fontname .. '\\newline')
  end
}
\end{document}
```

Then compile:
```bash
xelatex fonttest.tex
```

3. **Test Font in XeLaTeX Directly**
```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Font Name}
\begin{document}
Test text in the specified font
\end{document}
```

4. **Advanced Pandoc Font Options**
```python
pypandoc.convert_file(
    'input.md',
    'pdf',
    outputfile='output.pdf',
    extra_args=[
        '--pdf-engine=xelatex',
        '-V', 'mainfont=Arial',           # Main text font
        '-V', 'CJKmainfont=SimSun',       # Main CJK font
        '-V', 'sansfont=Helvetica',       # Sans-serif font
        '-V', 'monofont=Courier New',     # Monospace font
        '-V', 'mathfont=XITS Math',       # Math font
        '-V', 'CJKsansfont=Noto Sans CJK SC',  # CJK sans-serif
        '-V', 'CJKmonofont=Noto Sans Mono CJK SC',  # CJK monospace
    ]
)
```

5. **Font Debugging in XeLaTeX**
Add this to your markdown or template:
```latex
---
header-includes: |
    \usepackage{fontspec}
    \listfiles
---
```

This will generate a list of loaded fonts in the log file.

References:
- XeLaTeX Font Catalogue: https://tug.org/FontCatalogue/
- Fontspec package documentation: https://ctan.org/pkg/fontspec
- Pandoc Variables documentation: https://pandoc.org/MANUAL.html#variables-for-latex

Note: Font availability depends on your system installation. Some fonts might require additional LaTeX packages or system fonts to be installed.

## Using `grip` (GitHub-styled rendering) + weasyprint:

Note: Useful for quick preview in browser, CJK rendered correctly


Note: Easy to install and use, but PDF has big right-margin

If you love GitHub's Markdown rendering, this combination is perfect. It's particularly good at handling CJK text and offers several unique advantages:

- Lightning-fast conversion speed
- Excellent for quick previews in your browser
- The wide right margin in the GitHub style, while initially seeming like a limitation, actually provides a perfect space for annotations and editorial comments during document review


```
! pip install grip weasyprint

import grip
import weasyprint
# First convert MD to HTML with GitHub styling
grip.export('input.md', 'temp.html')
# Then HTML to PDF
weasyprint.HTML('temp.html').write_pdf('output.pdf')
```

```bash
grip <file.md>
open URL = http://localhost:6419
```

## mdpdf

https://pypi.org/project/mdpdf/

Note: Easy to install and use, but not good for CJK rendering

## two-step process with `markdown` + `pdfkit`:

TODO: NOT WORKING

This requires installing wkhtmltopdf (https://wkhtmltopdf.org/downloads.html) on your system but it's generally lighter than pandoc

```
! pip install markdown pdfkit wkhtmltopdf

import markdown
import pdfkit

# First convert MD to HTML
html = markdown.markdown(open('input.md').read())

# Then HTML to PDF
pdfkit.from_string(html, 'output.pdf')
```


## `md2pdf` (using WeasyPrint):

TODO: NOT WORKING

```
! pip install md2pdf

from md2pdf.core import md2pdf
md2pdf("output.pdf", "input.md")
```

## `markdown-pdf` (using headless Chrome):

```
! pip install markdown-pdf

import markdown_pdf
markdown_pdf.convert('input.md', 'output.pdf')

```
