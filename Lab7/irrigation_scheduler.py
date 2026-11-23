import math


def _require_text(value, label):
    if not isinstance(value, str):
        raise ValueError("{} must be text".format(label))
    return value


def parse_zone(text):
    text = _require_text(text, "zone")
    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("zone must contain one ':' separator")

    name, area_text = (part.strip() for part in parts)
    if not name or not area_text:
        raise ValueError("zone name and area are required")
    try:
        area = float(area_text)
    except ValueError as error:
        raise ValueError("area must be a number") from error
    if not math.isfinite(area) or area <= 0:
        raise ValueError("area must be a finite positive number")

    return name.title(), area

def moisture_average(readings_csv):
    readings_csv = _require_text(readings_csv, "moisture readings")
    tokens = readings_csv.split(',')
    if any(not token.strip() for token in tokens):
        raise ValueError("moisture readings cannot be empty")
    try:
        values = [int(token.strip()) for token in tokens]
    except ValueError as error:
        raise ValueError("moisture readings must be integers") from error
    if any(value < 0 or value > 100 for value in values):
        raise ValueError("moisture readings must be between 0 and 100")
    return sum(values) // len(values)

def water_needed(text):
    text = _require_text(text, "water calculation")
    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("water calculation must contain one '|' separator")

    plot_text, rain_text = (part.strip() for part in parts)
    if not plot_text or not rain_text:
        raise ValueError("area and rainfall are required")
    try:
        plot = float(plot_text)
        rain = float(rain_text)
    except ValueError as error:
        raise ValueError("area and rainfall must be numbers") from error
    if not math.isfinite(plot) or plot <= 0:
        raise ValueError("area must be a finite positive number")
    if not math.isfinite(rain) or rain < 0:
        raise ValueError("rainfall must be a finite nonnegative number")

    need = plot * 5 - rain
    if not math.isfinite(need):
        raise ValueError("calculated water need must be finite")
    return max(need, 0)

def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result)

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result)

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result)

if __name__ == "__main__":
    main()
