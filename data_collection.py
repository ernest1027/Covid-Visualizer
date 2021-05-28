import json
import requests
import datetime

response = requests.get("https://api.covid19india.org/v4/min/timeseries.min.json")
raw_json = json.loads(response.text)


def state_index():
    """
    Assigns a number to each state (alphabetical order by state code)
    :return: dictionary of state indexes and their corresponding code
    """
    s_index = {}
    count = 0
    for item in raw_json:
        s_index[count] = item
        count += 1

    return s_index


def cases(case_type, time_frame='delta', days_ago=0, index='All'):
    """
    gets number of cases
    :param case_type: confirmed, recovered, deceased
    :param time_frame: delta for selected day, delta7 for last 7 days, total for cumulative
    :param days_ago: data from x number of days ago
    :param index: specify province (int, str)
    :return: dictionary of province(s) and cas count(s)
    """
    date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    date = date.strftime("%Y-%m-%d")
    results = {}

    if index == 'All':
        for key, values in raw_json.items():
            try:
                results[key] = values['dates'][date][time_frame][case_type]
            except KeyError:
                results[key] = 'n/a'
                return results

        return results

    else:
        if type(index) == str:
            pass
        elif type(index) == int:
            index = state_index()[index]

        try:
            results[index] = raw_json[index]['dates'][date][time_frame][case_type]
            return results
        except KeyError:
            results[index] = 'n/a'
            return results


if __name__ == '__main__':
    print(cases('confirmed', time_frame='delta7', index=1))

# print(type(raw_json['AN']['dates']['2020-03-26']['delta']['confirmed']))
