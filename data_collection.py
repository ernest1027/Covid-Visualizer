import json
import requests
import datetime

response = requests.get("https://api.covid19india.org/v4/min/timeseries.min.json")
raw_json = json.loads(response.text)


def state_index():
    """Assigns a number to each state (alphabetical order by state code)"""
    dict = {}
    count = 0
    for item in raw_json:
        dict[count] = item
        count += 1

    return dict


def confirmed_cases(days_ago=0, index='All'):
    date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    date = date.strftime("%Y-%m-%d")
    results = {}
    print(type(index))

    if index == 'All':
        for key, values in raw_json.items():
            if key == 'UN':
                pass
            else:
                try:
                    results[key] = values['dates'][date]['delta']['confirmed']
                except KeyError:
                    results[key] = 'n/a'

        return results

    elif type(index) == str:
        results[index] = raw_json[index]['dates'][date]['delta']['confirmed']
        return results

    elif type(index) == int:
        results[state_index()[index]] = raw_json[state_index()[index]]['dates'][date]['delta']['confirmed']
        return results


if __name__ == '__main__':
    print(confirmed_cases(index=0))
    print(state_index()[6])


# print(type(raw_json['AN']['dates']['2020-03-26']['delta']['confirmed']))
