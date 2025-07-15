import re
from IPython.display import display, Markdown, HTML
try:
    from IPython.display import Code
except ImportError:
    # Fallback for older IPython versions
    Code = None

def display_grok_response(parsed_response, show_stats=True, collapsible_stats=False):
    """
    Display Grok response content nicely in Jupyter Notebook
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        show_stats (bool): Whether to show token usage statistics
        collapsible_stats (bool): Whether to make stats collapsible
    """
    
    content = parsed_response.get('message_content', '')
    
    if show_stats:
        # Create collapsible stats section
        stats_content = f"""
        <ul style="margin: 10px 0;">
            <li><strong>Model:</strong> {parsed_response.get('model', 'N/A')}</li>
            <li><strong>Total Tokens:</strong> {parsed_response.get('total_tokens', 0)}</li>
            <li><strong>Prompt Tokens:</strong> {parsed_response.get('prompt_tokens', 0)}</li>
            <li><strong>Completion Tokens:</strong> {parsed_response.get('completion_tokens', 0)}</li>
            <li><strong>Reasoning Tokens:</strong> {parsed_response.get('reasoning_tokens', 0)}</li>
            <li><strong>Finish Reason:</strong> {parsed_response.get('finish_reason', 'N/A')}</li>
        </ul>
        """
        
        if collapsible_stats:
            stats_html = f"""
            <details style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <summary style="cursor: pointer; font-weight: bold; font-size: 16px;">📊 Token Usage Statistics (Click to expand)</summary>
                {stats_content}
            </details>
            """
        else:
            stats_html = f"""
            <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h4>📊 Token Usage Statistics</h4>
                {stats_content}
            </div>
            """
        display(HTML(stats_html))
    
    # Display the main content with LaTeX support
    display(Markdown("### 🤖 Grok Response:"))
    display_content_with_latex(content)

def display_content_with_latex(content):
    """
    Display content with LaTeX math rendering support
    
    Args:
        content (str): Content that may contain LaTeX math
    """
    
    # Check if content contains LaTeX patterns (including old-style notation)
    latex_patterns = [
        r'\$\$.*?\$\

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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
""",  # Display math
        r'\$.*?\

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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
""",      # Inline math
        r'\\begin\{.*?\}.*?\\end\{.*?\}',  # LaTeX environments
        r'\\[a-zA-Z]+\{.*?\}',  # LaTeX commands
        r'\\\(.*?\\\)',  # Old-style inline math
        r'\\\[.*?\\\]',  # Old-style display math
    ]
    
    has_latex = any(re.search(pattern, content, re.DOTALL) for pattern in latex_patterns)
    
    if has_latex:
        # Enable MathJax for LaTeX rendering with comprehensive delimiter support
        mathjax_config = """
        <script>
        if (typeof window.MathJax === 'undefined') {
            window.MathJax = {
                tex: {
                    inlineMath: [['

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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
""", '

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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
"""], ['\\\\(', '\\\\)']],
                    displayMath: [['$', '$'], ['\\\\[', '\\\\]']],
                    processEscapes: true,
                    processEnvironments: true,
                    processRefs: true,
                    macros: {
                        hbar: "\\\\hbar",
                        psi: "\\\\psi",
                        Psi: "\\\\Psi",
                        partial: "\\\\partial",
                        nabla: "\\\\nabla",
                        hat: ["\\\\hat{#1}", 1],
                        vec: ["\\\\vec{#1}", 1]
                    }
                },
                options: {
                    ignoreHtmlClass: 'tex2jax_ignore',
                    processHtmlClass: 'tex2jax_process'
                },
                startup: {
                    ready() {
                        MathJax.startup.defaultReady();
                        MathJax.startup.promise.then(() => {
                            console.log('MathJax loaded successfully');
                        });
                    }
                }
            };
        }
        </script>
        <script type="text/javascript" id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
        """
        display(HTML(mathjax_config))
        
        # Pre-process content to handle old LaTeX notation better
        processed_content = content
        
        # Convert old-style delimiters to new ones for better compatibility
        # Handle display math first (longer patterns)
        processed_content = re.sub(r'\\\[(.*?)\\\]', r'$\1$', processed_content, flags=re.DOTALL)
        # Handle inline math
        processed_content = re.sub(r'\\\((.*?)\\\)', r'$\1

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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
""", processed_content, flags=re.DOTALL)
        
        # Display with MathJax processing and a slight delay to ensure loading
        display(HTML(f'''
        <div class="tex2jax_process" style="font-size: 16px; line-height: 1.6;">
            {processed_content}
        </div>
        <script>
        setTimeout(function() {{
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {{
                MathJax.typesetPromise();
            }}
        }}, 100);
        </script>
        '''))
    else:
        # Regular markdown display
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

def extract_tables(content):
    """
    Extract and enhance markdown tables
    
    Args:
        content (str): Content with potential tables
        
    Returns:
        list: List of table HTML strings
    """
    # Pattern to match markdown tables
    table_pattern = r'(\|.*?\|(?:\r?\n|\r)\|.*?\|(?:(?:\r?\n|\r)\|.*?\|)*)'
    matches = re.findall(table_pattern, content, re.MULTILINE)
    
    enhanced_tables = []
    for match in matches:
        # Convert markdown table to HTML with better styling
        lines = match.strip().split('\n')
        if len(lines) < 2:
            continue
            
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Skip separator line
        if len(lines) < 3:
            continue
            
        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip():
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(row)
        
        # Generate styled HTML table
        table_html = """
        <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
            <thead style="background-color: #f2f2f2;">
                <tr>
        """
        
        for cell in header:
            table_html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>'
        
        table_html += "</tr></thead><tbody>"
        
        for i, row in enumerate(rows):
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            table_html += f'<tr style="background-color: {bg_color};">'
            for cell in row:
                table_html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>'
            table_html += "</tr>"
        
        table_html += "</tbody></table>"
        enhanced_tables.append(table_html)
    
    return enhanced_tables

def display_code_blocks(parsed_response, collapsible=False):
    """
    Extract and display code blocks separately for easy copying
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        collapsible (bool): Whether to make code blocks collapsible
    """
    content = parsed_response.get('message_content', '')
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print("No code blocks found in the response.")
        return
    
    for i, block in enumerate(code_blocks, 1):
        code_display = ""
        
        # Use Code if available, otherwise fall back to HTML with syntax highlighting
        if Code:
            code_display = f'<div id="code-block-{i}"></div>'
        else:
            # Fallback: display as preformatted text with basic styling
            code_display = f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; 
                        border-left: 4px solid #007acc; margin: 10px 0;">
                <pre style="margin: 0; overflow-x: auto;"><code>{block['code']}</code></pre>
            </div>
            """
        
        if collapsible:
            display(HTML(f"""
            <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
                <summary style="cursor: pointer; padding: 10px; background-color: #f0f0f0; 
                               font-weight: bold;">📝 Code Block {i} ({block['language']}) - Click to expand</summary>
                <div style="padding: 10px;">
                    {code_display}
                </div>
            </details>
            """))
        else:
            display(HTML(f"<h4>📝 Code Block {i} ({block['language']})</h4>"))
            display(HTML(code_display))
        
        # Display actual code if using Code class
        if Code:
            display(Code(block['code'], language=block['language']))

def display_enhanced_tables(parsed_response):
    """
    Extract and display enhanced tables
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
    """
    content = parsed_response.get('message_content', '')
    tables = extract_tables(content)
    
    if not tables:
        print("No tables found in the response.")
        return
    
    for i, table_html in enumerate(tables, 1):
        display(HTML(f"<h4>📊 Table {i}</h4>"))
        display(HTML(table_html))

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

def display_grok_analysis(parsed_response, extract_code=True, extract_tables=True, 
                         show_stats=True, collapsible=True):
    """
    Complete analysis and display of Grok response with all enhancements
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        extract_code (bool): Whether to extract and display code blocks separately
        extract_tables (bool): Whether to extract and display tables separately
        show_stats (bool): Whether to show token usage statistics
        collapsible (bool): Whether to make sections collapsible
    """
    
    # Show main response with LaTeX support
    display_grok_response(parsed_response, show_stats=show_stats, collapsible_stats=collapsible)
    
    # Extract and display code blocks
    if extract_code:
        print("\n" + "="*50)
        display(HTML("<h3>🔧 Code Extraction</h3>"))
        display_code_blocks(parsed_response, collapsible=collapsible)
    
    # Extract and display tables
    if extract_tables:
        print("\n" + "="*50)
        display(HTML("<h3>📊 Table Enhancement</h3>"))
        display_enhanced_tables(parsed_response)

def create_comprehensive_display(parsed_response, title="Grok Response Analysis"):
    """
    Create a comprehensive, collapsible display of all response components
    
    Args:
        parsed_response (dict): Parsed response from parse_grok_response()
        title (str): Title for the display
    """
    
    # Main container with collapsible sections
    display(HTML(f"""
    <div style="border: 2px solid #007acc; border-radius: 10px; margin: 20px 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
        <h2 style="text-align: center; color: #007acc; margin: 0; padding: 20px;">
            🤖 {title}
        </h2>
    </div>
    """))
    
    # Stats section (collapsible)
    display_grok_response(parsed_response, show_stats=True, collapsible_stats=True)
    
    # Main content with LaTeX support
    content = parsed_response.get('message_content', '')
    display(HTML("""
    <details open style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
        <summary style="cursor: pointer; padding: 10px; background-color: #e8f4f8; 
                       font-weight: bold; font-size: 16px;">📝 Full Response Content</summary>
        <div style="padding: 10px;">
    """))
    
    display_content_with_latex(content)
    display(HTML("</div></details>"))
    
    # Code blocks (collapsible)
    code_blocks = extract_code_blocks(content)
    if code_blocks:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f0f8e8; 
                           font-weight: bold; font-size: 16px;">🔧 Code Blocks</summary>
            <div style="padding: 10px;">
        """))
        display_code_blocks(parsed_response, collapsible=False)
        display(HTML("</div></details>"))
    
    # Tables (collapsible)
    tables = extract_tables(content)
    if tables:
        display(HTML("""
        <details style="margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <summary style="cursor: pointer; padding: 10px; background-color: #f8f0e8; 
                           font-weight: bold; font-size: 16px;">📊 Enhanced Tables</summary>
            <div style="padding: 10px;">
        """))
        display_enhanced_tables(parsed_response)
        display(HTML("</div></details>"))

# Example usage functions
def fibonacci_test_example():
    """Example of how to use the enhanced helper with your Fibonacci response"""
    
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
    
    # Display with comprehensive analysis
    create_comprehensive_display(fibonacci_response, "Fibonacci Function Analysis")

# Enhanced usage examples
"""
# Basic usage with LaTeX support:
display_grok_response(your_parsed_response)

# Full analysis with collapsible sections:
display_grok_analysis(your_parsed_response, collapsible=True)

# Comprehensive display with all features:
create_comprehensive_display(your_parsed_response, "My Analysis")

# Just extract code for testing:
code = quick_test_code(your_parsed_response)
exec(code)

# Save code to file:
extract_and_save_code(your_parsed_response, "my_code.py")
"""