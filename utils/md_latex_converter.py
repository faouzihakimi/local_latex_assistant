import ollama
import textwrap
import re
import streamlit as st

#Usefull tools------------------------------------------------------------------------------------------------

def unicode_to_latex(text: str) -> str:
    """
    Convert Unicode characters to LaTeX equivalents (basic implementation).
    Replace with more comprehensive conversion for production use.
    """
    replacements = {
        '–': '--',
        '—': '---',
        '“': '``',
        '”': "''",
        '‘': '`',
        '’': "'",
        '…': '\\dots',
        '≥': '\\geq',
        '≤': '\\leq',
        '≠': '\\neq',
        '±': '\\pm'
    }
    for unicode_char, latex_cmd in replacements.items():
        text = text.replace(unicode_char, latex_cmd)
    return text

def process_lists(text):
    # Handle unordered lists
    text = re.sub(r'^(\s*)- (.*?)$', r'\1\\item \2', text, flags=re.MULTILINE)
    # Handle ordered lists
    text = re.sub(r'^(\s*)\d+\. (.*?)$', r'\1\\item \2', text, flags=re.MULTILINE)
    return text

def wrap_lists(text):
    # Find all list sections
    list_blocks = re.finditer(
        r'((?:^[ \t]*\\item .*?\n)+)',
        text,
        flags=re.MULTILINE
    )
    
    for match in reversed([m for m in list_blocks]):
        full_match = match.group(1)
        indentation = re.match(r'^(\s*)', full_match).group(1)
        is_ordered = any(line.lstrip().startswith(str(i)) 
                        for i, line in enumerate(full_match.split('\n'), 1) 
                        if line.strip())
        
        env = 'enumerate' if is_ordered else 'itemize'
        replacement = (
            f"{indentation}\\begin{{{env}}}\n"
            f"{full_match}"
            f"{indentation}\\end{{{env}}}\n"
        )
        text = text[:match.start()] + replacement + text[match.end():]
        
    return text





#Main functions------------------------------------------------------------------------------------------

def markdown_to_latex(markdown_text: str) -> str:
    """
    Convert Markdown text to LaTeX format with enhanced list handling.
    Handles unordered lists, ordered lists, nested lists, and mixed content.
    """
    markdown_text = "\n" + markdown_text + "\n" #avoid conversion issue (with lists)
    replacements = [
        # Headers
        (r'^##### (.*?)\n', r'\\subparagraph{\1}\n'),
        (r'^#### (.*?)\n', r'\\paragraph{\1}\n'),
        (r'^### (.*?)\n', r'\\subsubsection{\1}\n'),
        (r'^## (.*?)\n', r'\\subsection{\1}\n'),
        (r'^# (.*?)\n', r'\\section{\1}\n'),
        
        # Text formatting
        (r'\*\*(.*?)\*\*', r'\\textbf{\1}'),
        (r'\*(.*?)\*', r'\\textit{\1}'),
        (r'`(.*?)`', r'\\texttt{\1}'),
        (r'~~(.*?)~~', r'\\sout{\1}'),
        (r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}'),
    ]

    latex_text = markdown_text

    # Process ordered/unordered lists


    # Apply basic replacements
    for pattern, replacement in replacements:
        latex_text = re.sub(pattern, replacement, latex_text, flags=re.MULTILINE)

    # Process lists
    latex_text = process_lists(latex_text)

    # Wrap lists in appropriate environments


    latex_text = wrap_lists(latex_text)

    # Handle nested lists by adjusting indentation
    latex_text = re.sub(
        r'^(\s+)\\begin{(itemize|enumerate)}',
        lambda m: ' ' * (len(m.group(1))//2) + f'\\begin{{{m.group(2)}}}',
        latex_text,
        flags=re.MULTILINE
    )

    return latex_text


def get_enhanced_latex(markdown_text: str, model_name = 'gemma3:1b') -> str:
    """
    Use Ollama to convert Markdown to high-quality LaTeX with context awareness
    """
    system_prompt = textwrap.dedent("""
    You are a LaTeX conversion expert. Complete the Markdown conversion for complex use case:
    
    
    1. TEXT FORMATTING
    - **bold** → \textbf{bold}
    - *italic* → \textit{italic}
    - `code` → \texttt{code}
    - ~~strikethrough~~ → \sout{strikethrough}
    - Links: [text](url) → \href{url}{text}
    
    2. MATH ENVIRONMENTS
    - Block math: $$...$$ → \begin{equation} ... \end{equation}
    - Preserve equation environments
    
    3. SPECIAL CASES
    - Escape special chars: & % $ # _ { } ~ ^ \
    - Convert → to \rightarrow, © to \copyright
    - Smart quotes: “” → ``''
    - Handle tables using tabular environment
    
    
    Only do minimal edits. Return only valid LaTeX code. Never explain your work.
    """)
    
    try:
        response = ollama.generate(
            model=model_name,
            system=system_prompt,
            prompt=f"Convert this Markdown to LaTeX:\n\n{markdown_text}",
            options={
                'temperature': 0.1,
                'top_p': 0.9,
                'num_predict': 1024,
            }
        )
        return response['response'].strip()
    except Exception as e:
        st.error(f"Conversion Error: {str(e)}")
        return None