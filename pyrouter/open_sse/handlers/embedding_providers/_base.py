def bearer_auth(creds: dict):
    return {"Authorization": f"Bearer {creds.get('apiKey') or creds.get('accessToken')}"}
