from IPython.display import display, HTML
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from flask_app.helpers.preprocess_text import sort_coo, extract_topn_from_vector


def precompute_tfidf(df, supplier_column, description_column):
    counter = 0
    suppliers = df[supplier_column].value_counts().keys().tolist()
    df.dropna(subset=[description_column], inplace=True)
    df['tfidf_keywords'] = pd.Series(dtype=object)

    for supplier in suppliers:

        if df[description_column][df[supplier_column] == supplier].count() < 20:
            pass

        else:
            try:
                print("\n\n==================== CRUNCHING TFIDF FOR: {} ====================\n".format(supplier))

                supplier_df = df[df[supplier_column] == supplier]

                supplier_df.reset_index(drop=True, inplace=True)

                corpus = [' '.join(vocab.split()) if isinstance(vocab, str) else ' '.join(vocab) for vocab in
                          supplier_df[description_column]]
                loid_list = supplier_df['lo_id'].values

                print(f'number of documents in corpus: {len(supplier_df)}')

                stopwords = ['passes', 'assure', 'effectue', 'nu', 'vis', 'formateur', 'formateurs', 'coop', 'net',
                             'aleas', 'orange',
                             'mn', 'minutes', 'decouvrirez', 'proposees', 'dispensee conjugue', 'coopnet propose',
                             'proposeer',
                             'approprier cadre', 'mn minutes', 'passes professionnels', 'orange missions',
                             'oeuvre orange',
                             'formations coopnet', 'proposees decouvrirez', 'partir comprehension', 'collectivesavoir',
                             'rendez']

                print('removing stopwords')

                cv = CountVectorizer(max_df=0.8, stop_words=stopwords, max_features=10000)
                X = cv.fit_transform(corpus)
                tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
                tfidf_transformer.fit(X)
                # get feature names
                feature_names = cv.get_feature_names()
                print('extracting keywords')
                for i in range(len(corpus)):
                    doc = corpus[i]
                    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
                    sorted_items = sort_coo(tf_idf_vector.tocoo())
                    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
                    c_i = df[df['lo_id'] == loid_list[i]].index[0]
                    df['tfidf_keywords'][c_i] = keywords
                print('done')
                counter += 1

            except:
                print("SOMETHING WENT HORRIBLY WRONG WITH provider: ", supplier)

    display(HTML(f'<h5>computed {counter} providers</h5>'))

    return df
