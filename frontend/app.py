import streamlit as st
import requests


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="GitHub Code Explainer",
    page_icon="💻",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 35px;
    }

    .info-box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #111827;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        margin-top: 50px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="title">💻 GitHub Code Explainer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Understand any GitHub repository using a locally running AI model.
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Introduction
# -----------------------------

st.markdown(
    """
    <div class="info-box">

    ### 🔍 How it works

    **GitHub Repository → Code Processing → Local LLM → Explanation**

    Enter a public GitHub repository URL below.
    The application clones the repository, extracts relevant source
    code, sends it to the local Qwen 2.5 3B model, and generates
    a simple explanation.

    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# GitHub URL Input
# -----------------------------

st.markdown(
    '<div class="section-title">🔗 Repository</div>',
    unsafe_allow_html=True
)

github_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
    label_visibility="collapsed"
)


# -----------------------------
# Analyze Button
# -----------------------------

if st.button(
    "🚀 Analyze Repository",
    use_container_width=True,
    type="primary"
):

    if not github_url:

        st.warning(
            "Please enter a GitHub repository URL."
        )

    elif "github.com" not in github_url:

        st.error(
            "Please enter a valid GitHub repository URL."
        )

    else:

        with st.spinner(
            "Cloning repository and generating explanation..."
        ):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/explain",
                    json={
                        "github_url": github_url
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Repository analyzed successfully!"
                    )

                    # -----------------------------
                    # Statistics
                    # -----------------------------

                    st.markdown(
                        '<div class="section-title">📊 Analysis Summary</div>',
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Files Analyzed",
                            result["files_analyzed"]
                        )

                    with col2:
                        st.metric(
                            "AI Model",
                            "Qwen 2.5 3B"
                        )

                    # -----------------------------
                    # Explanation
                    # -----------------------------

                    st.markdown(
                        '<div class="section-title">📖 Project Explanation</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        result["explanation"]
                    )

                else:

                    try:
                        error = response.json().get(
                            "detail",
                            "Unknown error"
                        )
                    except Exception:
                        error = response.text

                    st.error(
                        f"❌ Error: {error}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    """
                    ❌ Could not connect to the FastAPI backend.

                    Please make sure the backend server is running.
                    """
                )

            except requests.exceptions.Timeout:

                st.error(
                    """
                    ⏳ The analysis took too long.

                    The repository may be very large.
                    Try a smaller GitHub repository.
                    """
                )

            except Exception as error:

                st.error(
                    f"❌ Something went wrong: {error}"
                )


# -----------------------------
# Footer
# -----------------------------

st.markdown(
    """
    <div class="footer">
    Local GenAI • Qwen 2.5 3B • FastAPI • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)