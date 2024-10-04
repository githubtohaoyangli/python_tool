import requests
url="https://githubtohaoyangli.github.io/info/info.json"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}
r = requests.get(url, headers=headers,verify=False)
latest_version = r.json()["releases"]["release1"]["version"]

print(str(str(latest_version).split(".")[0]+","+str(latest_version).split(".")[1]+","+str(latest_version).split(".")[2]).split(","))