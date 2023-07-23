import numpy as np
import pandas as pd
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
import json

class SymptomSearcher:
    def __init__(self, data_path, module_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"):
        self.module_url = module_url
        self.data = pd.read_csv(data_path)
        self.data["symptom"] = self.data["symptom"].apply(json.loads)
        self.data["embed"] = self.data["embed"].apply(json.loads)
        self.data["embed"] = self.data["embed"].apply(np.array)
        self.model = hub.load(module_url)
        self.embedded_data = self.data['embed'].values

    def embed_text(self, input):
        return self.model(input)

    def cosine_similarity(self, target_vector, vectors):
        return 1 - np.arccos(sklearn.metrics.pairwise.cosine_similarity(target_vector, vectors)) / np.pi

    def find_similar_vectors(self, target_vector, input_len):
        match_items = []
        for i, vectors in enumerate(self.embedded_data):
            sim = self.cosine_similarity(target_vector, vectors)
            similar_indices = np.where(sim > 0.63)
            len_match = len(set(similar_indices[0]))
            symp_match = set(similar_indices[1])
            sim_match = np.array([sim[i][j] for i in similar_indices[0] for j in similar_indices[1]])
            if len_match == input_len:
                outdic = {
                    "idx": i,
                    "symptom_idx": symp_match,
                    "symptom_num": len(symp_match),
                }
                match_items.append(outdic)

        return match_items

    def search(self, input,get_score = True):
        input_len = len(input)
        embedded_input = np.array(self.embed_text(input))
        match_item = self.find_similar_vectors(embedded_input, input_len)
        if get_score:
            if len(match_item) > 0:
                return self.get_score(match_item,embedded_input)
            else:
                return "Not Found Matching Disease"
        else: return match_item

    def get_score(self, match_item,embedded_input):
        symptom_idx = [item["symptom_idx"] for item in match_item]
        symptom_num = [item["symptom_num"] for item in match_item]
        idx = [item["idx"] for item in match_item]

        int_list = []
        for s in symptom_idx:
            int_list.extend(list(s))
        idx_repos = [x for x, y in zip(idx, symptom_num) for _ in range(y)]
        selected_symp = [self.data['symptom'][id_val][id_sym] for id_val, id_sym in zip(idx_repos, int_list)]

        embed_sim_data = self.embed_text(selected_symp)
        
        cos_sim = self.cosine_similarity(embed_sim_data, embedded_input)
        max_sim = np.max(cos_sim, axis=1)

        max_symp_sim = {}
        for id_, simV in zip(idx_repos, max_sim):
            if id_ in max_symp_sim:
                max_symp_sim[id_] += simV
            else:
                max_symp_sim[id_] = simV

        score = [v / n for v, n in zip(max_symp_sim.values(), symptom_num)]

        output_dict = {}
        for i, id in enumerate(idx):
            output_dict[id] = {
                "name": self.data["name"][id],
                "th_name": self.data["th_name"][id],
                "score": round(score[i], 4)
            }
        return output_dict


if __name__ == "__main__":
    data_path = "/content/drive/MyDrive/MED Chat bot/Embed_Sep_Symptom.csv"
    searcher = SymptomSearcher(data_path)

    input = ["เป็นผื่น", "คันทั่วตัว", "ตาแดง"]
    item_n_score = searcher.search(input)
    print(item_n_score)
    

