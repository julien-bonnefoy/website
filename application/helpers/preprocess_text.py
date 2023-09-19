import pandas as pd
from tqdm import trange
from IPython.display import display, HTML
from sklearn.feature_extraction.text import CountVectorizer
from tqdm.notebook import tqdm


def drop_na_values(df, subset=None):
    n_rows_before = df.shape[0]
    for column in subset:
        if column is None:
            print(f'no column specified...drop NA global')
            df.dropna(inplace=True)
        else:
            print(f'dropping NA in “{column}“')
            df.dropna(subset=[column], inplace=True)
            print('\tInitial number of rows: {}'.format(n_rows_before))
            n_rows_after = df.shape[0]
            print('\tnumber of NA rows removed: {}'.format(n_rows_before - n_rows_after))
            print('\tnumber of rows after drop NA : {}'.format(n_rows_after))
            df.reset_index(drop=True, inplace=True)
            print('\tindex reset\n')
    return df


def drop_duplicate_values(df, subset=None, printme=False):
    n_rows_before = df.shape[0]
    if subset is None:
        if printme:
            print(f'no column specified...drop  duplicates')

        df.drop_duplicates(inplace=True)
    else:
        if printme:
            print(f'dropping duplicates in “{subset}“')

        df.drop_duplicates(subset=subset, inplace=True)

    if printme:
        print('\tInitial number of rows: {}'.format(n_rows_before))

    n_rows_after = df.shape[0]

    if printme:
        print('\tnumber of duplicates NA rows removed: {}'.format(n_rows_before - n_rows_after))
        print('\tnumber of rows after drop duplicates : {}'.format(n_rows_after))

    df.reset_index(drop=True, inplace=True)

    if printme:
        print('\tindex reset\n')

    return df


def detect_language(df, column):
    import langid
    df['detected_lang'] = pd.Series(dtype=str)
    for i in trange(len(df)):
        text = df[column][i]
        detected_lang = langid.classify(text)[0]
        df['detected_lang'][i] = detected_lang
    return df[f'{column}']


def remove_not_description(df, column):
    import re
    exp_5 = re.compile("[Dd]emande de formation n°")

    exp_5_list = []

    for index, text in enumerate(df[column]):
        if exp_5.search(text):
            exp_5_list.append(index)

    print(f'Number of rows "Demande de formation n°" : {len(exp_5_list)}')

    df = df.iloc[[index for index in range(df.shape[0]) if index not in exp_5_list]]
    df.reset_index(drop=True, inplace=True)

    exp_6 = re.compile("[Rr][ée]gularisation\s+[cfC]")

    exp_6_list = []

    for index, text in enumerate(df[column]):
        if exp_6.search(text):
            exp_6_list.append(index)

    print(f'Number of rows "Régularisation CPF" : {len(exp_6_list)}')

    df = df.iloc[[index for index in range(df.shape[0]) if index not in exp_6_list]]
    df.reset_index(drop=True, inplace=True)

    return df


def remove_accents(text):
    import re
    # remove accents
    text = re.sub(r'[àâ]', r'a', str(text))
    text = re.sub(r'[ÀÂ]', r'A', str(text))
    text = re.sub(r'[éèêë]', r'e', str(text))
    text = re.sub(r'[ÉÈÊ]', r'E', str(text))
    text = re.sub(r'[îï]', r'i', str(text))
    text = re.sub(r'[Ï]', r'I', str(text))
    text = re.sub(r'[ô]', r'o', str(text))
    text = re.sub(r'[Ô]', r'O', str(text))
    text = re.sub(r'[ûùü]', r'u', str(text))
    text = re.sub(r'[œ]', r'oe', str(text))
    text = re.sub(r'[ç]', r'c', str(text))
    return text


def space_lower_upper(df, column):
    import re
    df[column] = [re.sub(r'([a-z])([A-Z])', r'\g<1> \g<2>', text) for text in df[column]]
    return df


def space_symbol_letter(df, column):
    import re
    df[column] = [re.sub(r'([a-zA-Zœç0-9])([^a-zA-Z\s0-9])', r'\g<1> \g<2>', text) for text in df[column]]
    df[column] = [re.sub(r'([^a-zA-Z\s0-9])([a-zA-Zœç0-9])', r'\g<1> \g<2>', text) for text in df[column]]
    return df


def space_digit_letter(df, column):
    import re
    df[column] = [re.sub(r'([a-zA-Z])([0-9])', r'\g<1> \g<2>', text) for text in df[column]]
    df[column] = [re.sub(r'([0-9])([a-zA-Z])', r'\g<1> \g<2>', text) for text in df[column]]
    return df


def get_top_n_words(corpus, stopwords = [],  n=15):
    vec = CountVectorizer(lowercase=False, ngram_range=(1, 1), stop_words=stopwords).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


def get_top_n2_words(corpus, stopwords = [], n=15):
    vec = CountVectorizer(lowercase=False, ngram_range=(2, 2), stop_words=stopwords).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


def get_stop_words(stop_file_path, print=False):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        # return frozenset(stop_set)
        if print:
            display(HTML("<h5>LOADED</h5>"))
            display(HTML(f'<p>number of stopwords :  <span style="fontSize: 18px; font-weight: bolder; display: inline; line-height: 24px; backgroundColor: #ff7900; color: #fff;">{len(stop_set)}</span></p>'))
        return set(stop_set)


def add_stopwords(STOPWORDS, ADDITIONAL_STOPWORDS):
    '''
    :param STOPWORDS: list of strings
    :param ADDITIONAL_STOPWORDS: other list of strings
    :return: a set of words
    '''
    for word in ADDITIONAL_STOPWORDS:
        STOPWORDS.add(word)
        STOPWORDS = list(STOPWORDS)
        STOPWORDS.sort()
        STOPWORDS = set(STOPWORDS)
    return STOPWORDS


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sentences_topics = pd.DataFrame()

    # Get main topic in each documentpickle
    for i, row in tqdm(enumerate(ldamodel[corpus])):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sentences_topics = sentences_topics.append(pd.Series([str(int(topic_num)), round(prop_topic, 4), topic_keywords]), ignore_index=True)
            else:
                break
    sentences_topics.columns = ['dominant_topic_id', 'topic_contribution_in_document', 'topic_keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sentences_topics = pd.concat([sentences_topics, contents], axis=1)

    return sentences_topics








