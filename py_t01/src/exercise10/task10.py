def getTime():
    while True:
        try:
            k, time = map(int, input().split())
            if k <= 0 or time <= 0:
                raise ValueError
            return k, time
        except ValueError:
            print('Two positive integers expected, try again.')


def getApparatInput() -> list:
    while True:
        try:
            apparat = input().split()
            if len(apparat) < 3:
                raise ValueError('Not enough data, try again.')
            elif len(apparat) > 3:
                raise ValueError('Extra data given, try again.')
            elif len(apparat[0]) != 4:
                raise ValueError('Wrong year given, try again.')
            try:
                apparat[1] = int(apparat[1])
                apparat[2] = int(apparat[2])
                if apparat[1] < 0 or apparat[2] < 0:
                    raise ValueError
            except:
                raise ValueError(
                    'Only positive integers expected, please, check time and cost data')
            return apparat
        except ValueError as e:
            print(f"Error: {e}")


def getApparats(k: int) -> dict:
    raw_data = [getApparatInput() for _ in range(k)]
    apps = dict()
    for item in raw_data:
        if item[0] not in apps.keys():
            apps[item[0]] = [[int(item[1]), int(item[2])]]
        else:
            apps[item[0]].append([int(item[1]), int(item[2])])
    return apps


def findMinCost(apps: dict, time: int) -> int:
    costs = []
    for year in apps.values():
        costs.extend([year[i][0] + year[j][0] for i in range(len(year) - 1)
                     for j in range(i + 1, len(year)) if year[i][1] + year[j][1] == time])
    return min(costs)


def main():
    k, time = getTime()
    print(findMinCost(getApparats(k), time))


if __name__ == "__main__":
    main()
# end main
