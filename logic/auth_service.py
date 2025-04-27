def authenticate(username: str, password: str) -> bool:
    # Hardcoded account
    return username == "admin" and password == "admin"
