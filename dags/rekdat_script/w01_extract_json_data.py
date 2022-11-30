import requests
import json
import pandas as pd

def extract_json_data():
    response = requests.get('https://interactive.guim.co.uk/2022/11/us-midterm-elections/results/production/results.json')
    data_dict = response.json() # Format dictionary dari jsonnya
    
    list_candidates = []
    for item in data_dict['houseDetails'].keys():
        district_candidates = data_dict['houseDetails'][item]['details']['candidates'] #Contoh: [{'name': 'Michael Burgess', 'party': 'R', 'votes': 183379, 'isWinner': 'X', 'isIncumbent': True}, {'name': 'Mike Kolls', 'party': 'L', 'votes': 81208}]
        for candidate in district_candidates:
            candidate['district'] = item
            list_candidates.append(candidate)
    
    candidates_df= pd.read_json(json.dumps(list_candidates))
    candidates_df['isWinner'] = candidates_df['isWinner'].apply(lambda x: True if x=="X" else False)
    candidates_df['isIncumbent'] = candidates_df['isIncumbent'].apply(lambda x: True if x==1 else False)
    candidates_df = candidates_df[(candidates_df['party']=="R")|(candidates_df['party']=="D")]
    
    candidates_df.to_csv('./output/candidates.csv',index=False)
    
    house_winners_df = pd.DataFrame.from_dict(data_dict['houseWinners'],orient='index',columns=['Winners'])
    house_winners_df["District"] = house_winners_df.index
    house_winners_df = house_winners_df[["District","Winners"]]
    
    house_winners_df.to_csv("./output/house_winners.csv",index=False)