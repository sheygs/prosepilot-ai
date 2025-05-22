import streamlit as st
from config.settings import HASHNODE_API_KEY, HASHNODE_PUBLICATION_ID


def initialize_session_state():
    """Initialize all session state variables"""
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = ""

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "hashnode_user_info" not in st.session_state:
        st.session_state.hashnode_user_info = None

    if "hashnode_api_key" not in st.session_state:
        st.session_state.hashnode_api_key = HASHNODE_API_KEY

    if "hashnode_publication_id" not in st.session_state:
        st.session_state.hashnode_publication_id = HASHNODE_PUBLICATION_ID

    if "hashnode_publications" not in st.session_state:
        st.session_state.hashnode_publications = []
