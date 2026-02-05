import pypandoc

file_name = "ustcj2025-2c"  # Replace with your .tex file name (without extension)
file_pdf = f"{file_name}.pdf"
file_tex = f"{file_name}.tex"

# Convert .tex to .pdf
pypandoc.convert_file(
    file_tex, 
    'pdf', 
    outputfile=file_pdf,
    extra_args=[
        '--pdf-engine=xelatex',  # Use XeLaTeX for CJK support
        # '-V', 'CJKmainfont=SimSun',  # Specify a CJK font (e.g., SimSun for Chinese)
        # '-V', 'CJKmainfont="Noto Sans CJK SC"',  # Specify a CJK font (e.g., SimSun for Chinese)
        '-V', 'geometry=margin=0.75in',  # Adjust margins
        '-V', 'fontsize=11pt',  # Set font size
        '-V', 'papersize=letter',  # Set paper size
    ]
)