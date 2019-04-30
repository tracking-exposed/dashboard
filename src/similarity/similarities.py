import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances

vectorizer = TfidfVectorizer()


# reduces similarities matrix to the ones below threshold
def similars(x, thres):
    #ret = [index for index, value in enumerate(x) if value <= thres and value > 0]
    # yes, we want the identical too, substring also has angle 0!
    ret = [index for index, value in enumerate(x) if value <= thres]
    if len(ret) > 0:
        return ret


# returns n:m matrix of distances every item with every other item
def distance(data):
    X = vectorizer.fit_transform(data.concatenatedText.tolist())
    return pd.DataFrame(data=euclidean_distances(X))



if __name__ == "__main__":
    df = pd.read_csv('fbtrx_onlyEN.csv', nrows=30000)
    dist = distance(df)
    df['similars'] = dist.apply(lambda x: similars(x, 0.5), axis=1)
    df.to_csv('with_similarities3.csv', index=False)



