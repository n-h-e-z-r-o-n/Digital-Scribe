import requests

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": f"Bearer sk-wEBf1qTVCMFuZ8tH7J171b4zCdcHIRtKUcGJiNER3pqWavHR",
        "accept": "image/*"
    },
    files={
        "none": ''
    },
    data={
        "prompt": "dog wearing black glasses",
        "output_format": "webp",
    },
)

if response.status_code == 200:
    with open("./lighthouse.webp", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))