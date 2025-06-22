def typewriter_modern(text):
    import streamlit as st
    st.markdown(f"<h3 style='animation: typing 2s steps(40, end);'>{text}</h3>", unsafe_allow_html=True)
