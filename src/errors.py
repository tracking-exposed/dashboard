# Custom errors handling
class EmptyDataframeError(Exception):
    pass


def checkId(fbtrexToken):
    token_chars = len(fbtrexToken)
    if (token_chars != 40):
        raise ValueError('the fbtrexToken in configuration should be 40 characters long. This is ' + str(token_chars))


def checkData(data):
    if (data.headers['Content-Type'] != 'application/json; charset=utf-8'):
        raise RuntimeError('Error getting data from API')


def checkDf(df):
    if df.empty or type(df) == 'NoneType':
        raise EmptyDataframeError('Dataframe is empty, are you sure you used the correct token/id?')
