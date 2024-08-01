import csv
import json
import sys
import time

import request
from config import *

for file_name, group_uuid in GROUPS.items():
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)
            flat = row[0].strip()
            full_name = row[1].split(' ')
            last_name = full_name[0].strip()
            first_name = full_name[1].strip()
            if len(full_name) == 3:
                middle_name = full_name[2].strip()
            else:
                middle_name = ""
            phone = row[2]
            obj = {
                "method": "create-letter",
                "obj": {
                    "format": "LETTER_110_X_220",
                    "paymentType": "POSTAGE_STAMP",
                    "withDeliveryNotification": False,
                    "type": "RECOMMENDED",
                    "senderUuid": SENDER_UUID,
                    "subpoena": False,
                    "sms": False,
                    "recipient": {
                        "address": {
                            "postcode": POSTCODE,
                            "region": REGION,
                            "district": DISTRICT,
                            "city": CITY,
                            "street": STREET,
                            "houseNumber": HOUSE_NUMBER,
                            "apartmentNumber": flat,
                            "specialDestination": None,
                            "country": "UA"
                        },
                        "type": "INDIVIDUAL",
                        "firstName": first_name,
                        "lastName": last_name,
                        "middleName": middle_name
                    },
                    "recipientAddress": {},
                    "weight": WEIGHT,
                    "senderAddressId": SENDER_ADDRESS_ID
                },
                "groupUuid": group_uuid
            }
            if phone:
                obj["obj"]["recipient"]["phoneNumber"] = "+" + phone
            payload = json.dumps(obj, ensure_ascii=False)
            print(payload)
            data = request.make(payload, COOKIE, REFERER, CSRF_TOKEN)
            success = False
            try:
                success = "barcode" in json.loads(data)
            except json.decoder.JSONDecodeError:
                success = False
            print(data.decode("utf-8"), file=sys.stdout if success else sys.stderr)
            if not success:
                with open(file_name.replace(".csv", "_failed.csv"), "a+") as failed_csv:
                    csv.writer(failed_csv).writerow(row)
            time.sleep(10)
