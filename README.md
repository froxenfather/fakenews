# fakenews
A quick and lightweight model that accurately predicts on if a given website is fake news using webscraping and such
im so tired

okay guys lets make a website

Ryan Freese
Aedon Kettles
Jack 

# Fake News

Just pulled the repo and want the site running? Just follow these four billion simple steps for me!

## Please maks sure you have
- Python installed
- Node.js installed
- The trained model file at:

```text
webapp/backend/saved/model.pkl
```
Needs to be named model.pkl as well

Use jacks jypnb to make a file if it is missing

## Start the website

Open a terminal, or simply run 

```powershell
launch-web.py
```
Two terminals will open, do not be alarmed!

If it works, the backend will be running on one of the terminals:

```text
http://127.0.0.1:8000
```
Then open the local Vite link it gives you on the second terminal, usually:

```text
http://localhost:5173/
```

## Next

- Paste a news article URL into the input box
- Click **Analyze**
- The frontend SHOULD send the URL to the backend
- The backend SHOULD scrape the site and run the model
- The result shows up on the page

## No worky?

### `npm` is not working
Use `npm.cmd` instead of `npm` in PowerShell. weird bug that happened to me as well

### Backend says the model is missing
Make sure this file exists:

```text
webapp/backend/saved/model.pkl
```

### Frontend opens but Analyze fails
Make sure the backend is still running on port 8000.

# TLDR

Terminal 1:

```powershell
cd webapp\backend
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

Terminal 2:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

### KEEP BOTH TERMINALS RUNNING

I cannot stress enough that you NEED node.js and it needs to be on your default path as well fellas

Godspeed. Feel free to tweak

# Other Files

Model Training is all handled in the model training files

EDA is in the EDA File. It contains a python script that you MUST run to fix the script (as i had a weird bug in my scraper)

Website Scraper is in data-aqq

## Full Run

- Scrape websites with csv_website_scraper.ipynb
- Fix CSV with csv_fixer after copying the scraped CSV into the same folder as EDA
- Run the EDA to trim the file
- Train a model with either of the model trainiers in model_training
- Save the model.pkl and move it into webapp/backend/saved
- select the models name in api.py
- launch the website with launch_web.py

