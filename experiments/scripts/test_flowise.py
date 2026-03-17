import requests

FLOWISE_URL = "http://localhost:3000/api/v1/prediction/1f705796-571c-400c-9e93-f835e4e44c3f"

def test():
    payload = {
        "question": "Vaccines cause autism"
    }

    r = requests.post(FLOWISE_URL, json=payload, timeout=120)

    print("Status:", r.status_code)
    print("JSON:", r.json())

if __name__ == "__main__":
    test()
