import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(layout="wide", page_title="AI Legal Contract Diff")
st.title("⚖️ AI Legal Contract Diff Analyzer")
st.write("Upload two versions of a contract to identify semantic changes.")

col1, col2 = st.columns(2)

with col1:
    file_v1 = st.file_uploader("Upload Original Contract (V1 PDF)", type=["pdf"])

with col2:
    file_v2 = st.file_uploader("Upload Modified Contract (V2 PDF)", type=["pdf"])

if st.button("Analyze Semantic Differences", type="primary"):
    if file_v1 and file_v2:
        with st.spinner("Analyzing text meaning and matching clauses..."):
            # Prepare files to post to FastAPI backend
            files = {
                "file_v1": (file_v1.name, file_v1.getvalue(), "application/pdf"),
                "file_v2": (file_v2.name, file_v2.getvalue(), "application/pdf")
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/analyze", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    
                    # Display structured data neatly
                    for change in data["changes"]:
                        with st.expander(f"⚠️ {change['clause']} Changes ({change['severity']} Risk)"):
                            c1, c2 = st.columns(2)
                            c1.text_area("Version 1 (Original)", change["v1_text"], height=100)
                            c2.text_area("Version 2 (Modified)", change["v2_text"], height=100)
                            st.info(f"**AI Insight:** {change['analysis']}")
                else:
                    st.error("Error communicating with processing engine.")
            except Exception as e:
                st.error(f"Failed to reach backend service: {e}")
    else:
        st.warning("Please upload both document versions first.")