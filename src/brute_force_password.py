import itertools

# Define the character set
import string

# Define the word length
import requests

word_length = 3

# Generate all combinations
passwords = [
    "".join(p) for p in itertools.product(string.ascii_lowercase, repeat=word_length)
]

# Print the combinations (not recommended for large word_length)
for password in passwords:
    response = requests.post(
        "http://127.0.0.1:8000/login",
        json={"username": "username", "password": password},
    )
    if response.status_code == 200:
        print(response.json())
        break
