import json
from pprint import pprint
from socket import timeout
from google_trans_new import google_translator
import pandas as pd 
from tqdm import tqdm
import ray
ray.init()

# translator = google_translator( timeout=20)
from easynmt import EasyNMT
model = EasyNMT('opus-mt')

@ray.remote
def for_loop(Questions):
    sentence = model.translate(Questions, source_lang="en", target_lang="vi" )
    # print(result["sentence"])
    # print(sentence)
    if sentence == Questions:
        print(Questions)
        print(sentence)
        assert False
    
    return sentence




def export(link_file, output_file):

    df_read = pd.read_csv(link_file)
    
    df = pd.DataFrame()
    Questions = []
    Category0 = []
    Category2 = []
    # list_sentence_orgin = []
    for idx in tqdm(range(len(df_read))):
        # result = json.loads(json_str)

        
        Questions.append(for_loop.remote(df_read["Questions"].iloc[idx]))
        
        Category0.append(df_read["Category0"].iloc[idx])
        Category2.append(df_read["Category2"].iloc[idx])

        # assert False
    Questions = ray.get(Questions)
    
    df["Questions"] = Questions
    df["Category0"] = Category0
    df["Category2"] = Category2
    df.to_csv(output_file, index=False)

export("Question_Classification_Dataset.csv", "Question_Classification_Dataset_vi.csv")
    