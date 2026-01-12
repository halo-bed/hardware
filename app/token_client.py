import requests

def fetch_device_pubnub_token(backend_base_url: str, device_key: str) -> str:
    url = f"{backend_base_url}/auth/device/pubnub-token"
    resp = requests.post(url, headers={"X-DEVICE-KEY": device_key}, timeout=10)

    if resp.status_code != 200:
        raise RuntimeError(f"Token request failed: {resp.status_code} {resp.text}")

    data = resp.json()
    token = data.get("token")
    if not token:
        raise RuntimeError(f"No token in response: {data}")

    return token

