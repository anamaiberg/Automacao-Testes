def get_current_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def save_screenshot(page, name):
    timestamp = get_current_timestamp()
    page.screenshot(path=f"screenshots/{name}_{timestamp}.png")

