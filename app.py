import streamlit as st
import openai
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY", "")
hashnode_api_key = os.getenv("HASHNODE_API_KEY", "")
hashnode_publication_id = os.getenv("HASHNODE_PUBLICATION_ID", "")

# Set up page configuration
st.set_page_config(page_title="Content AI Agent", layout="wide")

# Initialize session state variables if they don't exist
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "hashnode_user_info" not in st.session_state:
    st.session_state.hashnode_user_info = None
if "hashnode_api_key" not in st.session_state:
    st.session_state.hashnode_api_key = hashnode_api_key
if "hashnode_publication_id" not in st.session_state:
    st.session_state.hashnode_publication_id = hashnode_publication_id
if "hashnode_publications" not in st.session_state:
    st.session_state.hashnode_publications = []


# Function to get user's publications
def get_user_publications(api_key):
    # GraphQL endpoint
    url = "https://gql.hashnode.com/"

    # GraphQL query to get user's publications
    query = """
    query {
        me {
            publications {
                edges {
                    node {
                        id
                        title
                        isDefault
                    }
                }
            }
        }
    }
    """

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    try:
        response = requests.post(
            url,
            json={"query": query},
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()

            if "data" in result and "me" in result["data"] and "publications" in result["data"]["me"]:
                publications = result["data"]["me"]["publications"]["edges"]

                # Convert to a simplified format
                pub_list = []
                for pub in publications:
                    pub_list.append({
                        "id": pub["node"]["id"],
                        "title": pub["node"]["title"],
                        "isDefault": pub["node"].get("isDefault", False)
                    })

                # Sort so default is first
                pub_list.sort(key=lambda x: (0 if x["isDefault"] else 1, x["title"]))

                if pub_list:
                    return pub_list
                else:
                    st.warning("No publications found for your account. Please create a publication on Hashnode first.")
            else:
                # Mask any potentially sensitive data in the response
                result_copy = result.copy()
                mask_publication_ids(result_copy)
                st.error("Could not retrieve publications data structure. See response:", result_copy)
        else:
            # Mask any sensitive data in error response
            error_text = response.text
            # Simple masking of any ID-like strings
            import re
            error_text = re.sub(r'[0-9a-f]{24}', '*****', error_text)
            st.error(f"Error fetching publications: {error_text}")

        return None
    except Exception as e:
        st.error(f"Error fetching publications: {str(e)}")
        return None

# Function to authenticate with Hashnode
def authenticate_hashnode(api_key, endpoint="https://gql.hashnode.com/", with_bearer=False):
    if not api_key:
        st.error("No Hashnode API key provided")
        return False

    # GraphQL query to get user information - simplified to just basic info
    query = """
    query {
        me {
            username
            name
        }
    }
    """

    # Determine Authorization header
    auth_header = f"Bearer {api_key}" if with_bearer else api_key

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header
    }

    # Make the request
    try:
        response = requests.post(endpoint, json={"query": query}, headers=headers)

        # Debug info - will display in the app
        st.write(f"Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            # Debug info
            st.write("Response received. Checking data structure...")

            if "data" in result and "me" in result["data"]:
                st.session_state.hashnode_user_info = result["data"]["me"]
                st.session_state.hashnode_api_key = api_key
                return True
            else:
                # Show the actual response for debugging
                st.write("API Response structure:", result)
                return False
        else:
            # Show the error response
            st.write(f"API Error Response: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error authenticating with Hashnode: {str(e)}")
        return False

# Function to post content to Hashnode
def post_to_hashnode(title, content, tags=None, publication_id=None, subtitle=None, is_draft=True):
    if not st.session_state.hashnode_user_info:
        st.error("Not authenticated with Hashnode")
        return False

    # Check if publication_id is provided - it's required
    if not publication_id or not publication_id.strip():
        st.error("Publication ID is required. Please provide a valid publication ID.")
        return False

    api_key = st.session_state.hashnode_api_key

    if tags is None:
        tags = []

    # Create input variables with required publicationId
    input_vars = {
        "title": title,
        "contentMarkdown": content,
        "tags": tags,
        "publicationId": publication_id  # This is required and cannot be null
    }

    # Only add subtitle if it's provided and not empty
    if subtitle and subtitle.strip():
        input_vars["subtitle"] = subtitle

    # GraphQL endpoint
    url = "https://gql.hashnode.com/"

    # GraphQL mutation to create a draft
    mutation = """
    mutation createDraft($input: CreateDraftInput!){
        createDraft(input: $input) {
            draft {
                id
                title
                slug
                updatedAt
            }
        }
    }
    """

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    # Make the request
    try:
        # Show what we're sending for debugging (with masked publication ID)
        debug_vars = input_vars.copy()
        if "publicationId" in debug_vars:
            pub_id = debug_vars["publicationId"]
            debug_vars["publicationId"] = f"{pub_id[:5]}...{pub_id[-5:]}" if len(pub_id) > 10 else "****"
        st.write("Sending input variables:", debug_vars)

        response = requests.post(
            url,
            json={"query": mutation, "variables": {"input": input_vars}},
            headers=headers
        )

        # Debug response for inspection
        st.write(f"Response status: {response.status_code}")
        if response.status_code != 200:
            st.write(f"Error response: {response.text}")

        if response.status_code == 200:
            result = response.json()

            # Mask publication ID in debug output to protect privacy
            if "data" in result and isinstance(result["data"], dict):
                result_copy = result.copy()
                # Recursively search and mask any publication IDs in the response
                mask_publication_ids(result_copy)
                st.write("API response structure:", result_copy)
            else:
                st.write("API response structure:", result)

            if "data" in result and "createDraft" in result["data"] and "draft" in result["data"]["createDraft"]:
                return result["data"]["createDraft"]["draft"]

        st.error(f"Error posting to Hashnode: {response.text}")
        return False
    except Exception as e:
        st.error(f"Error posting to Hashnode: {str(e)}")
        return False

# Helper function to mask publication IDs in response
def mask_publication_ids(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "publicationId" and isinstance(value, str):
                obj[key] = f"{value[:5]}...{value[-5:]}" if len(value) > 10 else "****"
            elif isinstance(value, (dict, list)):
                mask_publication_ids(value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                mask_publication_ids(item)


# Function to get user's default publication ID
def get_default_publication_id(api_key):
    # GraphQL endpoint
    url = "https://gql.hashnode.com/"

    # GraphQL query to get user's publications
    query = """
    query {
        me {
            username
            publications {
                edges {
                    node {
                        id
                        title
                        isDefault
                    }
                }
            }
        }
    }
    """

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    try:
        response = requests.post(
            url,
            json={"query": query},
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()

            # Debug output
            st.write("Publications response:", result)

            if "data" in result and "me" in result["data"] and "publications" in result["data"]["me"]:
                publications = result["data"]["me"]["publications"]["edges"]

                # First, try to find the default publication
                for pub in publications:
                    if pub["node"].get("isDefault", False):
                        return pub["node"]["id"]

                # If no default, just return the first one
                if publications:
                    return publications[0]["node"]["id"]

            st.warning("No publications found for your account. Please create a publication on Hashnode first.")
        else:
            st.error(f"Error fetching publications: {response.text}")

        return None
    except Exception as e:
        st.error(f"Error fetching publications: {str(e)}")
        return None

# Function to get Hashnode tags
def get_hashnode_tags(search_text=""):
    if not st.session_state.hashnode_api_key:
        return []

    api_key = st.session_state.hashnode_api_key

    # GraphQL endpoint
    url = "https://gql.hashnode.com/"

    # Updated GraphQL query to search for tags
    query = """
    query getTags($page: Int!, $query: String) {
        tagCategories(page: $page, query: $query) {
            _id
            name
            slug
        }
    }
    """

    # Variables for the query - updated to use 'query' instead of 'searchText'
    variables = {
        "page": 0,
        "query": search_text
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    # Make the request
    try:
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            if "data" in result and "tagCategories" in result["data"]:
                return result["data"]["tagCategories"]
            else:
                st.write("Tag response structure:", result)
        return []
    except Exception as e:
        st.error(f"Error getting Hashnode tags: {str(e)}")
        return []

# Function to call OpenAI API
def generate_content(api_key, prompt, content_type, tone, max_length, model, temperature):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."

    try:
        openai.api_key = api_key

        system_message = f"""You are an expert content creator specialized in creating {content_type}s.
        Create content with a {tone.lower()} tone.
        Keep the content under {max_length} words.
        Format the content in Markdown.
        Focus on quality, engagement, and relevance."""

        full_prompt = f"Create a {content_type} about: {prompt}"

        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": full_prompt}
            ],
            temperature=temperature,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating content: {str(e)}"

# Sidebar for API configuration
with st.sidebar:
    st.title("Content AI Agent")
    api_key = st.text_input("Enter OpenAI API Key", value=openai_api_key, type="password")

    # Content type selection
    content_type = st.selectbox(
        "Select Content Type",
        ["Blog Post", "Tutorial", "Technical Article", "Opinion Piece", "Custom"]
    )

    if content_type == "Custom":
        custom_type = st.text_input("Enter custom content type")
        content_type = custom_type if custom_type else "General Content"

    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4.1"]
    )

    # Temperature slider
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    st.subheader("Hashnode Settings")

    # Hashnode connection
    if st.session_state.hashnode_user_info:
        st.success(f"Connected as: {st.session_state.hashnode_user_info.get('name', '')}")
        st.write(f"Username: @{st.session_state.hashnode_user_info.get('username', '')}")

        if st.button("Disconnect Hashnode"):
            st.session_state.hashnode_user_info = None
            st.session_state.hashnode_api_key = ""
            st.rerun()
    else:
        st.write("### Connect to Hashnode")
        st.info("Make sure you're using a Personal Access Token from your Hashnode Developer Settings")

        # Hashnode API Key input with expanded help text
        input_hashnode_api_key = st.text_input(
            "Enter Hashnode API Key (Personal Access Token)",
            value=st.session_state.hashnode_api_key,
            type="password",
            help="Find this in your Hashnode account > Profile > Developer Settings"
        )

        # Publication ID input - required and masked
        input_hashnode_publication_id = st.text_input(
            "Publication ID *",
            value=st.session_state.hashnode_publication_id,
            type="password",
            help="REQUIRED: Enter your Hashnode publication ID. You can find this in your Hashnode dashboard under Publications, or use the Load My Publications button after connecting."
        )

        # Show warning if field is empty
        if not input_hashnode_publication_id:
            st.warning("Publication ID is required for publishing. You won't be able to publish without providing this.")

        if st.button("Where to find my Publication ID?"):
            st.info("""
            **To find your Publication ID:**

            1. Go to your Hashnode dashboard
            2. Click on "Publications" in the sidebar
            3. Select your publication
            4. Look at the URL: https://hashnode.com/dashboard/publications/[YOUR_PUBLICATION_ID]/...
            5. Copy the ID portion from the URL

            Alternatively, connect first and then click "Load My Publications" to select from your publications.
            """)

        # Advanced options expander
        with st.expander("Advanced Connection Options"):
            test_mode = st.checkbox("Enable Debug Mode", value=True)
            token_format = st.radio("Token Format", ["Plain Token", "Bearer Token"], index=0,
                                  help="Hashnode API now uses plain token for authentication")
            endpoint_url = st.radio("API Endpoint", ["gql.hashnode.com", "api.hashnode.com"], index=0,
                                  help="Hashnode has moved to gql.hashnode.com")

        # Connection button with more info
        if st.button("Connect to Hashnode"):
            st.write("Attempting to connect to Hashnode...")

            # Store publication ID
            st.session_state.hashnode_publication_id = input_hashnode_publication_id

            # If using test mode, display masked token and try different combinations
            if test_mode:
                masked_token = input_hashnode_api_key[:5] + "..." + input_hashnode_api_key[-5:] if len(input_hashnode_api_key) > 10 else "***"
                st.write(f"Using token: {masked_token}")
                st.write(f"Token format: {'Bearer' if token_format == 'Bearer Token' else 'Plain'}")

                # First attempt with selected endpoint and format
                first_endpoint = f"https://{endpoint_url}/"
                st.write(f"Trying endpoint: {first_endpoint}")

                with_bearer = token_format == "Bearer Token"
                if authenticate_hashnode(input_hashnode_api_key, first_endpoint, with_bearer):
                    st.success(f"Connected to Hashnode as: {st.session_state.hashnode_user_info.get('name', '')}")
                    st.rerun()
                else:
                    st.warning("First attempt failed, trying alternative format...")

                    # Try alternative format with same endpoint
                    with_bearer = not with_bearer
                    if authenticate_hashnode(input_hashnode_api_key, first_endpoint, with_bearer):
                        st.success(f"Connected to Hashnode with alternative token format!")
                        st.rerun()
                    else:
                        st.warning("Second attempt failed, trying alternative endpoint...")

                        # Try alternative endpoint with original format
                        second_endpoint = f"https://{'api' if endpoint_url == 'gql.hashnode.com' else 'gql'}.hashnode.com/"
                        st.write(f"Trying endpoint: {second_endpoint}")

                        with_bearer = token_format == "Bearer Token"
                        if authenticate_hashnode(input_hashnode_api_key, second_endpoint, with_bearer):
                            st.success(f"Connected to Hashnode with alternative endpoint!")
                            st.rerun()
                        else:
                            st.warning("Third attempt failed, trying last combination...")

                            # Try alternative endpoint with alternative format
                            with_bearer = not with_bearer
                            if authenticate_hashnode(input_hashnode_api_key, second_endpoint, with_bearer):
                                st.success(f"Connected to Hashnode with alternative endpoint and token format!")
                                st.rerun()
                            else:
                                st.error("All connection attempts failed. Please check your API key and try again.")
            else:
                # Normal authentication - try with plain token at gql.hashnode.com
                if authenticate_hashnode(input_hashnode_api_key, "https://gql.hashnode.com/", False):
                    st.success(f"Connected to Hashnode as: {st.session_state.hashnode_user_info.get('name', '')}")
                    st.rerun()
                else:
                    st.error("Failed to connect to Hashnode. Enable Debug Mode for more details.")

    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.generated_content = ""
        st.rerun()

# Main app interface
st.title("Content Generator AI Agent")

# Input section
prompt_col1, prompt_col2 = st.columns([3, 1])

with prompt_col1:
    user_prompt = st.text_area("What content would you like to generate?", height=100)

with prompt_col2:
    st.write("Content Parameters")
    tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic", "Informative", "Technical"])
    max_length = st.number_input("Max Words", min_value=50, max_value=2000, value=500, step=50)

# Generate button
generate_pressed = st.button("Generate Content")

# Generate content when the button is pressed
if generate_pressed and user_prompt:
    with st.spinner("Generating content..."):
        generated_text = generate_content(api_key, user_prompt, content_type, tone, max_length, model, temperature)
        st.session_state.generated_content = generated_text

        # Add to conversation history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.conversation_history.append({
            "timestamp": timestamp,
            "prompt": user_prompt,
            "content_type": content_type,
            "tone": tone,
            "response": generated_text
        })

# Display generated content
if st.session_state.generated_content:
    st.subheader("Generated Content")
    st.markdown(st.session_state.generated_content)

    # Actions row
    col1, col2, col3 = st.columns(3)

    with col1:
        # Copy button
        st.button("Copy to Clipboard", help="Copy the generated content to clipboard")

    with col2:
        # Export as TXT
        st.download_button(
            label="Download as TXT",
            data=st.session_state.generated_content,
            file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    with col3:
        # Export as MD
        st.download_button(
            label="Download as MD",
            data=st.session_state.generated_content,
            file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

    # Publishing options
    if st.session_state.hashnode_user_info:
        st.subheader("Publish to Hashnode")

        # Article details
        title = st.text_input("Article Title", value=f"{content_type}: {user_prompt[:50]}..." if len(user_prompt) > 50 else user_prompt)
        subtitle = st.text_input("Subtitle (optional)")

        # Get available tags from Hashnode
        tag_search = st.text_input("Search for tags")
        if tag_search:
            available_tags = get_hashnode_tags(tag_search)
            if available_tags:
                tag_options = {tag["name"]: tag["_id"] for tag in available_tags}
                selected_tags = st.multiselect("Select tags", options=list(tag_options.keys()))
                selected_tag_ids = [tag_options[tag] for tag in selected_tags]
                st.info("You can select up to 5 tags")
            else:
                st.info("No tags found. Try another search term.")
                selected_tag_ids = []
        else:
            selected_tag_ids = []

        # Remove Draft/Published option since Hashnode API has changed
        # Now we can only create drafts, which must be published from Hashnode dashboard
        st.info("Note: Content will be created as a draft. You can publish it from your Hashnode dashboard.")
        is_draft = True  # Always draft with new API

        # Publication selection
        st.write("### Publication Settings")
        st.warning("⚠️ A publication ID is REQUIRED for publishing to Hashnode.")

        # Publication ID input field (required) - masked for privacy
        manual_pub_id = st.text_input(
            "Publication ID *",
            value=st.session_state.hashnode_publication_id,
            type="password",  # Mask the input
            help="This field is required. You cannot publish without a valid publication ID."
        )

        # Get available publications for selection
        if st.button("Load My Publications"):
            publications = get_user_publications(st.session_state.hashnode_api_key)
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
                manual_pub_id = selected_pub_id
                st.session_state.hashnode_publication_id = selected_pub_id

            # Show confirmation without revealing the full ID
            masked_id = f"{selected_pub_id[:5]}...{selected_pub_id[-5:]}" if len(selected_pub_id) > 10 else "****"
            st.success(f"Using publication: {selected_pub_name} (ID: {masked_id})")
        else:
            # If no publications loaded, use the manual input
            if manual_pub_id.strip():
                selected_pub_id = manual_pub_id
                # Show confirmation without revealing the full ID
                masked_id = f"{selected_pub_id[:5]}...{selected_pub_id[-5:]}" if len(selected_pub_id) > 10 else "****"
                st.write(f"Using publication ID: {masked_id}")
            else:
                st.error("No publication ID provided. You must enter a publication ID or load your publications.")
                selected_pub_id = None  # Make it explicit that we don't have a valid ID

        # Publish button - disabled if no publication ID
        publish_button_disabled = not selected_pub_id

        if publish_button_disabled:
            st.error("Cannot publish without a publication ID. Please enter a publication ID or select one above.")
            st.button("Publish to Hashnode", disabled=True)
        else:
            if st.button("Publish to Hashnode"):
                with st.spinner("Publishing to Hashnode..."):
                    post_result = post_to_hashnode(
                        title=title,
                        content=st.session_state.generated_content,
                        tags=selected_tag_ids,
                        publication_id=selected_pub_id,
                        subtitle=subtitle,
                        is_draft=True  # Always draft with new API
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

# Display conversation history
if st.session_state.conversation_history:
    with st.expander("Conversation History", expanded=False):
        for i, exchange in enumerate(reversed(st.session_state.conversation_history)):
            st.write(f"**[{exchange['timestamp']}] {exchange['content_type']} ({exchange['tone']})**")
            st.write(f"Prompt: {exchange['prompt']}")
            st.write("Response:")
            st.markdown(exchange['response'])
            st.divider()

# Footer
st.markdown("---")
st.caption("Content AI Agent - Created with Streamlit and OpenAI")
