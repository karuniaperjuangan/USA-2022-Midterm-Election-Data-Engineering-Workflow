import xgboost as xgb
import pandas as pd
from sklearn import datasets
from sklearn import metrics
from sklearn.model_selection import train_test_split

def train_xgboost_model():
    df = pd.read_csv("./output/election_summary.csv")
    df = df.dropna()
    
    X = df.drop(["District","Winners"],axis=1)
    y= df["Winners"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    
    model.save_model("./output/us_election_xgb_model.json")