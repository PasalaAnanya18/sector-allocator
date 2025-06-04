def get_sentiment(headlines, analyser):
    labels = {'positive': 1, 'negative': -1, 'neutral': 0}
    mean_scores = []
    mean_labels_words = []
    for random, row in headlines.iterrows():
        try:
            sector_headlines = row['headlines']
    
            results = analyser(sector_headlines)
            score = [res['score'] for res in results]
            label = [labels[res['label'].lower()] for res in results]
            mean_score = sum(score) / len(score)
            mean_label = sum(label) / len(label)
            if mean_label > 0:
                mean_labels_words.append('positive')
            elif mean_label < 0:
                mean_labels_words.append('negative')
            else:
                mean_labels_words.append('neutral')
        except:
            mean_score = 0
        mean_scores.append(mean_score)
    headlines['mean_score'] = mean_scores
    headlines['mean_label'] = mean_labels_words

    return headlines
