import re
from pathlib import Path
from urllib.parse import urlparse

import joblib
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



"""
This file contains utility functions for loading the model, cleaning text, engineering features, and making predictions. 
The API file will call these functions to process the scraped data and return predictions to the frontend. 
This keeps our code organized and modular, and allows us to easily update the model or feature engineering without having to change the API code.

If you need to mess with things, do it here. Save the model with joblib, change it to "model.pkl" and put it in the saved directory, and then you can load it here with the load_model function.
The predict_from_scrape function is where the API will call to get a prediction from the scraped data. It takes the scrape result and the loaded model, 
builds the feature row, and then returns a dict with the predicted label, confidence, and probabilities for each class.

Does that make sense? does ANY of this make sense? if not, just ask and I can explain it in more detail. most of this is YOUR code and my code anyway jack lmfao.
"""


# needed so you chuds can load this from anywhere and it will still find the model file in the saved directory. Also good practice to keep file paths organized and not hardcode them all over the place i suppose
BASE_DIR = Path(__file__).resolve().parent
SAVED_DIR = BASE_DIR / "saved"
MODEL_PATH = SAVED_DIR / "fake_news_model.pkl" #Change this name to swap models, make sure to save

# BEAUTIFULSOUP4 and REQUESTS are imported in scraper.py, so we can use them there without importing here. This file is for model utils, so we keep it focused on that
# bELOW IS A RESOURCE CHECKER, MODEL LOADER, TEXT CLEANER, FEATURE BUILDER, AND PREDICTION FUNCTION. THE API FILE CALLS THESE FUNCTIONS TO MAKE PREDICTIONS BASED ON SCRAPED DATA FROM THE WEBSITE
# quick check to make sure nltk resources exist before we try to use them
# otherwise stopwords/wordnet will randomly throw a fit at runtime and ruin my afternoon
def ensure_nltk_resources():
    resources = [
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
    ]

    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)

# aight we okay
ensure_nltk_resources()

# nuke the badwords and lemmatize the rest to get a cleaner version of the text for the model to work with
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def load_model():
    return joblib.load(MODEL_PATH)

# Jacks Text Cleaner, url features code
def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(tokens)

# Jacks code, tweaked it slightly to make it reusable in a fucntion
def engineer_url_features(df):
    # deals with missing values with blank spaces
    url = df["news_url"].fillna("")
    furl = df["fixed_url"].fillna("")

    # extract more useful features from urls
    return pd.DataFrame({
        "url_length": url.str.len(),
        "url_num_slashes": url.str.count("/"),
        "url_has_https": url.str.startswith("https").astype(int),
        "url_suspicious": url.str.contains(
            r"breaking|alert|shock|secret|viral|hoax",
            case=False,
            na=False
        ).astype(int),
        "url_was_redirected": (url != furl).astype(int),
    })


# take the scraped website result and convert it into a one-row dataframe
# that matches the shape of the training features as closely as possible
# this was a bulk of my work, and was a bit of a fucking nightmare
def build_feature_row(scrape_result: dict) -> pd.DataFrame:
    df = pd.DataFrame([{
        "title": scrape_result.get("title", "") or "",
        "scraped_words": scrape_result.get("scraped_words", "") or "",
        "tweet_num": 0,
        # TODO: JACK DO THIS
        # jack if you have an answer on HOW to work around this put it here man
        # tweet_num is set to 0 here because we do not have that live from scraping
        # not ideal, but good enough for now unless we redesign the feature set later
        "scraped_word_count": scrape_result.get("scraped_word_count", 0) or 0,
        "news_url": scrape_result.get("original_url", "") or "",
        "fixed_url": scrape_result.get("fixed_url", "") or "",
        "source_domain": scrape_result.get("source_domain", "unknown") or "unknown",
    }])

    # clean both the title and body of the article
    df["clean_title"] = df["title"].apply(clean_text)
    df["clean_body"] = df["scraped_words"].apply(clean_text)

    # collect info from urls
    url_feats = engineer_url_features(df)
    df = pd.concat([df, url_feats], axis=1)

    # fill in missing source_domain if needed
    df["source_domain"] = df["source_domain"].fillna("unknown")

    numeric_cols = [
        "tweet_num",
        "scraped_word_count",
        "url_length",
        "url_num_slashes",
        "url_has_https",
        "url_suspicious",
        "url_was_redirected",
    ]
    categorical_cols = ["source_domain"]
    text_title_col = "clean_title"
    text_body_col = "clean_body"

    feature_cols = [text_title_col, text_body_col] + numeric_cols + categorical_cols
    X = df[feature_cols]

    return X


# Call the model itself and return a dict with the label, confidence, and probabilities for each class. The API will call this function and return the result to the frontend
# Mrfreese
def predict_from_scrape(scrape_result: dict, model) -> dict:
    X = build_feature_row(scrape_result)

    # Binary Encoding 


    # such a innocent looking line of code that does everythiung lmfao
    prediction = model.predict(X)[0]




    label_map = {
        0: "Fake",
        1: "Real",
    }

    readable_label = label_map.get(prediction, str(prediction))

    result = {
        "label": readable_label
    }

    # Probability that the model assigns to the predicted class, or rather its confidence
    probabilities = model.predict_proba(X)[0]
    predicted_index = probabilities.argmax()

    # YO JACK THIS WAS THE LINE YOU WERE TALKING ABOUT
    # THERE IS A PROBABILITY FOR EACH CLASS
    result["confidence"] = float(probabilities[predicted_index])
    result["probabilities"] = probabilities.tolist()

    return result