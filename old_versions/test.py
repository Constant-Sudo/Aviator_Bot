import json


# Define data
data = {
    "bets": [
        1.20,
        2.235,
        353.35,
        29.93,
        40.2,
    ],
}


def saveScore(value: float):
    with open('data.json') as data_file:
        data_loaded = json.load(data_file)
    data_loaded['bets'].append(value)
    with open('data.json', 'w') as f:
        json.dump(data_loaded, f, ensure_ascii=False)
    return None


saveScore(float(1.20))