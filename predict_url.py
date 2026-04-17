import sys
import requests
from bs4 import BeautifulSoup
import joblib

def get_article_title(url):
    try:
        # Add more comprehensive headers to mimic a real browser to avoid 403 Forbidden errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Several sites use og:title, which is often cleaner than the <title> tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
            
        # Fallback to standard <title>
        if soup.title and soup.title.string:
            return soup.title.string.strip()
            
        return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict_url.py <article_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    
    print(f"Fetching title for: {url}")
    title = get_article_title(url)
    
    if not title:
        print("Could not extract title from the provided URL.")
        sys.exit(1)
        
    print(f"\nExtracted Title: '{title}'")
    
    print("Loading model...")
    try:
        model = joblib.load("fake_news_model.pkl")
    except FileNotFoundError:
        print("Error: Model file 'fake_news_model.pkl' not found. Please run train_model.py first.")
        sys.exit(1)
        
    print("Making prediction...")
    prediction = model.predict([title])[0]
    
    # Extract the keywords and their impact on the decision
    tfidf = model.named_steps['tfidf']
    clf = model.named_steps['clf']
    
    # Transform the title using TF-IDF
    vector = tfidf.transform([title])
    feature_names = tfidf.get_feature_names_out()
    non_zero_indices = vector.nonzero()[1]
    
    contributions = []
    for idx in non_zero_indices:
        word = feature_names[idx]
        # Calculate impact: tfidf score * model coefficient
        impact = clf.coef_[0][idx] * vector[0, idx]
        contributions.append((word, impact))
        
    # Sort contributions: negative impact = Fake, positive impact = Real
    contributions.sort(key=lambda x: x[1])
    
    fake_driving_words = [word for word, impact in contributions if impact < 0]
    real_driving_words = [word for word, impact in contributions if impact > 0]
    
    # Looking at train_model.py: target_names=['Fake (0)', 'Real (1)']
    if prediction == 1:
        result = "REAL NEWS"
        color_code = "\033[92m" # Green
    else:
        result = "FAKE NEWS"
        color_code = "\033[91m" # Red
        
    reset_code = "\033[0m"
    
    print(f"\nResult: {color_code}{result}{reset_code}")
    print("\n--- Model Analysis ---")
    if fake_driving_words:
        print(f"Keywords pushing toward FAKE: {', '.join(fake_driving_words[:5])}")
    if real_driving_words:
        # We reverse so the most impactful 'Real' words are first
        print(f"Keywords pushing toward REAL: {', '.join(reversed(real_driving_words[-5:]))}")
    if not fake_driving_words and not real_driving_words:
        print("No strongly predictive keywords found. The model made a weak guess based on bias/unknown words.")

if __name__ == "__main__":
    main()
