import streamlit as st

def render_stream_recommendation(res: dict):
    # Recommended stream heading - centered and bold
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="color: var(--color-text-secondary, #A0AEC0); font-size: 1rem; margin-bottom: 0.5rem;">Your recommended stream is</p>
        <h1 style="font-size: 2.5rem; font-weight: 800; color: #4F8BF9; margin: 0;">{res['recommended_stream']}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Justification flashcard
    st.markdown(f"""
    <div style="
    background: #E6F1FB;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin: 1rem 0 2rem 0;
    width: 100%;
    box-sizing: border-box;
    ">
    <p style="font-size: 0.9rem; font-weight: 600; color: #185FA5; text-transform: uppercase; 
              letter-spacing: 0.05em; margin-bottom: 1rem;">Justification</p>
    <p style="font-size: 1.1rem; color: #1a1a1a; line-height: 1.8; margin: 0; white-space: pre-wrap;">{res['justification']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Alternative stream
    if res['alternative_stream']:
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: #A0AEC0; font-size: 0.95rem; margin-bottom: 0.3rem;">You may also consider</p>
            <h3 style="font-size: 1.5rem; font-weight: 700; color: #A78BFA; margin: 0;">{res['alternative_stream']}</h3>
        </div>
        """, unsafe_allow_html=True)
