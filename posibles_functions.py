# retrieve data from fithub api
import requests
import json
username = "octocat"  # Replace with the desired GitHub username
api_url = f"https://api.github.com/users/{username}"
headers = {
    "Accept": "application/vnd.github.v3+json",
    # "Authorization": "token YOUR_PERSONAL_ACCESS_TOKEN" # Uncomment and add your token for private data/higher rate limits
}
response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    user_data = response.json()
    print(f"Name: {user_data.get('name')}")
    print(f"Public Repos: {user_data.get('public_repos')}")
    print(f"Followers: {user_data.get('followers')}")
else:
    print(f"Error: {response.status_code} - {response.text}")