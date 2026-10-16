import gps_service


MENU = {
    "pho": 50000,
    "bun": 45000,
    "com": 30000,
}

PROMO_CODES = {
    "GIAM10": {
        "discount": 0.10,
        "min_os": 0,
    },
    "NEW_OS_ONLY": {
        "discount": 0.20,
        "min_os": 15,
    },
}

RESTAURANTS = {
    "10.0,105.0": [
        "Nha hang Pho Ly Quoc Su",
        "Bun cha Huong Lien",
    ],
}


class YummyApp:
    def __init__(self):
        self.network_status = "online"
        self.os_version = 15

    def calculate_order_total(self, cart):
        return sum(MENU[item] * quantity for item, quantity in cart.items())

    def apply_promo_code(self, total, promo_code):
        if self.network_status != "online":
            raise ConnectionError("Khong the ket noi mang.")

        if promo_code not in PROMO_CODES:
            raise ValueError("Ma khuyen mai khong hop le.")

        promo = PROMO_CODES[promo_code]

        if self.os_version < promo["min_os"]:
            raise ValueError("Phien ban he dieu hanh khong duoc ho tro.")

        return int(total * (1 - promo["discount"]))

    def get_nearby_restaurants(self):
        try:
            latitude, longitude = gps_service.get_current_location()
            location_key = f"{latitude},{longitude}"
            return RESTAURANTS.get(location_key, [])
        except gps_service.GPSSignalLostError:
            return "Khong the xac dinh vi tri."
