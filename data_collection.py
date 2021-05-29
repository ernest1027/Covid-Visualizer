import json
import requests
import datetime

response = requests.get("https://api.covid19india.org/v4/min/timeseries.min.json")
raw_json = json.loads(response.text)
with open('population.json') as f:
    pop = json.loads(f.read())


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


def case_day(case_type, time_frame='delta', days_ago=0, index='All'):
    """
    gets number of case on a given day
    :param case_type: confirmed, recovered, deceased, vaccinated
    :param time_frame: delta for selected day, delta7 for last 7 days, total for cumulative
    :param days_ago: data from x number of days ago
    :param index: specify province (int, str)
    :return: dictionary of province(s) and cas count(s)
    """
    date = datetime.datetime.now() - datetime.timedelta(days=days_ago+1)
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


def cases_list(case_type, length, index='All'):
    """
    gets list of historical data
    :param case_type: confirmed, recovered, deceased, vaccinated
    :param length: quantity of historical data (days)
    :param index: specify province (int, str)
    :return: dictionary with state code and list of case numbers
    """
    results = {}
    cases = []

    if type(index) == int:
        index = state_index()[index]

    if index == 'All':
        for state in raw_json:
            for key in raw_json[state]['dates']:
                try:
                    cases.append(raw_json[state]['dates'][key]['delta'][case_type])
                except KeyError:
                    cases.append('n/a')

            results[state] = cases[-length:]
            cases = []
        return results

    else:
        for key in raw_json[index]['dates']:
            try:
                cases.append(raw_json[index]['dates'][key]['delta'][case_type])
            except KeyError:
                cases.append('n/a')

        results[index] = cases[-length:]
        return results


def get_beta():
    avg = 0
    counts = {'d': {}, 'd_1': {}}
    for i in range(14):
        for case_type in ['recovered', 'deceased', 'confirmed', 'vaccinated']:
            counts['d'][case_type] += case_day(case_type, time_frame='total', days_ago=i)['AP']
            counts['d_1'][case_type] += case_day(case_type, time_frame='total', days_ago=i+1)['AP']
        print(counts['d'])

        beta = counts['rm-d'] - counts['rm']
        beta += counts['vaccinated'] - counts['vaccinated-d']
        beta *= pop['AP']
        beta /= pop['AP']

        print(susceptible)


    for i in range(0,14):
        R_1 = case_day('recovered', time_frame='total', days_ago=i+1)['AP']
        R = case_day('recovered', time_frame='total', days_ago=i)['AP']
        D_1 = case_day('deceased', time_frame='total', days_ago=i+1)['AP']
        D = case_day('deceased', time_frame='total', days_ago=i)['AP']
        I_1 = case_day('confirmed', time_frame='total', days_ago=i+1)['AP']
        I = case_day('confirmed', time_frame='total', days_ago=i)['AP']
        V_1 = case_day('vaccinated', time_frame='total', days_ago=i+1)['AP']
        V = case_day('vaccinated', time_frame='total', days_ago=i)['AP']

        S_1 = total_pop-I_1-D_1-R_1-V_1
        S = total_pop-I-D-R-V

        beta = S-S_1
        # print(beta)
        beta += V-V_1
        # print(beta)
        beta *= total_pop
        # print(beta)
        beta /= (S_1*I_1)
        # print(beta)
        avg -= beta
        # print(i, avg)
    return avg/14


def get_delta():
    total_pop = raw_population["AP"]
    avg = 0
    for i in range(0,14):
        R_1 = case_day('recovered', time_frame='total', days_ago=i+1)['AP']
        R = case_day('recovered', time_frame='total', days_ago=i)['AP']
        D_1 = case_day('deceased', time_frame='total', days_ago=i+1)['AP']
        D = case_day('deceased', time_frame='total', days_ago=i)['AP']
        I_1 = case_day('confirmed', time_frame='total', days_ago=i+1)['AP']
        I = case_day('confirmed', time_frame='total', days_ago=i)['AP']
        V_1 = case_day('vaccinated', time_frame='total', days_ago=i+1)['AP']
        V = case_day('vaccinated', time_frame='total', days_ago=i)['AP']

        S_1 = total_pop - I_1 - D_1 - R_1 - V_1
        S = total_pop - I - D - R - V

        beta = S-S_1
        # print(beta)
        beta += V-V_1
        # print(beta)
        beta *= total_pop
        # print(beta)
        beta /= (S_1*I_1)
        # print(beta)
        avg -= beta
        # print(i, avg)
    return avg/14


if __name__ == '__main__':
    # print(case_day('confirmed', time_frame='delta7', index=1))
    # print(cases_list('recovered', 5, 'AP'))
    print(get_beta())