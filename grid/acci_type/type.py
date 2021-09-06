import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def acci_type(acci,data):
        top=31
        my_acci=acci

        data.loc[len(data)] = [my_acci,'None']

        count_vector = CountVectorizer(ngram_range=(1,3))
        c_vector_title = count_vector.fit_transform(data['input'])

        title_c_sim = cosine_similarity(c_vector_title, c_vector_title).argsort()[:,::-1]

        target_type_index = data[data['input'] == my_acci].index.values

        sim_index = title_c_sim[target_type_index, :top].reshape(-1)
        sim_index = sim_index[sim_index != target_type_index]
        result = data.iloc[sim_index]
        best_type = result['output'].value_counts().head(3)
        
        top_3={}
        l=1
        for i in best_type.index:
                top_3[l]=i
                l+=1
        
        return top_3
