import ollama
import streamlit as st

# New function for scientific text improvement
def improve_scientific_text(text, model_name = 'gemma3:1b'):
    system_prompt = """
    You are a scientific writing specialist. Enhance text for academic publication with these guidelines:

    1. INPUT/OUTPUT HANDLING
    - If input contains LaTeX commands (e.g., \section, \begin{equation}), 
      preserve LaTeX syntax in output
    - Process LaTeX content contextually (e.g., improve text within equations)
    - Maintain existing LaTeX environments (itemize, align, etc.)
    - Escape special characters in non-LaTeX text

    2. TONE & STYLE
    - Formal academic register (avoid colloquialisms)
    - Third-person perspective preferred
    - Precise technical terminology
    - Nominalization where appropriate
    - Hedging language for claims (e.g., "suggest", "appear to")

    3. STRUCTURE & CLARITY
    - Topic sentences for paragraphs
    - Signposting transitions (However, Consequently)
    - Active/passive voice balance (passive for methods/results)
    - Remove redundant phrases
    - Define acronyms on first use

    4. APA 7TH EDITION COMPLIANCE
    - In-text citations: (Author, Year)
    - Numbers: Words <10, numerals ≥10
    - Statistical formatting: t(24)=3.41, p<.001
    - Measurement units: SI units with spacing (5 mm)
    - Latin terms: e.g., i.e., vs. (proper punctuation)

    5. TECHNICAL PRECISION
    - Discipline-specific terminology
    - Consistent tense usage
    - Appropriate hedging verbs (indicate, demonstrate)
    - Proper article usage (a/an/the)
    - Parallel structure in lists

    6. LaTeX-SPECIFIC ENHANCEMENTS
    - Maintain existing math environments: $...$, \[...\]
    - Preserve bibliographic references: \cite{}, \citet{}
    - Improve text within equations contextually
    - Ensure consistent use of \emph vs \textit
    - Add non-breaking spaces (~) where needed

    Return only improved text without explanations or markdown formatting.
    Maintain original LaTeX structure if present in input. 
    """
    
    try:
        response = ollama.generate(
            model=model_name,
            system=system_prompt,
            prompt=f"Improve this scientific text:\n\n{text}",
            options={
                'temperature': 0.25,
                'top_p': 0.9,
                'num_predict': 512,  # Increased for LaTeX content
                'stop': ["\n\n", "---", "\\end{"]
            }
        )
        
        # Post-processing cleanup
        improved_text = response['response'].strip()
        improved_text = improved_text.replace("**", "")
        improved_text = improved_text.replace("`", "")
        
        return improved_text
         
    except Exception as e:
        st.error(f"Text Enhancement Error: {str(e)}")
        st.error("Common solutions: Check input length, verify model availability, or try simpler phrasing.")
        return None