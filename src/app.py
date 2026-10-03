
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from anonymizer import PrivacyAnonymizer

st.set_page_config(
    page_title="PrivyNLP",
    page_icon="🔐",
    layout="wide"
)

@st.cache_resource
def load_engine():
    return PrivacyAnonymizer()

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 PrivyNLP")
st.caption("Privacy-Preserving NLP for Sensitive Text")
st.markdown(
    "Detect sensitive information and pseudonymize it "
    "using NLP and rule-based detection."
)

st.divider()

st.subheader("📝 Enter your text")

sample = (
    "Patient Maya Rao (MRN-20481) visited Green Valley "
    "Clinic on 14/09/2026. Email: maya.rao@example.com. "
    "Phone: +91 9876543210."
)

text_input = st.text_area(
    "Enter synthetic healthcare or student text",
    value=sample,
    height=160,
    placeholder="Enter synthetic text here..."
)

if st.button("🔒 Anonymize Text", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        try:
            engine = load_engine()
            anonymized, report = engine.anonymize(text_input)

            st.divider()
            st.subheader("📄 Anonymized Output")

            st.text_area(
                "Processed text",
                value=anonymized,
                height=140
            )

            st.download_button(
                "⬇️ Download Anonymized Text",
                data=anonymized,
                file_name="privynlp_output.txt",
                mime="text/plain"
            )

            st.subheader("🔍 Detected Entities")

            if report.empty:
                st.info("No in-scope entities detected.")
            else:
                st.dataframe(
                    report,
                    use_container_width=True,
                    hide_index=True
                )

                st.metric(
                    "Entities detected",
                    len(report)
                )

                st.subheader("📊 Entity Summary")
                summary = (
                    report.groupby("label")
                    .size()
                    .reset_index(name="Count")
                )

                st.bar_chart(
                    summary.set_index("label")
                )

        except Exception as error:
            st.error(f"Unable to process text: {error}")

st.divider()

st.caption(
    "PrivyNLP | Academic micro-project | "
    "Synthetic data only. This prototype does not "
    "guarantee complete anonymization."
)