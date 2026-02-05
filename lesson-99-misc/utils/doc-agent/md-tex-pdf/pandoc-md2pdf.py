import pypandoc

file_name = "ustc-journal-ENU-v0.5" # "zinets-v0.8" # "zinets-v0.5"
file_pdf = f"{file_name}.pdf"
file_md = f"{file_name}.md"

# Basic test
pypandoc.convert_file(
    file_md, 
    'pdf', 
    outputfile=file_pdf,
    extra_args=[
        '--pdf-engine=xelatex',
        # '-V', 'CJKmainfont=SimSun',  # Specify a CJK font (e.g., SimSun for Chinese)
        # '-V', 'CJKmainfont="AR PL SungtiL GB"',  # Specify a CJK font (e.g., SimSun for Chinese)
        '-V', 'geometry=margin=0.75in',  # adjust margins
        '-V', 'fontsize=11pt',        # change font size
        '-V', 'papersize=letter',         # set paper size        
    ]
)
