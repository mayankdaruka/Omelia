import urllib.parse as urlparse
from urllib.parse import parse_qs
url = "https://docs.google.com/spreadsheets/d/1K8n-Bcn9uqcuNXfVG4PA2zgDvNIUG5bUyh54CescYVc/edit?ts=5f944b9b#gid=1457133577"
parsed = urlparse.urlparse(url)
print(parse_qs(parsed.fragment))