import streamlit as st


st.set_page_config(page_title="Student Grade System", page_icon="G", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fa;
        color: #20252b;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .block-container { max-width: 680px; padding-top: 4rem; }
    h1 { color: #20252b !important; letter-spacing: 0 !important; }
    label { color: #20252b !important; font-weight: 600; }
    .stNumberInput input {
        background: #ffffff !important;
        border: 1px solid #cbd3dc !important;
        border-radius: 8px !important;
        color: #20252b !important;
    }
    .result {
        background: #ffffff;
        border-left: 5px solid #bd2338;
        border-radius: 4px;
        box-shadow: 0 3px 12px #20252b12;
        color: #20252b;
        font: 1rem 'Courier New', monospace;
        margin-top: 1.5rem;
        padding: 1.1rem 1.25rem;
    }
    .result-grade { color: #bd2338; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


def calculate_grade(mark: float) -> str:
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "E"


st.title("Student Grade System")

mark = st.number_input(
    "Enter your mark (0-100):",
    min_value=0.0,
    max_value=100.0,
    value=None,
    step=1.0,
    placeholder="Type a mark...",
)

if mark is None:
    st.info("Enter a number between 0 and 100 to calculate the grade.")
else:
    grade = calculate_grade(mark)
    st.markdown(
        f'<div class="result"><div class="result-message">Mark: {mark:g} '
        f'-&gt; <span class="result-grade">Grade: {grade}</span></div></div>',
        unsafe_allow_html=True,
    )
