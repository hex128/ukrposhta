import csv
import json
import sys
import time

import request

SENDER_UUID = '01234567-89ab-cdef-0123-456789abcdef'
SENDER_ADDRESS_ID = 123456789
POSTCODE = '012345'
REGION = "Київ"
DISTRICT = "Київ"
CITY = "Київ"
STREET = "вул. Вулиця"
HOUSE_NUMBER = "1"
WEIGHT = 20

COOKIE = ''
REFERER = ''
CSRF_TOKEN = ''


for file_name, group_uuid in {
    '1-100.csv': "01234567-89ab-cdef-0123-456789abcdef",
    '101-200.csv': "11234567-89ab-cdef-0123-456789abcdef",
    '201-300.csv': "21234567-89ab-cdef-0123-456789abcdef",
    '301-400.csv': "31234567-89ab-cdef-0123-456789abcdef",
    '401-441.csv': "41234567-89ab-cdef-0123-456789abcdef",
}.items():
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
            payload = json.dumps({
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
                        "middleName": middle_name,
                        "phoneNumber": "+" + phone
                    },
                    "recipientAddress": {},
                    "weight": WEIGHT,
                    "senderAddressId": SENDER_ADDRESS_ID
                },
                "groupUuid": group_uuid
            }, ensure_ascii=False)
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
