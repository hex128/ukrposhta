import http.client

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'


def make(payload, cookie, referer, csrf_token):
    conn = http.client.HTTPSConnection("ok.ukrposhta.ua")
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': cookie,
        'DNT': '1',
        'Origin': 'https://ok.ukrposhta.ua',
        'Pragma': 'no-cache',
        'Referer': referer,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': UA,
        'X-XSRF-TOKEN': csrf_token,
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    conn.request("POST", "/ajax/lk-api", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    return res.read()
