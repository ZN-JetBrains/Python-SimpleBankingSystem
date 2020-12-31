from datetime import datetime


def get_release_date(release_str):
    processed_str = release_str.split(":")[1].strip()
    return datetime.strptime(processed_str, "%d %B %Y")
