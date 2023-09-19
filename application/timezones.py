from datetime import datetime
from pytz import timezone
import re
import json


utc_minus_11 = "Pacific/Pago_Pago"
utc_minus_10 = "Pacific/Honolulu"
utc_minus_9 = "Pacific/Gambier"
utc_minus_8 = "America/Anchorage"
utc_minus_7 = "America/Los_Angeles"
utc_minus_6 = "Pacific/Galapagos"
utc_minus_5 = "America/Mexico_City"
utc_minus_4 = "America/New_York"
utc_minus_3 = "America/Santiago"
utc_minus_2 = "America/Noronha"
utc_minus_1 = "Atlantic/Cape_Verde"
utc_0 = "Atlantic/Azores"
utc_plus_1 = "Europe/London"
utc_plus_2 = "Europe/Paris"
utc_plus_3 = "Europe/Moscow"
utc_plus_4 = "Asia/Dubai"
utc_plus_5 = "Asia/Karachi"
utc_plus_6 = "Asia/Dhaka"
utc_plus_7 = "Asia/Jakarta"
utc_plus_8 = "Asia/Hong_Kong"
utc_plus_9 = "Asia/Tokyo"
utc_plus_10 = "Australia/Brisbane"
utc_plus_11 = "Pacific/Noumea"
utc_plus_12 = "Pacific/Wallis"

tzones = (
    utc_minus_11, utc_minus_10, utc_minus_9, utc_minus_8, utc_minus_7, utc_minus_6, utc_minus_5, utc_minus_4,
    utc_minus_3, utc_minus_2, utc_minus_1, utc_0, utc_plus_1, utc_plus_2, utc_plus_3, utc_plus_4, utc_plus_5,
    utc_plus_6, utc_plus_7, utc_plus_8, utc_plus_9, utc_plus_10, utc_plus_11, utc_plus_12
)

clocksIds = [
    "00", "01", "10", "11", "20", "21", "30", "31",
    "02", "03", "12", "13", "22", "23", "32", "33",
    "04", "05", "14", "15", "24", "25", "34", "35"
]

now_utc = datetime.now(timezone('UTC'))

time_dict = {}

for i, tz in enumerate(tzones):
    clockId = clocksIds[i]
    time_dict[clockId] = {}

    regex = re.compile(r".*/(.*)")
    city = re.search(regex, tz).group(1)
    city = re.sub(r"_", " ", city)
    time = now_utc.astimezone(timezone(tz))
    h = time.strftime("%H")
    m = time.strftime("%M")

    time_dict[clockId]["city"] = city
    time_dict[clockId]["h"] = h
    time_dict[clockId]["m"] = m

citiz_clocks_j = json.dumps(time_dict, indent=4)