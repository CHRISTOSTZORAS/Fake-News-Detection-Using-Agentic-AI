import requests

import os
from dotenv import load_dotenv

load_dotenv()
FLOWISE_URL = os.getenv("FLOWISE_URL")
def test():
    payload = {
        "question": "Vaccines cause autism"
    }

    r = requests.post(FLOWISE_URL, json=payload, timeout=120)

    print("Status:", r.status_code)
    print("JSON:", r.json())

if __name__ == "__main__":
    test()
