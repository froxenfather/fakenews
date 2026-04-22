# dont touch most of this
# this is the connections for our backend
# as complex as it is, it should be pretty straightforward. 
# The API receives a URL from the frontend, scrapes the website using scraper.py, 
# processes the scraped data into features using model_utils.py, and then returns the prediction result to the frontend.
# im sure it works fine!

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scraper import scrape_website
from model_utils import load_model, predict_from_scrape

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# added this for model
model = load_model()


class PredictRequest(BaseModel):
    url: str


# Make sure backend works?
@app.get("/")
def root():
    return {"message": "Backend is alive"}


@app.post("/predict")
def predict(request: PredictRequest):
    raw_url = request.url.strip()

    if not raw_url:
        raise HTTPException(status_code=400, detail="That's not a website bro.")

    scrape_result = scrape_website(raw_url)

    if scrape_result["scrape_status"] != "success":
        raise HTTPException(
            status_code=400,
            detail="Couldn't scrape that site. Try a real article link."
        )

    try:
        prediction = predict_from_scrape(scrape_result, model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return {
        "url": scrape_result["fixed_url"],
        "title": scrape_result["title"],
        "source_domain": scrape_result["source_domain"],
        "scrape_status": scrape_result["scrape_status"],
        "scraped_word_count": scrape_result["scraped_word_count"],
        "prediction": prediction,
        "preview": scrape_result["scraped_text"][:500],
    }