def topLabels():
    df = API.getFacebook(config['token'], apiname='semantics', count=config['amount'], skip=config['skip'])
    df = df[['impressionTime', 'labels', 'user']]
    df = tools.setDatetimeIndexFloor(tools.setDatetimeIndex(df), what='d')
    df = df.dropna()
    df = df.drop('impressionTime', axis=1)
    df = df.reset_index()
    df = df.groupby(['impressionTime', 'user']).agg({'labels': 'sum'})
    df['labels_str'] = df['labels'].apply(', '.join)

    count = df.labels_str.str.split(', ', expand=True)
    count = pd.get_dummies(count, prefix='', prefix_sep='')
    count = count.groupby(count.columns, axis=1).sum()

    output = pd.concat([df, count], axis=1)
    output = output.drop(['labels', 'labels_str'], axis=1)
    output = output.stack()
    output = output.replace(0, pd.np.nan).dropna(axis=0, how='any').fillna(0)
    output = output.reset_index()
    output.columns = ['impressionTime', 'user', 'word', 'count']
    if config['name'] != None:
        savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.csv')
    else:
        savepath = tools.uniquePath(config['path'] + '/' + config['token'] + '_labels.csv')
    output.to_csv(savepath, header=True)
