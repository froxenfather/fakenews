import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    print("Loading datasets...")
    # Load dataset
    df = pd.read_csv("datasets/FakeNewsNet.csv")
    
    print(f"Dataset loaded with {len(df)} rows.")
    
    # Data preprocessing
    print("Preprocessing data...")
    # Fill NaN values in 'title' with an empty string to avoid errors with vectorizer
    df['title'] = df['title'].fillna('')
    
    # We will use the 'title' column for prediction
    X = df['title']
    y = df['real']
    
    # Split the dataset
    print("Splitting dataset into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create the pipeline
    print("Creating Pipeline with TfidfVectorizer and LogisticRegression...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1,2))),
        ('clf', LogisticRegression(random_state=42, max_iter=1000))
    ])
    
    # Train the model
    print("Training the model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate the model
    print("Evaluating the model...")
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake (0)', 'Real (1)']))
    
    # Save the model
    model_filename = "fake_news_model.pkl"
    print(f"Saving the model to {model_filename}...")
    joblib.dump(pipeline, model_filename)
    print("Done!")

if __name__ == "__main__":
    main()
