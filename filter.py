import re


def normalize(text):
    text = str(text or "").lower()

    replacements = {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ۀ": "ه",
        "ة": "ه",
        "‌": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


def extract_number(text):
    if not text:
        return None

    text = normalize(text)
    text = text.replace(",", "").replace("٬", "")

    match = re.search(r"\d+(?:\.\d+)?", text)

    if match:
        return float(match.group())

    return None


def price_in_toman(value):
    """
    قیمت را به تومان برمی‌گرداند.
    """
    if value is None:
        return None

    value = normalize(str(value))
    number = extract_number(value)

    if number is None:
        return None

    if "میلیون" in value:
        return int(number * 1_000_000)

    return int(number)


def mileage_in_km(value):
    """
    کارکرد را به کیلومتر برمی‌گرداند.
    """
    if value is None:
        return None

    value = normalize(str(value))
    number = extract_number(value)

    if number is None:
        return None

    if "هزار" in value:
        return int(number * 1000)

    return int(number)


def check_listing(listing, config):
    """
    listing باید شامل این فیلدها باشد:

    name
    city
    price
    year
    mileage
    description
    fuel
    transmission
    """

    vehicle_name = normalize(listing.get("name"))
    city = normalize(listing.get("city"))
    description = normalize(listing.get("description"))

    rules = config

    # نام خودرو
    if rules["name"] not in vehicle_name:
        return False, 0, "نام خودرو"

    # شهر
    cities = [normalize(c) for c in rules["cities"]]

    if city not in cities:
        return False, 0, "شهر"

    # مدل
    year = extract_number(listing.get("year"))

    if year is None or year < rules["min_year"]:
        return False, 0, "مدل"

    # قیمت
    price = price_in_toman(listing.get("price"))

    if price is None or price > rules["max_price"]:
        return False, 0, "قیمت"

    # کارکرد
    mileage = mileage_in_km(listing.get("mileage"))

    if mileage is None or mileage > rules["max_mileage"]:
        return False, 0, "کارکرد"

    # سوخت
    fuel = normalize(listing.get("fuel"))

    if rules.get("fuel") and rules["fuel"] not in fuel:
        return False, 0, "سوخت"

    # گیربکس
    transmission = normalize(listing.get("transmission"))

    if rules.get("transmission") and rules["transmission"] not in transmission:
        return False, 0, "گیربکس"

    # کلمات ممنوع
    for word in rules.get("reject_words", []):
        if normalize(word) in description:
            return False, 0, f"کلمه ممنوع: {word}"

    # امتیاز
    score = 50

    if mileage <= 150_000:
        score += 20
    elif mileage <= 180_000:
        score += 10

    if year >= 1382:
        score += 10

    if price <= rules["max_price"] - 20_000_000:
        score += 10

    if "شاسی سالم" in description or "شاسی پلمپ" in description:
        score += 5

    if "بدون رنگ" in description:
        score += 5

    return True, score, "تأیید شد"
