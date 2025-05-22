import re


def mask_publication_ids(obj) -> None:
    """Recursively mask publication IDs in API responses"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "publicationId" and isinstance(value, str):
                obj[key] = mask_sensitive_id(value)
            elif isinstance(value, (dict, list)):
                mask_publication_ids(value)

    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                mask_publication_ids(item)


def mask_sensitive_id(id_string: str) -> str:
    """Mask a sensitive ID for display"""
    if not id_string or len(id_string) < 8:
        return "****"
    return f"{id_string[:5]}...{id_string[-5:]}" if len(id_string) > 10 else "****"


def mask_api_response(response_text):
    """Mask potentially sensitive IDs in API responses"""
    # Match patterns that look like IDs (hexadecimal or UUID-like)
    id_pattern = r'[0-9a-f]{24}'
    return re.sub(id_pattern, '*****', response_text)
