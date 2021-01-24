import requests
import os
import json
from bs4 import BeautifulSoup


def sendMessage(channelId: str, message: str = "", embed: dict = None):
    if not os.path.exists("config.json"):
        print("config.json not found.")
        exit(1)

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    print("[INFO] sendMessage: {message}".format(message=message))
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot {token}".format(token=config["discord_token"]),
        "User-Agent": "Bot"
    }
    params = {
        "content": message,
        "embed": embed
    }
    response = requests.post(
        "https://discord.com/api/channels/{channelId}/messages".format(channelId=channelId), headers=headers,
        json=params)
    print("[INFO] response: {code}".format(code=response.status_code))
    print("[INFO] response: {message}".format(message=response.text))


def main():
    if not os.path.exists("config.json"):
        print("config.json not found.")
        exit(1)

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    readed = []
    init = True
    if os.path.exists("data.json"):
        print("[INFO] Usual mode")
        init = False
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        readed = data["readed"]
    else:
        print("[INFO] Initialize mode")

    response = requests.get("https://cp.conoha.jp/information.aspx")
    print("[INFO] response: {}".format(response.status_code))
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    newsList = soup.find("dl", {"class": "newsList"})
    news_dd = newsList.findAll("dd")

    for dd in news_dd:
        news_url = dd.find("a").get("href")

        if news_url in readed:
            continue

        print("[INFO] New: {}".format(news_url))
        readed.append(news_url)

        if init:
            continue

        response = requests.post("https://cp.conoha.jp/GetInforMation.aspx", params={
            "mid": news_url[1:]
        })
        response.raise_for_status()
        result = response.json()

        news_category = result.get("category")
        news_categoryClass = result.get("categoryCssClass")
        news_subject = result.get("subject")
        news_date = result.get("date")
        news_body = result.get("body")
        news_body = BeautifulSoup(news_body, "html.parser").text

        embed = {
            "title": news_subject,
            "type": "rich",
            "url": "https://cp.conoha.jp/information.aspx{}".format(news_url),
            "fields": [
                {
                    "name": "Body",
                    "value": "```{}```".format(news_body)
                },
                {
                    "name": "Category",
                    "value": "`{}` ({})".format(news_category, news_categoryClass)
                },
                {
                    "name": "Date",
                    "value": news_date
                }
            ]
        }

        sendMessage(config["discord_channel"], "", embed)

    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "readed": readed
        }))


if __name__ == "__main__":
    if not os.path.exists("config.json"):
        print("config.json not found.")
        exit(1)
    main()
