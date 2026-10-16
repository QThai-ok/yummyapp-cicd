class GPSSignalLostError(Exception):
    """Ngoại lệ khi không nhận được tín hiệu GPS."""
    pass


def get_current_location():
    """Lấy tọa độ GPS hiện tại (mô phỏng)."""
    return (10.0, 105.0)
