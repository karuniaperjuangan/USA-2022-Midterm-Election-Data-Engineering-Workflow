import snscrape
from tqdm import tqdm
import datetime as dt
import os
import snscrape.modules.twitter as sntwitter
import pandas as pd

def scrape_tweets(query, max_tweets=-1): 
    tweets_list = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if max_tweets != -1 and i >= int(max_tweets):
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content])
    df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text'])
    return df

def scrape_twitter(max_tweets=200):
    candidates_df = pd.read_csv('./output/candidates.csv')

    candidates_df = candidates_df[candidates_df['party'].apply(lambda x : x in ["D","R"])] #Filter hanya calon republikan dan demokrat saja

    all_tweet_df = pd.DataFrame(columns=['Datetime', 'Tweet Id', 'Text','Candidate Name','Candidate Party','Candidate District'])
    for index,row in tqdm(candidates_df.iterrows()):
        tweet_calon_ini_df = scrape_tweets(row['name'],max_tweets=max_tweets)
        tweet_calon_ini_df['Candidate Name'] = row['name']
        tweet_calon_ini_df['Candidate Party'] = row['party']
        tweet_calon_ini_df['Candidate District'] = row['district']
        all_tweet_df = pd.concat([all_tweet_df,tweet_calon_ini_df])
    all_tweet_df.to_csv('./output/tweet_200percalon.csv',index=False)