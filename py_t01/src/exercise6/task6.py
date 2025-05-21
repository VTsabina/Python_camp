import json


def sortLists(data: dict) -> dict:
    full_list = {"list0": []}
    for item in data.values():
        full_list["list0"].extend(item)
    if full_list["list0"] == []:
        raise ValueError('Your list of movies is empty.')
    try:
        full_list = sorted(full_list["list0"], key=lambda i: i["year"])

    except KeyError:
        raise ValueError(
            'Error with getting a year of some movie. Please, check your data.')
    return full_list


def printJson(full_list: dict) -> None:
    print(json.dumps(full_list, indent=4))


def main():
    try:
        with open("input.txt", "r", encoding='utf-8') as file:
            data = json.load(file)
        printJson(sortLists(data))
    except FileNotFoundError:
        print("No such file or directory.")
    except json.JSONDecodeError:
        print("File is empty or has incorrect json format.")
    except Exception as e:
        print(f"Sorry, something went wrong: {e}")


if __name__ == "__main__":
    main()
# end main
