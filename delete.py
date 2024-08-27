import json
import time
import http.client
import sys

import request
from config import *

for item in [
    # "01234567-89ab-cdef-0123-456789abcdef",
]:
    conn = http.client.HTTPSConnection("ok.ukrposhta.ua")
    payload = json.dumps({
        "method": "delete-letter",
        "item": item
    }, ensure_ascii=False)
    print(payload)
    data = request.make(payload, COOKIE, REFERER, CSRF_TOKEN)
    success = False
    try:
        success = json.loads(data).get("code_DeleteShipment", None) == 200
    except json.decoder.JSONDecodeError:
        success = False
    print(data.decode("utf-8"), file=sys.stdout if success else sys.stderr)
    time.sleep(10)
