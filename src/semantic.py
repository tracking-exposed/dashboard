from lib import API, tools
from lib.config import p
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# Configuration
p.add('-a', '--amount', help='amount of entries to fetch from api', default=400)
p.add('--skip', help='amount of entries to skip', default=0)
p.add('--top', help='integer of top labels to get', default=25)
p.add('--no-csv', dest='csv', action='store_false', default=True, help='do not create a csv')
p.add('--wordcloud', dest='wordcloud', action='store_true', default=False, help='generate a wordcloud')
config = vars(p.parse_args())
# Load Data

def generate_wordcloud(text): # optionally add: stopwords=STOPWORDS and change the arg below


    wordcloud = WordCloud(font_path='src/DejaVuSans.ttf',
                          relative_scaling = 1.0
                          ).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.svg')
    plt.savefig(savepath, format='svg')

def topLabels(df, top):

    full_list = []  # list containing all words of all texts
    for label in df.labels.fillna('[]'):  # loop over lists in df
        full_list += label  # append elements of lists to full list
    full_list = [word for word in full_list if len(word) >= 3]
    val_counts = pd.Series(full_list).value_counts().nlargest(top)  # make temporary Series to count
    return val_counts

def main():
    df = API.getDf(config['token'], apiname='semantics', count=config['amount'], skip=config['skip'])
    text = df.labels.str.join(sep=',').reset_index()
    text.columns = ['date', 'words']
    text = text.words.str.cat(sep=' ')

    if config['wordcloud']:
        generate_wordcloud(text)
    if config['csv']:
        savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.csv')
        top_labels = topLabels(df, config['top'])
        top_labels.to_csv(savepath, header=False)
    else:
        print('Top Labels for user '+config['name']+'\n'+df.labels)

if __name__ == '__main__':
    main()