import requests

FLOWISE_URL = "http://localhost:3000/api/v1/prediction/YOUR_FLOW_ID"

def test():
    payload = {
        "question": "Vaccines cause autism"
    }

    r = requests.post(FLOWISE_URL, json=payload, timeout=120)

    print("Status:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    test()
