from lib import API, tools
from lib.config import p
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

p.add('-s', '--start', help='start date for harmonizer. default is a week ago', default=str(datetime.date.today()-datetime.timedelta(days=7)))
p.add('-e', '--end', help='end date for harmonizer. default is today.', default=str(datetime.date.today()))
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv, creates a json instead')
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--no-labels', dest='labels', action='store_false', default=True, help='do not create a csv with labels')
p.add('--wordcloud', dest='wordcloud', action='store_true', default=False, help='generate a wordcloud')
config = vars(p.parse_args())

def downloadSummary():

        if config['name'] != None:
            path = config['path'] + '/' + config['name'] + '_summary'
        else:
            path = config['path'] + '/' + config['token'] + '_summary'

        df = API.getFacebook(config['token'], 'summary', config['amount'], config['skip'])

        if config['csv']:
            print('Saving CSV to '+path+ '.csv')
            df.to_csv(tools.uniquePath(path + '.csv'), index=False)
        if not config['csv']:
            print('Saving JSON to '+path + '.json')
            df.to_json(tools.uniquePath(path + '.json'))

def generate_wordcloud(): # optionally add: stopwords=STOPWORDS and change the arg below
    df = API.getFacebook(config['token'], apiname='semantics', count=config['amount'], skip=config['skip'])
    text = df.labels.str.join(sep=',').reset_index()
    text.columns = ['date', 'words']
    text = text.words.str.cat(sep=' ')

    wordcloud = WordCloud(font_path='src/fonts/DejaVuSans.ttf',
                          relative_scaling = 1.0
                          ).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    if config['name'] != None:
        savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.svg')
    else:
        savepath = tools.uniquePath(config['path'] + '/' + config['token'] + '_labels.svg')
    plt.savefig(savepath, format='svg')

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
    output.columns = ['impressionTime','user', 'word','count']
    if config['name'] != None:
        savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.csv')
    else:
        savepath = tools.uniquePath(config['path'] + '/' + config['token'] + '_labels.csv')
    output.to_csv(savepath, header=True)


def main():
    downloadSummary()
    if config['wordcloud']:
        generate_wordcloud()
    if config['labels']:
        topLabels()
    else:
        print('Warning: labels csv and wordcloud disabled. Not returning any "semantic" output.')

if __name__ == '__main__':
    main()