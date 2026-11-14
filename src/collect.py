import requests
url = "https://guide.wisc.edu/courses/comp_sci/"
response = requests.get(url)
print(response.status_code)
print(len(response.text))
print(response.text[:500])