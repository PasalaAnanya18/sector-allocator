def allocate_sector(headlines):
    headlines['adj_score'] = headlines['mean_score'].clip(lower=0)
    total_score = headlines['adj_score'].sum()
    if total_score == 0:
        headlines['weights'] = (1.0 / len(headlines))*100
    else:
        headlines['weights'] = (headlines['adj_score'] / total_score)*100
    
    return headlines[['sector', 'weights']].set_index('sector').to_dict()['weights']