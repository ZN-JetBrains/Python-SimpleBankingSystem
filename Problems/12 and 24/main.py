from datetime import datetime


def format_time(datetime_obj):
    time_1 = datetime_obj.strftime("%H:%M")
    time_2 = datetime_obj.strftime("%I:%M")
    print(f"24h {time_1}")
    print(f"12h {time_2}")
