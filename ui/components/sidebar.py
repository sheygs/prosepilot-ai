import streamlit as st
from api.hashnode_client import HashnodeClient
from config.settings import OPENAI_API_KEY, HASHNODE_API_KEY, HASHNODE_PUBLICATION_ID

def render_sidebar():
    """Render the sidebar UI"""
    st.sidebar.title("ProsePilot AI")

    # API key input
    api_key = st.sidebar.text_input("Enter OpenAI API Key", value=OPENAI_API_KEY, type="password")

    # Content type selection
    content_type = st.sidebar.selectbox(
        "Select Content Type",
        ["Blog Post", "Tutorial", "Technical Article", "Opinion Piece", "Custom"]
    )

    if content_type == "Custom":
        custom_type = st.sidebar.text_input("Enter custom content type")
        content_type = custom_type if custom_type else "General Content"

    # Model selection
    model = st.sidebar.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4.1"]
    )

    # Temperature slider
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Hashnode connection UI
    render_hashnode_connection()

    # Clear conversation button
    if st.sidebar.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.generated_content = ""
        st.rerun()

    return {
        "api_key": api_key,
        "content_type": content_type,
        "model": model,
        "temperature": temperature
    }

def render_hashnode_connection():
    """Render the Hashnode connection UI in the sidebar"""
    st.sidebar.subheader("Hashnode Settings")

    if st.session_state.hashnode_user_info:
        st.sidebar.success(f"Connected as: {st.session_state.hashnode_user_info.get('name', '')}")
        st.sidebar.write(f"Username: @{st.session_state.hashnode_user_info.get('username', '')}")

        if st.sidebar.button("Disconnect Hashnode"):
            st.session_state.hashnode_user_info = None
            st.session_state.hashnode_api_key = ""
            st.rerun()
    else:
        st.sidebar.write("### Connect to Hashnode")
        st.sidebar.info("Make sure you're using a Personal Access Token from your Hashnode Developer Settings")

        # Hashnode API Key input with expanded help text
        input_hashnode_api_key = st.sidebar.text_input(
            "Enter Hashnode API Key (Personal Access Token)",
            value=st.session_state.hashnode_api_key,
            type="password",
            help="Find this in your Hashnode account > Profile > Developer Settings"
        )

        # Publication ID input - required and masked
        input_hashnode_publication_id = st.sidebar.text_input(
            "Publication ID *",
            value=st.session_state.hashnode_publication_id,
            type="password",
            help="REQUIRED: Enter your Hashnode publication ID. You can find this in your Hashnode dashboard under Publications."
        )

        # Show warning if field is empty
        if not input_hashnode_publication_id:
            st.sidebar.warning("Publication ID is required for publishing. You won't be able to publish without providing this.")

        if st.sidebar.button("Where to find my Publication ID?"):
            st.sidebar.info("""
            **To find your Publication ID:**

            1. Go to your Hashnode dashboard
            2. Click on "Publications" in the sidebar
            3. Select your publication
            4. Look at the URL: https://hashnode.com/dashboard/publications/[YOUR_PUBLICATION_ID]/...
            5. Copy the ID portion from the URL

            Alternatively, connect first and then click "Load My Publications" to select from your publications.
            """)

        # Connect button
        if st.sidebar.button("Connect to Hashnode"):
            st.sidebar.write("Attempting to connect to Hashnode...")

            hashnode_client = HashnodeClient(input_hashnode_api_key)
            user_info = hashnode_client.authenticate()

            if user_info:
                st.session_state.hashnode_user_info = user_info
                st.session_state.hashnode_api_key = input_hashnode_api_key
                st.session_state.hashnode_publication_id = input_hashnode_publication_id
                st.sidebar.success(f"Connected as: {user_info.get('name', '')}")
                st.rerun()
            else:
                st.sidebar.error("Failed to connect to Hashnode. Check your API key and try again.")