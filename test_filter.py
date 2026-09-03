import json
from filter import check_listing


with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


test_listing = {
    "name": "دوو ماتیز",
    "city": "کرج",
    "price": "240 میلیون",
    "year": "1381",
    "mileage": "165 هزار",
    "fuel": "بنزینی",
    "transmission": "دستی",
    "description": "شاسی سالم و پلمپ، موتور و گیربکس سالم"
}


accepted, score, reason = check_listing(test_listing, config)

print("Accepted:", accepted)
print("Score:", score)
print("Reason:", reason)
