from lib import API, tools
from lib.config import p
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# Configuration
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
p.add('--wordcloud', dest='wordcloud', action='store_true', default=False, help='generate a wordcloud')
config = vars(p.parse_args())
# Load Data

def generate_wordcloud(df): # optionally add: stopwords=STOPWORDS and change the arg below
    text = df.labels.str.join(sep=',').reset_index()
    text.columns = ['date', 'words']
    text = text.words.str.cat(sep=' ')

    wordcloud = WordCloud(font_path='src/DejaVuSans.ttf',
                          relative_scaling = 1.0
                          ).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.svg')
    plt.savefig(savepath, format='svg')

def topLabels(df):
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

    savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.csv')
    output.to_csv(savepath, header=True)


def main():
    df = API.getDf(config['token'], apiname='semantics', count=config['amount'], skip=config['skip'])

    if config['wordcloud']:
        generate_wordcloud(df)
    if config['csv']:
        topLabels(df)
    else:
        print('Warning: csv and wordcloud disabled. Not returning any output.')

if __name__ == '__main__':
    main()