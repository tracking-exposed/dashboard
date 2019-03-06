from cachetools import cached, TTLCache
import requests
import pandas as pd


cache = TTLCache(maxsize=1, ttl=600) # time to live is 10 mins (except its stored = problem might be here)


# calls api summary and returns a pandas dataframe. this could be generic when APIs are final
@cached(cache)
def getSummary(id):
    url = 'https://facebook.tracking.exposed/api/v1/summary/' + str(id) + '/' + '0'
    print("Accessing summary, ID hidden.")
    data = requests.get(url).json()
    df = pd.DataFrame.from_records(data)
    return df
