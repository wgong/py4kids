# AWS SageMaker Studio Setup Guide for docx-md.py

This guide provides AWS SageMaker Studio-specific instructions for setting up and using the `docx-md.py` document conversion tool.

## Overview

AWS SageMaker Studio has specific constraints that affect package installation and system-level tools like Pandoc. This guide addresses these challenges and provides working solutions.

## Installation Options for SageMaker Studio

### Option 1: pypandoc-binary (Recommended ⭐)

The most reliable option for SageMaker Studio environments:

```bash
pip install pypandoc-binary
```

**Why this works:**
- Includes Pandoc binary bundled with the Python package
- No system-level installation required
- Works in containerized environments
- Persists with your conda environment

**Usage:**
```bash
python docx-md.py --in document.md --engine pypandoc --number-sections
```

### Option 2: Conda Installation

Often works when pip/apt installations fail:

```bash
conda install -c conda-forge pandoc
```

**Usage:**
```bash
python docx-md.py --in document.md --engine pandoc --number-sections
```

### Option 3: User-space Installation

For cases where conda doesn't work:

```bash
# Download Pandoc to user directory
cd /tmp
wget https://github.com/jgm/pandoc/releases/download/3.1.8/pandoc-3.1.8-linux-amd64.tar.gz
tar -xzf pandoc-3.1.8-linux-amd64.tar.gz

# Add to PATH (add this to your ~/.bashrc for persistence)
export PATH=/tmp/pandoc-3.1.8/bin:$PATH

# Verify installation
pandoc --version
```

## Complete Setup Instructions

### Step 1: Install Base Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install SageMaker-Compatible Pandoc

Choose one of the options above. We recommend starting with Option 1:

```bash
pip install pypandoc-binary
```

### Step 3: Verify Installation

```bash
python -c "import pypandoc; print('pypandoc-binary installed successfully')"
```

### Step 4: Test Conversion

```bash
# Create a test file
echo "# Test Document

## Section 1
Content here.

## Section 2
More content." > test.md

# Test conversion with section numbering
python docx-md.py --in test.md --engine pypandoc --number-sections

# Clean up
rm test.md test.docx
```

## SageMaker Studio Specific Considerations

### Environment Persistence

SageMaker Studio environments can be ephemeral. To ensure your setup persists:

1. **Use conda environments:**
   ```bash
   conda create -n docx2md python=3.11
   conda activate docx2md
   pip install -r requirements.txt pypandoc-binary
   ```

2. **Add to startup script** (if using custom images):
   ```bash
   echo 'export PATH=/tmp/pandoc-3.1.8/bin:$PATH' >> ~/.bashrc
   ```

### Memory and Performance

For large documents in SageMaker:

- Use smaller instance types for basic conversions
- Consider `ml.t3.medium` or `ml.t3.large` for complex documents
- MarkItDown engine is more memory-efficient for DOCX→MD conversions

## Engine Comparison for SageMaker

| Engine | SageMaker Compatibility | Installation | Section Numbering |
|--------|------------------------|--------------|-------------------|
| **pypandoc** (with pypandoc-binary) | ✅ Excellent | `pip install pypandoc-binary` | ✅ Yes |
| **pandoc** (system) | ⚠️ Limited | Requires conda or manual setup | ✅ Yes |
| **markitdown** | ✅ Excellent | `pip install markitdown[all]` | ❌ No |
| **md2docx** | ✅ Excellent | `pip install md2docx-python` | ❌ No |

## Troubleshooting

### Common Issues and Solutions

#### "pandoc not found in system PATH"

**Solution:** Use pypandoc-binary instead:
```bash
pip install pypandoc-binary
python docx-md.py --in document.md --engine pypandoc --number-sections
```

#### "Permission denied" errors

**Solution:** SageMaker Studio restricts system modifications. Use user-space installations:
- Use `pip install --user` if needed
- Install to conda environments instead of system-wide

#### "ModuleNotFoundError: No module named 'pypandoc'"

**Solution:** Install in the correct conda environment:
```bash
conda activate your-environment
pip install pypandoc-binary
```

#### Large file conversion failures

**Solution:**
- Use MarkItDown for DOCX→MD (more memory efficient)
- Break large documents into smaller sections
- Increase SageMaker instance memory if needed

## Best Practices for SageMaker Studio

1. **Use conda environments** for package isolation
2. **Prefer pypandoc-binary** over system pandoc
3. **Test with small files first** before processing large documents
4. **Set environment variables** in your notebook/script:
   ```python
   import os
   os.environ['PYPANDOC_PANDOC'] = '/path/to/pandoc'  # if using manual installation
   ```

## Example SageMaker Notebook Setup

```python
# Cell 1: Setup
import subprocess
import sys

# Install requirements
subprocess.check_call([sys.executable, "-m", "pip", "install", "pypandoc-binary", "click", "markitdown[all]"])

# Cell 2: Test conversion
import os
os.chdir('/path/to/docx2md/')

# Create test markdown
with open('test.md', 'w') as f:
    f.write("""# Introduction
## Overview
## Objectives
# Methodology
## Approach""")

# Convert with numbering
subprocess.run(['python', 'docx-md.py', '--in', 'test.md', '--engine', 'pypandoc', '--number-sections'])
```

## Support and Resources

- **SageMaker Documentation**: [Amazon SageMaker Studio](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html)
- **pypandoc-binary**: [PyPI Package](https://pypi.org/project/pypandoc-binary/)
- **Pandoc Documentation**: [Pandoc User Guide](https://pandoc.org/MANUAL.html)

For additional help with SageMaker-specific issues, consult the AWS SageMaker community forums or AWS Support.