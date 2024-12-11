def sort_pharmacies_by_distance(pharmacy_list):
    """Sorts the pharmacy list by distance in ascending order."""
    return sorted(pharmacy_list, key=lambda x: x["distance"])


def load_json_from_file(filename):
    """
    Loads JSON data from a file.

    Args:
        filename (str): The name of the file to load JSON data from.

    Returns:
        dict: The loaded JSON data.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data_json = json.load(f)
    print(f"Loaded JSON data from '{filename}' file.")
    print(f"Data: {data_json}")
    return data_json


def check_json_to_file(json_data, filename1="yesterday.json", filename2="today.json"):
    """
    Save a JSON string to a file.

    Args:
        json_data (str): The JSON data to be saved.
        filename (str, optional): The name of the file to save the data to. Defaults to "data.json".
    """

    global yesterday_json_data
    global today_json_data

    # save_json_to_file(json_data, filename1)
    # save_json_to_file(json_data, filename2)
    # return

    if yesterday_json_data == "":
        yesterday_json_data = load_json_from_file(filename1)

    if today_json_data == "":
        today_json_data = load_json_from_file(filename2)

    if json_data != today_json_data:
        save_json_to_file(today_json_data, filename1)
        yesterday_json_data = today_json_data
        save_json_to_file(json_data, filename2)

