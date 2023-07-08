import numpy as np
import pandas as pd
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
import ast

module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'

model = hub.load(module_url)

def embed_text(input):
  return model(input)

def cosine_similarity(target_vector,vectors):
    return 1 - np.arccos(sklearn.metrics.pairwise.cosine_similarity(target_vector,vectors))/np.pi

def find_similar_vectors(target_vector, vectorss, input_len):
    match_items = []
    for i,vectors in enumerate(vectorss):
        sim = cosine_similarity(target_vector,vectors)
        similar_indices = np.where(sim > 0.65)
        len_match = len(set(similar_indices[0]))
        symp_match = set(similar_indices[1])
        sim_match = np.array([sim[i][j] for i in similar_indices[0] for j in similar_indices[1]])
        if len_match  == input_len:
            outdic = {"idx":i,
                      "symptom_idx": symp_match,
                      "symptom_num": len(symp_match),
                      }
            match_items.append(outdic)
    
    return match_items

def get_input_symptom(input,data):
    """# search"""

    input_len = len(input)
    target_vector = np.array(embed_text(input))
    vectors = data['embed'].values

    match_item = find_similar_vectors(target_vector, vectors, input_len)


    """# post process"""

    symptom_idx = [item["symptom_idx"] for item in match_item]
    symptom_num = [item["symptom_num"] for item in match_item]
    idx = [item["idx"] for item in match_item]


    # Convert list of sets to a single list of integers
    int_list = []
    [int_list.extend(list(s)) for s in symptom_idx]
    idx_repos = [x for x, y in zip(idx, symptom_num) for _ in range(y)]
    selected_symp = [data['symptom'][id_val][id_sym] for id_val,id_sym in zip(idx_repos,int_list)]

    embed_sim_data = embed_text(selected_symp)
    cos_sim = cosine_similarity(embed_sim_data, target_vector)
    max_sim = np.max(cos_sim, axis=1)


    max_symp_sim = {}
    # Iterate over the data
    for id_,simV in zip(idx_repos,max_sim):
        # Check if the ID is already in the dictionary
        if id_ in max_symp_sim:
            # Append the name to the existing list
            max_symp_sim[id_]+= simV
        else:
            # Create a new list with the name
            max_symp_sim[id_] = simV


    socre = [v/n for v,n in zip(max_symp_sim.values(),symptom_num)]

    output_dict = {}
    for i,id in enumerate(idx):
        output_dict[id] = {"name":data["name"][id],
                        "th_name":data["th_name"][id],
                            "score":round(socre[i],4)}
    print("...ประมวลผลเสร็จสิ้น...")
    return output_dict

if __name__ == "__main__":
    """# Data loading"""
    # data = pd.read_csv("/home/patiparn/rasa_thainlp/rasatest/actions/sepSymptom.csv")
    # data["symptom"] = data["symptom1"].apply(ast.literal_eval)
    # data['embed'] = [np.array(embed_text(text)) for text in data['symptom']]
    # symptoms = ['ปวดหัว', 'ตัวร้อน']
    # print(get_input_symptom(symptoms,data))