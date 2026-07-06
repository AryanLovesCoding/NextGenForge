import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        /* Ambient background blobs for atmosphere */
        .stApp::before {
            content: "";
            position: fixed;
            top: -10%; left: -10%;
            width: 45%; height: 45%;
            background: radial-gradient(circle, rgba(6,93,255,0.18), transparent 70%);
            filter: blur(60px);
            z-index: 0;
            pointer-events: none;
        }
        .stApp::after {
            content: "";
            position: fixed;
            bottom: -15%; right: -10%;
            width: 50%; height: 50%;
            background: radial-gradient(circle, rgba(160,107,255,0.14), transparent 70%);
            filter: blur(70px);
            z-index: 0;
            pointer-events: none;
        }

        /* Buttons */
        .stButton button {
            white-space: nowrap;
            min-width: 90px;
            border-radius: 10px;
            border: 1px solid #2a3441;
            transition: all 0.25s ease;
        }
        .stButton button:hover {
            border-color: #065dff;
            background-color: #065dff;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(6,93,255,0.4);
        }
        button[kind="primary"] {
            background: linear-gradient(90deg, #065dff, #a06bff) !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(6,93,255,0.35) !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(160,107,255,0.5) !important;
            transform: translateY(-2px);
        }

        /* Slider */
        div[data-baseweb="slider"] [role="slider"] {
            background-color: #FAFAFA !important;
            border: 2px solid #4f9bff;
        }
        /* Unselected/background track - keep original color */
        div[data-baseweb="slider"] > div > div:nth-child(1) {
            background: linear-gradient(90deg, #065dff, #a06bff) !important;
        }
        

        /* Expanders */
        div[data-testid="stExpander"] {
            border-radius: 14px;
            border: 1px solid #2a3441;
            background-color: rgba(22,27,34,0.85);
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="stExpander"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(0,0,0,0.4);
        }

        /* Chat messages */
        div[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 0.6rem;
        }

        /* Headers - unified bold, tight, big look across all pages */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -1px !important;
            font-size: 2.8rem !important;
        }

        .stCaption {
            opacity: 0.7;
        }

        section[data-testid="stSidebar"] {
            background-color: #0b0e14;
            border-right: 1px solid #1E2530;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid #2a3441;
        }

        div[data-testid="column"] {
            background-color: rgba(22,27,34,0.85);
            border-radius: 14px;
            border: 1px solid #2a3441;
            padding: 1.3rem;
            margin: 0 0.4rem;
            transition: transform 0.2s ease;
        }
        div[data-testid="column"]:hover {
            transform: translateY(-3px);
        }
        div[data-testid="column"] h3, div[data-testid="column"] h4 {
            color: #4f9bff;
        }

        /* Fade-in on content blocks */
        div[data-testid="stVerticalBlock"] > div {
            animation: fadeIn 0.45s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
                
        /* Widen the main content area so cards/boxes get more horizontal room */
        .block-container {
            max-width: 1400px !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
    </style>
    """, unsafe_allow_html=True)


def show_loading_bar():
    st.markdown("""
    <div style="
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: #0E1117;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="width: 40%; max-width: 400px; height: 6px; background-color: #1E2530; border-radius: 3px; overflow: hidden;">
            <div style="width: 30%; height: 100%; background: linear-gradient(90deg, #065dff, #a06bff); border-radius: 3px; animation: slide 1.2s infinite ease-in-out;"></div>
        </div>
    </div>
    <style>
    @keyframes slide {
        0% { margin-left: -30%; }
        100% { margin-left: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)


def run_with_loader(fetch_fn, *args):
    """
    Runs fetch_fn(*args) while showing the sliding loading bar.
    On a cache hit the call returns almost instantly, so the loader
    just flashes briefly instead of needing a separate skip-flag.
    """
    loader = st.empty()
    with loader:
        show_loading_bar()
    result = fetch_fn(*args)
    loader.empty()
    return result


def roadmap_card(title, content_html):
    st.markdown(f"""
    <div style="background-color:#161b22; border:1px solid #2a3441; border-radius:12px; padding:1.2rem; min-height:100%;">
        <h4 style="color:#065dff; margin-top:0;">{title}</h4>
        <div style="color:#FAFAFA; font-size:0.9rem; line-height:1.5;">{content_html}</div>
    </div>
    """, unsafe_allow_html=True)

def step_progress(current_step, total_steps=11):
    pct = int((current_step / total_steps) * 100)
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#7a8699; margin-bottom:0.4rem;">
            <span>Step {current_step} of {total_steps}</span>
            <span>{pct}%</span>
        </div>
        <div style="width:100%; height:6px; background-color:#1E2530; border-radius:3px; overflow:hidden;">
            <div style="width:{pct}%; height:100%; background: linear-gradient(90deg, #065dff, #4f9bff); border-radius:3px; transition: width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def gradient_heading(text, size="3rem"):
    st.markdown(f"""
    <h1 style="font-size:{size}; font-weight:800; margin-bottom:0.5rem;
        background: linear-gradient(90deg, #4f9bff, #a06bff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;">
        {text}
    </h1>
    """, unsafe_allow_html=True)


def fade_in_wrapper_css():
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div {
        animation: fadeIn 0.4s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)