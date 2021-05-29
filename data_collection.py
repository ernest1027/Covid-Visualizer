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

def get_SIDRV(day, location):
    counts = {'a': {}, 'b': {}}
    counts['a']['susceptible'] =  pop[location]
    counts['b']['susceptible'] =  pop[location]
    for case_type in ['recovered', 'deceased', 'confirmed', 'vaccinated']:
        counts['a'][case_type] = case_day(case_type, time_frame='total', days_ago=day)[location]
        counts['b'][case_type] = case_day(case_type, time_frame='total', days_ago=day+1)[location]
        counts['a']['susceptible'] -= counts['a'][case_type]  
        counts['b']['susceptible'] -= counts['b'][case_type]  
    counts['a']['confirmed'] -= counts['a']['recovered'] + counts['a']['deceased']
    counts['b']['confirmed'] -= counts['b']['recovered'] + counts['b']['deceased']
    return counts
    
def get_vaccinated(location):
    return case_day("vaccinated", time_frame='total')[location]

def get_beta(location):
    avg = 0

    for i in range(14):       

        SIDRV = get_SIDRV(i, location)


        beta = SIDRV['a']['susceptible'] - SIDRV['b']['susceptible']
        beta += SIDRV['a']['vaccinated'] - SIDRV['b']['vaccinated']
        beta *= pop[location]        
        beta /= (SIDRV['b']['susceptible']*SIDRV['b']['confirmed'])
        # print(beta)
        avg -= beta        
    return avg/14


def get_delta(location):
    SIDRV = get_SIDRV(0, location)['a']
    # print(SIDRV)
    return SIDRV['deceased']/(SIDRV['deceased']+SIDRV['recovered'])

if __name__ == '__main__':
    print(get_beta('AP'))
    print(get_delta('AP'))
