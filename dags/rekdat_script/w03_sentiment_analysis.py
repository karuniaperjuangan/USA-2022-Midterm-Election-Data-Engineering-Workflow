import pandas as pd
from nltk.tokenize import TweetTokenizer
from tqdm import tqdm
import re
from textblob import TextBlob


tweet_tokenizer = TweetTokenizer()

def tokenize_tweet(text):
  return " ".join(tweet_tokenizer.tokenize(text))

def remove_unnecessary_char(text):
  #text = re.sub("\[USERNAME\]", " ", text)
  text = re.sub("\[URL\]", " ", text)
  text = re.sub("\[SENSITIVE-NO\]", " ", text)
  text = re.sub('  +', ' ', text)
  return text

def preprocess_tweet(text):
  text = re.sub('\n',' ',text) # Remove every '\n'
  text = re.sub('^(\@\w+ ?)+',' ',text)
  text = re.sub(r'\@\w+',' ',text) # Remove every username
  text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
  text = re.sub('/', ' ', text)
  text = re.sub(r'[^\w\s]', '', text)
  text = re.sub('  +', ' ', text) # Remove extra spaces
  return text
    
def remove_nonaplhanumeric(text):
  text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
  return text

def preprocess(text):
  text = preprocess_tweet(text)
  text = remove_unnecessary_char(text)
  text = text.lower()
  text = tokenize_tweet(text)
  return text

def sentiment_analysis_tweet():
    df_tweet = pd.read_csv('./output/tweet_200percalon.csv')
    
    df_tweet["Clean Text"] = df_tweet["Text"].apply(preprocess)
    
    df_tweet["Polarity"] = df_tweet["Clean Text"].apply(lambda x : TextBlob(x).polarity)

    district_sentiment_df = pd.DataFrame(columns=["District","D Positive Tweet","D Negative Tweet","R Positive Tweet","R Negative Tweet"])
    for district in df_tweet["Candidate District"].unique():
        district_dict = {}
        district_dict["District"] = district
        district_dict["D Positive Tweet"] = len(df_tweet[(df_tweet["Candidate District"]==district) & (df_tweet["Candidate Party"]=="D") & (df_tweet["Polarity"]>0)])
        district_dict["D Negative Tweet"] = len(df_tweet[(df_tweet["Candidate District"]==district) & (df_tweet["Candidate Party"]=="D") & (df_tweet["Polarity"]<0)])
        district_dict["R Positive Tweet"] = len(df_tweet[(df_tweet["Candidate District"]==district) & (df_tweet["Candidate Party"]=="R") & (df_tweet["Polarity"]>0)])
        district_dict["R Negative Tweet"] = len(df_tweet[(df_tweet["Candidate District"]==district) & (df_tweet["Candidate Party"]=="R") & (df_tweet["Polarity"]<0)])
        
        district_sentiment_df = pd.concat([district_sentiment_df,pd.DataFrame([district_dict])])

    district_sentiment_df = district_sentiment_df.reset_index()
    
    district_sentiment_normalized_df = district_sentiment_df.copy()
    for index, row in district_sentiment_normalized_df.iterrows():
        total_d = row["D Positive Tweet"]+row["D Negative Tweet"]
        total_r = row["R Positive Tweet"]+row["R Negative Tweet"]
        if total_d>0:
            district_sentiment_normalized_df.loc[index,"D Positive Tweet"] = row["D Positive Tweet"]/total_d
            district_sentiment_normalized_df.loc[index,"D Negative Tweet"] = row["D Negative Tweet"]/total_d
        if total_r>0:
            district_sentiment_normalized_df.loc[index,"R Positive Tweet"] = row["R Positive Tweet"]/total_r
            district_sentiment_normalized_df.loc[index,"R Negative Tweet"] = row["R Negative Tweet"]/total_r
    district_sentiment_normalized_df.to_csv("./output/sentiment_per_district.csv",index=False) 