import streamlit as st
from api.hashnode_client import HashnodeClient
from utils.masking import mask_sensitive_id

def render_publisher(user_prompt):
    """Render the Hashnode publishing UI"""
    if not st.session_state.hashnode_user_info:
        st.info("Connect to Hashnode in the sidebar to enable publishing.")
        return

    st.subheader("Publish to Hashnode")

    # Article details
    title = st.text_input("Article Title", value=f"{user_prompt[:50]}..." if len(user_prompt) > 50 else user_prompt)
    subtitle = st.text_input("Subtitle (optional)")

    # Publication selection
    selected_pub_id = render_publication_selector()

    # Tags selection
    selected_tag_ids = render_tag_selector()

    # Publish button - disabled if no publication ID
    publish_button_disabled = not selected_pub_id

    if publish_button_disabled:
        st.error("Cannot publish without a publication ID. Please enter a publication ID or select one above.")
        st.button("Publish to Hashnode", disabled=True)
    else:
        if st.button("Publish to Hashnode"):
            with st.spinner("Publishing to Hashnode..."):
                hashnode_client = HashnodeClient(st.session_state.hashnode_api_key)
                post_result = hashnode_client.create_draft(
                    title=title,
                    content=st.session_state.generated_content,
                    tags=selected_tag_ids,
                    publication_id=selected_pub_id,
                    subtitle=subtitle
                )

                if post_result:
                    st.success(f"Successfully created draft on Hashnode!")
                    st.write(f"Title: {post_result['title']}")
                    st.write(f"Slug: {post_result['slug']}")

                    # Use updatedAt instead of dateUpdated
                    if 'updatedAt' in post_result:
                        st.write(f"Last updated: {post_result['updatedAt']}")

                    username = st.session_state.hashnode_user_info.get("username")
                    if username:
                        st.write(f"Once published, you can view your post at: https://{username}.hashnode.dev/{post_result['slug']}")
                        st.info("Go to your Hashnode dashboard to publish this draft when ready.")
                else:
                    st.error("Failed to publish to Hashnode. Please check your publication ID and try again.")
                    st.info("Hashnode's API requires a valid publication ID for publishing content.")

def render_publication_selector():
    """Render the publication selection UI and return the selected publication ID"""
    st.write("### Publication Settings")
    st.warning("⚠️ A publication ID is REQUIRED for publishing to Hashnode.")

    # Publication ID input field (required)
    manual_pub_id = st.text_input(
        "Publication ID *",
        value=st.session_state.hashnode_publication_id,
        type="password",
        help="This field is required. You cannot publish without a valid publication ID."
    )

    # Get available publications for selection
    if st.button("Load My Publications"):
        hashnode_client = HashnodeClient(st.session_state.hashnode_api_key)
        publications = hashnode_client.get_publications()
        if publications:
            st.session_state.hashnode_publications = publications
            st.success(f"Found {len(publications)} publications. Select one from the dropdown below.")
        else:
            st.error("Could not retrieve your publications. You must enter a publication ID manually.")

    # Show publication dropdown if we have loaded publications
    selected_pub_id = None
    if "hashnode_publications" in st.session_state and st.session_state.hashnode_publications:
        pub_options = {pub["title"]: pub["id"] for pub in st.session_state.hashnode_publications}
        selected_pub_name = st.selectbox("Select publication", options=list(pub_options.keys()))
        selected_pub_id = pub_options[selected_pub_name]

        # Update the manual input field with the selected ID
        if selected_pub_id != manual_pub_id:
            st.session_state.hashnode_publication_id = selected_pub_id

        # Show masked publication ID
        masked_id = mask_sensitive_id(selected_pub_id)
        st.success(f"Using publication: {selected_pub_name} (ID: {masked_id})")
    else:
        # If no publications loaded, use the manual input
        if manual_pub_id.strip():
            selected_pub_id = manual_pub_id
            masked_id = mask_sensitive_id(selected_pub_id)
            st.write(f"Using publication ID: {masked_id}")
        else:
            st.error("No publication ID provided. You must enter a publication ID or load your publications.")
            selected_pub_id = None

    return selected_pub_id

def render_tag_selector():
    """Render the tag selection UI and return the selected tag IDs"""
    # Get available tags from Hashnode
    tag_search = st.text_input("Search for tags")

    selected_tag_ids = []
    if tag_search:
        hashnode_client = HashnodeClient(st.session_state.hashnode_api_key)
        available_tags = hashnode_client.get_tags(tag_search)
        if available_tags:
            tag_options = {tag["name"]: tag["_id"] for tag in available_tags}
            selected_tags = st.multiselect("Select tags", options=list(tag_options.keys()))
            selected_tag_ids = [tag_options[tag] for tag in selected_tags]
            st.info("You can select up to 5 tags")
        else:
            st.info("No tags found. Try another search term.")

    return selected_tag_ids