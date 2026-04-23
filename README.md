# fakenews
A quick and lightweight model that accurately predicts on if a given website is fake news using webscraping and such
im so tired

okay guys lets make a website

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

Godspeed. Feel free to tweak ts
