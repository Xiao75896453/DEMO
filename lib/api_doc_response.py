def api_doc_response(example: dict, description: str | None = None) -> dict:
    return {
        "description": description,
        "content": {"application/json": {"examples": example}},
    }
