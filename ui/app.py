import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT
from ui.state.session_state import initialize_session_state
from ui.components.sidebar import render_sidebar
from ui.components.content_generator import render_content_generator, render_conversation_history
from ui.components.publisher import render_publisher


def setup_page() -> None:
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )


def run_app():
    """Main application entry point"""
    # Set up page configuration
    setup_page()

    # Initialize session state
    initialize_session_state()

    # Render sidebar and get user settings
    user_settings = render_sidebar()

    # Render content generator and get generation parameters
    content_params = render_content_generator(
        user_settings["api_key"],
        user_settings["content_type"],
        user_settings["model"],
        user_settings["temperature"]
    )

    # Render the publisher component if content has been generated
    if st.session_state.generated_content:
        render_publisher(content_params["user_prompt"])

    # Render conversation history
    render_conversation_history()

    # Footer
    st.markdown("------")
    st.caption("Made with ❤️ by ProsePilot AI")
