import streamlit as st
from services.extractor import extract_text_from_pdf
from services.ollama_client import query_ollama

st.set_page_config(page_title="SOW Analyzer", layout="wide")

st.title("📄 SOW Upload & Scope Analyzer")

uploaded_file = st.file_uploader("Upload SOW (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("File uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)

    with st.expander("📖 Extracted Text Preview"):
        st.text(text[:3000])

    if st.button("Analyze SOW"):
        with st.spinner("Analyzing..."):

            # prompt = f"""
            #             You are a contract analyst.

            #             Extract:
            #             1. In-scope items
            #             2. Out-of-scope items
            #             3. Deliverables

            #             Return JSON format:

            #             {{
            #             "in_scope": [],
            #             "out_of_scope": [],
            #             "deliverables": []
            #             }}

            #             SOW:
            #             {text[:8000]}
            #         """

            prompt = f"""
SYSTEM ROLE:
You are a senior contract analyst with deep expertise in interpreting Statements of Work (SOWs), identifying scope boundaries, and highlighting ambiguities.

OBJECTIVE:
Carefully read the SOW and explain your understanding of it in a clear, structured way. Focus on accuracy, completeness, and clarity.

Do NOT summarize blindly — interpret the intent of the document like a human analyst.

--------------------------------
ANALYSIS INSTRUCTIONS
--------------------------------

1. Understand the purpose of the engagement
2. Identify what work is explicitly included
3. Identify what is explicitly excluded (if mentioned)
4. Identify key deliverables or outputs
5. Highlight any ambiguity, missing details, or risky wording

--- ASSUMPTIONS / GAPS / RISKS ---
Critically analyze the SOW and highlight:
- Missing details
- Vague language
- Potential areas of dispute
- Implicit assumptions that are not clearly defined

--------------------------------
OUTPUT FORMAT
--------------------------------

--- SUMMARY ---
Explain in 2–4 lines:
- What is this project about?
- What is the objective of the SOW?

--- ASSUMPTIONS / GAPS / RISKS ---
Critically analyze the SOW and highlight:
- Missing details
- Vague language
- Potential areas of dispute
- Implicit assumptions that are not clearly defined

--------------------------------
STRICT RULES
--------------------------------
- Do NOT hallucinate or invent details
- Do NOT assume missing scope as out-of-scope
- Clearly separate facts from interpretation
- If something is unclear, explicitly say so
- Be precise, not verbose

--------------------------------
SOW:
--------------------------------
{text[:8000]}
"""

            result = query_ollama(prompt)

        # st.subheader("🧠 Analysis Output")
        # st.code(result, language="json")

        st.subheader("🧠 LLM Understanding of SOW")
        st.markdown(result)
        st.write(f"📊 Extracted text length: {len(text)} characters")