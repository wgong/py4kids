import re
from IPython.display import display, Markdown, HTML
from IPython.core.display import Code

def display_grok_response(parsed_response, show_stats=True):
    """
    Display Grok response content nicely in Jupyter Notebook
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        show_stats (bool): Whether to show token usage statistics
    """
    
    content = parsed_response.get('message_content', '')
    
    if show_stats:
        # Display token usage statistics
        stats_html = f"""
        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <h4>📊 Token Usage Statistics</h4>
            <ul>
                <li><strong>Model:</strong> {parsed_response.get('model', 'N/A')}</li>
                <li><strong>Total Tokens:</strong> {parsed_response.get('total_tokens', 0)}</li>
                <li><strong>Prompt Tokens:</strong> {parsed_response.get('prompt_tokens', 0)}</li>
                <li><strong>Completion Tokens:</strong> {parsed_response.get('completion_tokens', 0)}</li>
                <li><strong>Reasoning Tokens:</strong> {parsed_response.get('reasoning_tokens', 0)}</li>
                <li><strong>Finish Reason:</strong> {parsed_response.get('finish_reason', 'N/A')}</li>
            </ul>
        </div>
        """
        display(HTML(stats_html))
    
    # Display the main content
    display(Markdown("### 🤖 Grok Response:"))
    display(Markdown(content))

def extract_code_blocks(content):
    """
    Extract code blocks from markdown content
    
    Args:
        content (str): Content with potential code blocks
        
    Returns:
        list: List of dictionaries with 'language' and 'code' keys
    """
    # Pattern to match code blocks with language specification
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match[0] if match[0] else 'text'
        code = match[1].strip()
        code_blocks.append({
            'language': language,
            'code': code
        })
    
    return code_blocks

def display_code_blocks(parsed_response):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
        display(Code(block['code'], language=block['language']))

def extract_and_save_code(parsed_response, filename=None):
    """
    Extract code blocks and optionally save to file
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        filename (str): Optional filename to save the code
        
    Returns:
        list: List of code blocks
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found.")
        return []
    
    # If filename provided, save the first code block
    if filename and code_blocks:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code_blocks[0]['code'])
        print(f"Code saved to {filename}")
    
    return code_blocks

def quick_test_code(parsed_response):
    """
    Quick test function - extracts first Python code block and returns it for execution
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        
    Returns:
        str: Python code ready for execution
    """
    code_blocks = extract_code_blocks(parsed_response.get('message_content', ''))
    
    python_blocks = [block for block in code_blocks if block['language'].lower() == 'python']
    
    if not python_blocks:
        print("No Python code blocks found.")
        return ""
    
    return python_blocks[0]['code']

# Enhanced display function with everything
def display_grok_analysis(parsed_response, extract_code=True, show_stats=True):
    """
    Complete analysis and display of Grok response
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        show_stats (bool): Whether to show token usage statistics
    """
    
    # Show statistics
    if show_stats:
        display_grok_response(parsed_response, show_stats=True)
    else:
        display_grok_response(parsed_response, show_stats=False)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response)

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the helper with your Fibonacci response"""
    
    # Your actual Fibonacci response
    fibonacci_response = {
        'message_content': '```python\ndef fibonacci(n):\n    """\n    计算斐波那契数列的第n项（从0开始索引）。\n    例如：\n    - fibonacci(0) = 0\n    - fibonacci(1) = 1\n    - fibonacci(2) = 1\n    - fibonacci(3) = 2\n    - fibonacci(4) = 3\n    - fibonacci(5) = 5\n\n    参数:\n    n (int): 非负整数，表示斐波那契数列的索引。\n\n    返回:\n    int: 斐波那契数列的第n项。\n\n    异常:\n    ValueError: 如果n为负数。\n    """\n    if n < 0:\n        raise ValueError("n must be a non-negative integer")\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    \n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n\n# 示例用法\nif __name__ == "__main__":\n    print(fibonacci(0))  # 输出: 0\n    print(fibonacci(1))  # 输出: 1\n    print(fibonacci(5))  # 输出: 5\n    print(fibonacci(10)) # 输出: 55\n```',
        'model': 'grok-4-0709',
        'total_tokens': 697,
        'prompt_tokens': 24,
        'completion_tokens': 301,
        'reasoning_tokens': 372,
        'finish_reason': 'stop',
        'response_id': 'bb50a4de-ca80-0d5e-ab8f-ce5b4ddfb758',
        'created': 1752149057
    }
    
    # Display with full analysis
    display_grok_analysis(fibonacci_response)
    
    # Extract code for testing
    code = quick_test_code(fibonacci_response)
    print("\n" + "="*50)
    print("🚀 Ready to test! Use this code:")
    print("="*50)
    return code

# Simple usage examples
"""
# Basic usage:
display_grok_response(your_parsed_response)

# With code extraction:
display_grok_analysis(your_parsed_response)

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)  # Execute the code

# Save code to file:
extract_and_save_code(your_parsed_response, "fibonacci.py")
"""
