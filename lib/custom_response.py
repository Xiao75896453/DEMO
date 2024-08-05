def success_response(reason: str | None = None) -> dict:
    return __general_response(is_success=True, reason=reason)

def failed_response(reason: str) -> dict:
    return __general_response(is_success=False, reason=reason)

def __general_response(is_success: bool, reason: str) -> dict:
    return {"success": is_success, "reason": reason}


