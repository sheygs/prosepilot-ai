import requests
import streamlit as st
from utils.masking import mask_publication_ids, mask_sensitive_id
from config.settings import HASHNODE_GRAPHQL_URL


class HashnodeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.graphql_url = HASHNODE_GRAPHQL_URL

    def _get_headers(self):
        """Get headers for API requests"""
        return {"Content-Type": "application/json", "Authorization": self.api_key}

    def authenticate(self):
        """Authenticate with Hashnode"""
        if not self.api_key:
            st.error("No Hashnode API key provided")
            return False

        query = """
            query {
                me  {
                    username
                    name
                }
            }
        """

        try:
            response = requests.post(
                self.graphql_url, json={"query": query}, headers=self._get_headers()
            )

            st.write(f"Response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                if "data" in result and "me" in result["data"]:
                    return result["data"]["me"]
                else:
                    st.write("API Response structure:", result)
                    return False
            else:
                st.write(f"API Error Response: {response.text}")
                return False
        except Exception as e:
            st.error(f"Error authenticating with Hashnode: {str(e)}")
            return False

    def get_publications(self):
        """Get user's publications"""
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

        try:
            response = requests.post(
                self.graphql_url, json={"query": query}, headers=self._get_headers()
            )

            if response.status_code == 200:
                result = response.json()

                if (
                    "data" in result
                    and "me" in result["data"]
                    and "publications" in result["data"]["me"]
                ):
                    publications = result["data"]["me"]["publications"]["edges"]

                    publications_list = []

                    for publication in publications:
                        publications_list.append(
                            {
                                "id": publication["node"]["id"],
                                "title": publication["node"]["title"],
                                "isDefault": publication["node"].get(
                                    "isDefault", False
                                ),
                            }
                        )

                    publications_list.sort(
                        key=lambda x: (0 if x["isDefault"] else 1, x["title"])
                    )

                    return publications_list
                else:
                    # Mask sensitive data
                    result_copy = result.copy()
                    mask_publication_ids(result_copy)
                    st.error("Could not retrieve publications structure")

            return None
        except Exception as e:
            st.error(f"Error fetching publications: {str(e)}")
            return None

    def get_tags(self, search_text=""):
        """Get tags matching search text"""
        query = """
            query getTags($page: Int!, $query: String) {
                tagCategories(page: $page, query: $query) {
                    _id
                    name
                    slug
                }
            }
        """

        variables = {"page": 0, "query": search_text}

        try:
            response = requests.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self._get_headers(),
            )

            if response.status_code == 200:
                result = response.json()

                if "data" in result and "tagCategories" in result["data"]:
                    return result["data"]["tagCategories"]

            return []
        except Exception as e:
            st.error(f"Error getting Hashnode tags: {str(e)}")
            return []

    def create_draft(
        self, title, content, tags=None, publication_id=None, subtitle=None
    ):
        """Create a draft post on Hashnode"""
        if not publication_id or not publication_id.strip():
            st.error(
                "Publication ID is required. Please provide a valid publication ID."
            )
            return False

        if tags is None:
            tags = []

        input_vars = {
            "title": title,
            "contentMarkdown": content,
            "tags": tags,
            "publicationId": publication_id,
        }

        if subtitle and subtitle.strip():
            input_vars["subtitle"] = subtitle

        mutation = """
            mutation createDraft($input: CreateDraftInput!) {
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

        try:
            # Create a copy with masked publication ID
            debug_vars = input_vars.copy()

            if "publicationId" in debug_vars:
                debug_vars["publicationId"] = mask_sensitive_id(
                    debug_vars["publicationId"]
                )

            st.write("Sending input variables: ", debug_vars)

            response = requests.post(
                self.graphql_url,
                json={"query": mutation, "variables": {"input": input_vars}},
                headers=self._get_headers(),
            )

            st.write(f"Response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                # Mask sensitive data for display
                result_copy = result.copy()
                mask_publication_ids(result_copy)
                st.write("API response structure:", result_copy)

                if (
                    "data" in result
                    and "createDraft" in result["data"]
                    and "draft" in result["data"]["createDraft"]
                ):
                    return result["data"]["createDraft"]["draft"]

            st.error(f"Error posting to Hashnode: {response.text}")
            return False
        except Exception as e:
            st.error(f"Error posting to Hashnode: {str(e)}")
            return False
