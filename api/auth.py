import requests


AUTH_URL = "https://connectapi.nubceo.com/authenticate"


def obtener_token(api_key, api_secret):

    body = {
        "API_KEY": api_key,
        "API_SECRET": api_secret
    }


    response = requests.post(
        AUTH_URL,
        json=body
    )


    if response.status_code != 200:
        raise Exception(
            f"Error autenticando: {response.text}"
        )


    data = response.json()


    return data["token"]