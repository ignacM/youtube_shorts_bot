from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    import requests

    cookies = {
        '__cflb': '02DiuEcwseaiqqyPC5q2oCJHbWKXcE97UCrF6HQfL25HV',
        '_ga': 'GA1.2.778537680.1673554490',
        '_gid': 'GA1.2.391192008.1673554490',
        '__gads': 'ID=0469385f04db3f4e-22c308b45dd80063:T=1673554489:RT=1673554489:S=ALNI_MZ1i3Z7_mH2kblY-hR53z5MKlF3Ig',
        '__gpi': 'UID=00000bc035bad535:T=1673554489:RT=1673554489:S=ALNI_Mae0JFewx_zb2VPgpFjcQvNfv5_hA',
        '_gat_UA-3524196-6': '1',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cflb=02DiuEcwseaiqqyPC5q2oCJHbWKXcE97UCrF6HQfL25HV; _ga=GA1.2.778537680.1673554490; _gid=GA1.2.391192008.1673554490; __gads=ID=0469385f04db3f4e-22c308b45dd80063:T=1673554489:RT=1673554489:S=ALNI_MZ1i3Z7_mH2kblY-hR53z5MKlF3Ig; __gpi=UID=00000bc035bad535:T=1673554489:RT=1673554489:S=ALNI_Mae0JFewx_zb2VPgpFjcQvNfv5_hA; _gat_UA-3524196-6=1',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'ckd3dW9j',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)



    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]

    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break


driver = webdriver.Chrome()
# Change the tiktok link
driver.get("https://www.instagram.com/explore/tags/footballskills/")

time.sleep(1)

"""
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if (screen_height) * i > scroll_height:
        break
"""

soup = BeautifulSoup(driver.page_source, "html.parser")
# this class may change, so make sure to inspect the page and find the correct class
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

print(len(videos))
for index, video in enumerate(videos):
    downloadVideo(video.a["href"], index)
    time.sleep(10)