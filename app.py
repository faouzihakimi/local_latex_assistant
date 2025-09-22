import streamlit as st
import ollama
from streamlit_markdown import st_markdown
from time import perf_counter

#import custom functions
from utils.bibtex_converter import *
from utils.md_latex_converter import *
from utils.text_improver import *

used_model = 'gemma3:1b'
#Initialize session state variables
if "ollama_initialized" not in st.session_state:
    ollama.pull(used_model)  
    st.session_state.ollama_initialized = True

# Streamlit UI
st.set_page_config(
    page_title="Latex Writing Assistant",
    page_icon="📚",
    layout="centered"
)


st.title("📚 Latex Writing Assistant")
st.caption("Powered by Ollama | "+used_model)

tab1, tab2, tab3 = st.tabs(["BibTeX", "Text Improvement", "Markdown→LaTeX"])

with tab1:
    # Existing BibTeX conversion UI
    with st.expander("💡 Citation examples"):
        st.markdown("""
        *Example 1*:  
         Loh WL. On latin hypercube sampling. Annals of Statistics 24 1996;p. 2058-2080.
        
        *Example 2*:
         A. Altun, “Understanding hypertext in the context of reading on the web,” *Current Issues in Education*, 
         vol. 6, no. 12, July 2005. [Online]. 

        """)
    
    citation_input = st.text_area(
        "Enter citation:",
        placeholder="Paste your citation here...",
        height=150,
        key="citation_input"
    )
    
    if st.button("✨ Convert to BibTeX", type="primary", key="bibtex_button"):
        if citation_input.strip():
            with st.spinner("Generating BibTeX..."):
                start_time = perf_counter()
                bibtex_output = get_bibtex(citation_input, used_model)
                st.session_state.last_inference_time = perf_counter() - start_time
            
            if bibtex_output:
                st.success("Conversion successful!")
                st.code(bibtex_output, language="bibtex")
                
                if "last_inference_time" in st.session_state:
                    st.caption(f"⏱️ Inference time: {st.session_state.last_inference_time:.2f}s")
        else:
            st.warning("Please enter a citation")

with tab2:

    with st.expander("💡 Example"):
            st.text("""
            For this aim, a study of the realizations $x_{A,j}$ such that the code fails and their associated distribution function is performed.         
            """)
    
    text_input = st.text_area(
        "Enter text for improvement:",
        placeholder="Paste your scientific text here...",
        height=200,
        key="text_input"
    )

    
    if st.button("🔬 Improve Text", type="primary", key="improve_button"):

        if text_input.strip():
            with st.spinner("Enhancing text..."):
                start_time = perf_counter()
                improved_text = improve_scientific_text(text_input, used_model)
                st.session_state.last_inference_time = perf_counter() - start_time

            if improved_text:
                st.success("Text improvement complete!")
                st.code(improved_text, language="latex")
        else:
            st.warning("Please enter text to improve")


with tab3:
    # Add AI toggle control
    use_ai = st.toggle(
        "🤖 Enable AI-powered conversion",
        value=False,
        help="Uses Ollama for complex conversions when enabled."
    )
    
    with st.expander("💡 Markdown Examples & Syntax Guide"):
            st.text("""
                    # Time Evolution in Quantum Systems

                        The **time-dependent Schrödinger equation** governs quantum state evolution:

                        $$i\hbar \frac{\partial}{\partial t}\Psi(x,t) = \hat{H}\Psi(x,t)$$

                        For a particle in a potential $V(x)$, the Hamiltonian becomes:

                        $$
                        \hat{H} = -ac{\hbar^2}{2m} \frac{\partial^2}{\partial x^2} + V(x)
                        $$

                        Key features:
                        - First term: Kinetic energy operator
                        - Second term: Potential energy
                        
            """)
            st.warning("⚠️ Only use AI-powered conversion for complex cases.")
    
    md_input = st.text_area(
        "Markdown Input:",
        placeholder="Paste Markdown here...",
        height=200,
        key="md_input"
    )
    
    if st.button("🛠️ Convert to LaTeX", type="primary", key="convert_button"):
        if md_input.strip():
            with st.spinner("Converting..."):
                start_time = perf_counter()
                latex_output = markdown_to_latex(md_input)
                if use_ai:
                    latex_output = get_enhanced_latex(latex_output, used_model) # Modified function
                st.session_state.last_conv_time = perf_counter() - start_time
            st.session_state.latex_output = latex_output
                
            if latex_output:
                st.success("Conversion complete!")
                st.code(latex_output, language="latex")
                
                if "last_conv_time" in st.session_state:
                    st.caption(f"⏱️ Conversion time: {st.session_state.last_conv_time:.2f}s")
        else:
            st.warning("Please enter Markdown text")

# with st.expander("Debug Info"):
#     st.write("Ollama Status:", "✅ Running" if st.session_state.ollama_initialized else "❌ Not Initialized")

