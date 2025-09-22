import ollama
import streamlit as st

def extract_section(text):
    try:
        # Find positions
        at_index = text.index('@')   # Start after '@'
        last_brace = text.rindex('}')+1    # Last '}' position
        
        # Extract and return the segment
        return text[at_index:last_brace].strip()
    
    except ValueError:
        return "Required symbols not found"

def get_bibtex(citation, model_name = 'gemma3:1b'):

    try:
        response = ollama.generate(
            model=model_name,
            system= """
            You are an academic assistant that converts citations to precise BibTeX entries. 
            Only output the BibTeX entry, no explanations.
            """,
            prompt=citation,
            options={
                'num_predict': 150,
                'temperature': 0.2,
                'top_p': 0.85
            }
        )
        Bib_citation   = response['response'].strip()
        # Post-processing cleanup
        #cut off the text before "@" and after the last "}"
        Bib_citation = extract_section(Bib_citation)

        return Bib_citation
    except Exception as e:
        st.error(f"Ollama Error: {str(e)}")
        return None