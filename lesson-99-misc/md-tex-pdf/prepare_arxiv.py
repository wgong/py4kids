import re
import os
import shutil
import subprocess
import pypandoc

def convert_md_to_tex(md_filename):
    """Convert markdown to tex"""
    base_name = md_filename.rsplit('.', 1)[0]
    pypandoc.convert_file(
        md_filename,
        'latex',
        outputfile=f"{base_name}.tex",
        extra_args=['--standalone']
    )
    return base_name

def prepare_arxiv_package(base_filename):
    """Prepare files for arXiv submission"""
    submission_dir = f"{base_filename}_arxiv"
    # Create submission directory and images subdirectory
    os.makedirs(os.path.join(submission_dir, 'images'), exist_ok=True)
    
    # Copy main tex file
    shutil.copy(f"{base_filename}.tex", submission_dir)
    
    # Copy all images maintaining directory structure
    image_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    source_images_dir = './images'
    target_images_dir = os.path.join(submission_dir, 'images')
    
    if os.path.exists(source_images_dir):
        for file in os.listdir(source_images_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                shutil.copy(
                    os.path.join(source_images_dir, file),
                    os.path.join(target_images_dir, file)
                )
                print(f"Copied image: {file}")
    
    # Test compilation in the submission directory
    original_dir = os.getcwd()
    try:
        os.chdir(submission_dir)
        # First compilation
        subprocess.run(['xelatex', '-interaction=nonstopmode', f"{base_filename}.tex"], check=True)
        # Second run for references
        subprocess.run(['xelatex', '-interaction=nonstopmode', f"{base_filename}.tex"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in compilation: {e}")
    finally:
        os.chdir(original_dir)
    
    # Create submission zip
    shutil.make_archive(f"{base_filename}_arxiv", 'zip', submission_dir)
    
    print(f"\nSubmission package created: {base_filename}_arxiv.zip")

# Modified running section
md_file = "zinets-v0.9.md"  # Your markdown file
base_name = convert_md_to_tex(md_file)
prepare_arxiv_package(base_name)