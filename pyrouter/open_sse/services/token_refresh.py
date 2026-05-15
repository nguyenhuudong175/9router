async def refresh_with_retry(refresh_fn, retries: int, log=None):
    last_error = None
    for _ in range(max(retries, 1)):
        try:
            refreshed = await refresh_fn()
            if refreshed:
                return refreshed
        except Exception as exc:
            last_error = exc
    if log and hasattr(log, "warn") and last_error:
        log.warn("TOKEN", f"refresh failed: {last_error}")
    return None
