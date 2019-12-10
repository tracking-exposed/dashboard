def generate_wordcloud():  # optionally add: stopwords=STOPWORDS and change the arg below
    df = API.getFacebook(config['token'], apiname='semantics', count=config['amount'], skip=config['skip'])
    text = df.labels.str.join(sep=',').reset_index()
    text.columns = ['date', 'words']
    text = text.words.str.cat(sep=' ')

    wordcloud = WordCloud(font_path='src/fonts/DejaVuSans.ttf',
                          relative_scaling=1.0
                          ).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    if config['name'] != None:
        savepath = tools.uniquePath(config['path'] + '/' + config['name'] + '_labels.svg')
    else:
        savepath = tools.uniquePath(config['path'] + '/' + config['token'] + '_labels.svg')
    plt.savefig(savepath, format='svg')
