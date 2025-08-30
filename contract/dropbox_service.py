import os
import requests
from django.conf import settings
import time

API_KEY = settings.DROPBOX_SIGN.get("api_key")
BASE_URL = settings.DROPBOX_SIGN.get("base_url", "https://api.hellosign.com/v3")
CLIENT_ID = settings.DROPBOX_SIGN.get("client_id")

DEFAULT_FILE_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

def Create_Embedded_Signature_Request(
    signer1_name, signer1_email, signer2_name, signer2_email, file_url=None, test_mode=True
):
    if not CLIENT_ID:
        raise RuntimeError(
            "Embedded signing requires DROPBOX_SIGN_CLIENT_ID in .env. "
            "Create an app in Dropbox Sign dashboard (Apps/API) and set DROPBOX_SIGN_CLIENT_ID=<client_id>."
        )

    if not signer1_email:
        signer1_email = f"{signer1_name or 'user'}@example.com"

    data = {
        "client_id": CLIENT_ID,
        "test_mode": "1" if test_mode else "0",
        "signers[0][name]": signer1_name,
        "signers[0][email_address]": signer1_email,
        "signers[1][name]": signer2_name,
        "signers[1][email_address]": signer2_email,
        "file_url[0]": file_url or DEFAULT_FILE_URL,
    }

    url = f"{BASE_URL}/signature_request/create_embedded"
    auth = (API_KEY, "")

    response = None
    for attempt in range(3):
        response = requests.post(url, auth=auth, data=data)
        if response.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        break

    if not response or response.status_code != 200:
        raise RuntimeError(f"Dropbox Sign Error: {response.status_code} => {response.text}")

    resp_json = response.json()
    signature_id = resp_json["signature_request"]["signatures"][0]["signature_id"]

    sign_url_resp = requests.get(
        f"{BASE_URL}/embedded/sign_url/{signature_id}",
        auth=auth
    ).json()

    signing_url = sign_url_resp["embedded"]["sign_url"]

    return resp_json["signature_request"]["signature_request_id"], signing_url
