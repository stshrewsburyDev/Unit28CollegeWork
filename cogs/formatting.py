def seconds_to_timestamp(seconds):
    r = int(seconds)
    d, r = divmod(r, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    return f"{d} day(s) {h} hour(s) {m} minute(s) {s} second(s)"


def make_bar(percentage):
    filled = int((20 / 100) * percentage)
    return f"[{'▰' * filled}{'▱' * (20 - filled)}] {percentage}%"
