import streamlit as st

def render_stream_recommendation(res: dict):
    # Recommended stream heading - centered, gradient, glowing
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="color: #7a8699; font-size: 1rem; margin-bottom: 0.5rem;">Your recommended stream is</p>
            <h1 style="font-size: 3rem; font-weight: 800; margin: 0;
                background: linear-gradient(90deg, #4f9bff, #a06bff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 30px rgba(79,155,255,0.3);">
                {res['recommended_stream']}
            </h1>
        </div>
        """, unsafe_allow_html=True)
    # Justification flashcard
    st.markdown(f"""
        <div style="
        background: rgba(6,93,255,0.08);
        border: 1px solid #2a4a7a;
        border-left: 4px solid #4f9bff;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin: 1rem 0 2rem 0;
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        ">
        <p style="font-size: 0.85rem; font-weight: 700; color: #4f9bff; text-transform: uppercase; 
                  letter-spacing: 0.08em; margin-bottom: 1rem;">Justification</p>
        <p style="font-size: 1.1rem; color: #E6E9EF; line-height: 1.8; margin: 0; white-space: pre-wrap;">{res['justification']}</p>
        </div>
        """, unsafe_allow_html=True)
    # Alternative stream
    if res['alternative_stream'] and res['alternative_stream'] != "null":
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="color: #7a8699; font-size: 0.95rem; margin-bottom: 0.3rem;">You may also consider</p>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #c299ff; margin: 0;">{res['alternative_stream']}</h3>
            </div>
            """, unsafe_allow_html=True)