import pandas as pd

def merge_data():
    election_summary_df = pd.read_csv("./output/house_winners.csv")
    candidates_df = pd.read_csv("./output/candidates_detailed.csv")
    sentiment_df = pd.read_csv("./output/sentiment_per_district.csv")
    sentiment_df = sentiment_df.drop("index",axis=1)
    election_summary_df = election_summary_df.merge(sentiment_df,on=["District"],how="left")

    poll_dataset_df = pd.read_csv("https://datawrapper.dwcdn.net/LkGXt/3/dataset.csv",storage_options={'User-Agent': 'Mozilla/5.0'})
    poll_dataset_df["Name"] = poll_dataset_df["Name"].str.replace("-AL","00").str.replace("-","")
    
    election_summary_df = election_summary_df.merge(poll_dataset_df[["Name","Raw PVI","2020 Biden %","2020 Trump %","2016 Clinton %","2016 Trump %"]],how="left",left_on="District",right_on="Name")
    election_summary_df = election_summary_df.drop("Name",axis=1)
    
    election_summary_df["D Popularity"] = election_summary_df["District"].apply(lambda x: candidates_df[(candidates_df["party"]=="D")&(candidates_df["district"]==x)]["googleNewsPopularity"].sum())
    election_summary_df["R Popularity"] = election_summary_df["District"].apply(lambda x: candidates_df[(candidates_df["party"]=="R")&(candidates_df["district"]==x)]["googleNewsPopularity"].sum())
    election_summary_df[["2020 Biden %","2020 Trump %","2016 Clinton %","2016 Trump %"]] = election_summary_df[["2020 Biden %","2020 Trump %","2016 Clinton %","2016 Trump %"]].applymap(lambda x : float(x.replace("%",""))/100)

    election_summary_df = election_summary_df[['District', 'D Positive Tweet', 'D Negative Tweet','R Positive Tweet', 
                                           'R Negative Tweet', 'Raw PVI', '2020 Biden %','2020 Trump %', '2016 Clinton %', 
                                           '2016 Trump %', 'D Popularity', 'R Popularity', 'Winners']]
    election_summary_df.to_csv("./output/election_summary.csv",index=False)