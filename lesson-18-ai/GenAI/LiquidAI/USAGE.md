# Liquid AI Model Usage Guide

## Files Created/Fixed

### 1. Streamlit Chatbot (`st_chat.py`)
A modern web-based chatbot interface using Streamlit.

**Features:**
- Interactive chat interface with message history
- Sidebar settings for response length control
- Example questions to get started
- Model caching to avoid reloading
- Clean, responsive UI

**To run:**
```bash
streamlit run st_chat.py
```

### 2. Fixed Jupyter Notebook (`ask_lfm_fixed.ipynb`)
A properly formatted Jupyter notebook with interactive widgets.

**Features:**
- Step-by-step cells for learning
- Interactive widgets interface
- Error handling and status updates
- Sample questions included
- Direct testing capabilities

**To run:**
```bash
jupyter notebook ask_lfm_fixed.ipynb
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For Jupyter support (if not already installed):
```bash
pip install jupyter
```

## What Was Fixed in the Notebook

The original `ask_lfm.ipynb` had several issues:
- Incorrect cell formatting (raw instead of code cells)
- Missing proper JSON structure for Jupyter
- No error handling or status feedback
- Limited interactive features

The new `ask_lfm_fixed.ipynb` provides:
- Proper cell structure and formatting
- Better error handling
- Status updates during generation
- More interactive features
- Clear documentation

## Model Details

Both implementations use:
- **Model:** LiquidAI/LFM2.5-1.2B-Instruct
- **Quantization:** 4-bit (nf4) with double quantization
- **Optimization:** Auto device mapping (GPU when available)
- **Parameters:** temperature=0.4, top_p=0.9, max_tokens=256 (configurable)

## Best Use Cases

This model excels at:
- Educational explanations
- Math and science problems
- Coding questions
- Step-by-step tutorials
- Simple reasoning tasks

## Troubleshooting

- **GPU Memory Issues:** The model uses 4-bit quantization to reduce memory usage
- **Slow Loading:** First run downloads the model (~1.2GB), subsequent runs use cache
- **Import Errors:** Make sure all requirements are installed: `pip install -r requirements.txt`