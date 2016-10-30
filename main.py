import urllib.request
import re
import json
import time
from bs4 import BeautifulSoup

def save(data, filename):
    with open(filename, "w") as f:
        f.write(json.dumps((data)))


def load(filename):
    try:
        with open(filename) as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        return {
            "already": []
        }
    return data


def request_to_popute(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    return html


def parse_to_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("a", title=re.compile("\[.+\]"))


def find_image_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find("img", alt="comic")
    return res.get("src")


if __name__ == "__main__":
    url = "http://mangalifewin.takeshobo.co.jp/rensai/popute2/"
    save_file = "./popute.json"
    html = request_to_popute(url)
    res = parse_to_links(html)
    saved = load(save_file)
    for r in res:
        title = r.get("title")
        link = r.get("href")
        if not (title in saved and saved[title]["image"] is not None):
            time.sleep(1)
            res = request_to_popute(url)
            image_url = find_image_url(res)
            saved[title] = {
                "url": link,
                "image": image_url,
            }
            saved["already"].append(title)
    save(saved, save_file)
