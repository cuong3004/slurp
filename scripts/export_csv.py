import json
from pprint import pprint
from google_trans_new import google_translator
import pandas as pd 
from tqdm import tqdm

translator = google_translator()

def export(link_file, output_file):
    with open(link_file, 'r') as json_file:
        json_list = list(json_file)
    
    df = pd.DataFrame()

    list_id = []
    list_sentence = []
    list_intent = []
    list_sentence_orgin = []
    for json_str in tqdm(json_list):
        result = json.loads(json_str)

        sentence = translator.translate(result["sentence"], lang_src="en", lang_tgt="vi")
        # print(result["sentence"])
        # print(sentence)
        if sentence == result["sentence"]:
            print(result["sentence"])
            print(sentence)
            assert False
        list_id.append(result["slurp_id"])
        
        list_sentence.append(sentence)
        list_sentence_orgin.append(result["sentence"])
        list_intent.append(result["intent"])
        # assert False
    
    df["ids"] = list_id
    df["intents"] = list_intent
    df["sentences"] = list_sentence
    df["sentence_orgin"] = list_sentence_orgin
    df.to_csv(output_file, index=False)

export("../dataset/slurp/train.jsonl", "train_vi.csv")
export("../dataset/slurp/test.jsonl", "test_vi.csv")
    