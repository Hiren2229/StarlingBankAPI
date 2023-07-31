import requests

# Set up the token endpoint URL
token_url = 'https://oauth-sandbox.starlingbank.com/oauth/access-token'

# Set up your client credentials
client_id = '4anzfY6rIa7cDqIflTb6'
client_secret = 'y3AZcTQjT3y9lDVFVaiWuh9Fi6oRKI5z0cTktbbh'

# Set up the redirect URI where the user will be redirected after authorization
redirect_uri = 'http://www.google.com'

# Set up the authorization code
authorization_code = 'YOUR API TOKEN'

# Set up the request payload
data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri
}

# Send the POST request to the token endpoint
response = requests.post(token_url, data=data)
# Process the response
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    print(f"Access Token: {access_token}")
else:
    print("Error:", response.text)
