import pypandoc

file_name = "zinets-v0.8" # "zinets-v0.8" # "zinets-v0.5"
file_tex = f"{file_name}.tex"
file_md = f"{file_name}.md"

# Convert to LaTeX
pypandoc.convert_file(
    file_md, 
    'latex', 
    outputfile=file_tex,
    extra_args=[
        '--pdf-engine=xelatex',
        '--standalone',  # This ensures proper document structure
        '-V', 'documentclass=article',
        '-V', 'CJKmainfont=Noto Sans CJK TC Medium',
        '-V', 'geometry=margin=0.75in',  # adjust margins
        '-V', 'fontsize=11pt',        # change font size
        '-V', 'papersize=letter',     # set paper size        
    ]
)