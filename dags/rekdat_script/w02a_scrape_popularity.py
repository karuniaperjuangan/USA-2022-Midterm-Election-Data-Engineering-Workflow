from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
tqdm.pandas()

def find_popularity(keyword):
  for i in range(3): # Mencoba 3 kali jika error
    try:
      query_keyword = keyword.replace(" ","+").lower()
      #print(query_keyword)
      r = requests.get(f"https://www.google.com/search?q={query_keyword}&tbm=nws",headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
      if r.status_code == 429:
        print("429 Error! Retry After",r.headers['Retry-After'])
        time.sleep(int(r.headers['Retry-After']))
        r = requests.get(f"https://www.google.com/search?q={query_keyword}&tbm=nws",headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
      soup = BeautifulSoup(r.text, 'html.parser')
      return int( soup.find_all("div", attrs={"id":'result-stats'})[0].text.split(" ")[1].replace(",","") )
    except Exception as ex:
      print(ex)
      continue
  print(f"Keyword {keyword} Not Found")
  return np.nan

def scrape_candidates_popularity():
    df = pd.read_csv('./output/candidates.csv')
    df = df[(df["party"]=="D")|(df["party"]=="R")]
    df["googleNewsPopularity"] = df["name"].apply(find_popularity)
    
    df.to_csv('./output/candidates_detailed.csv',index=False)