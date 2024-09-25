import requests
url = "http://localhost:5000/analyze_sentiment"
files = {'file': open('customer_reviews.xlsx', 'rb')}
response = requests.post(url, files=files)
print(response.json())