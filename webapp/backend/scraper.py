# scraper code.
# most of this came from the original jupyter notebook where i scraped a giant csv of article links.
# this version is way more focused and just handles one site at a time for the web app,
# which is a lot saner than trying to drag the goddam thing in here

# this should work fine jack
import re
from typing import Dict, Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from url_normalize import url_normalize



# pretend to be a normal browser so websites are slightly less likely to instantly hate us.
# this does not make us invincible, it just makes us look a little less suspicious.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

# clean up website title
def clean_website_title(text: str) -> str:
     # if this is not even a string, we are already off to a bad start
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_words(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def scrape_website(url: str, timeout: int = 10) -> Dict[str, Any]:
    if not isinstance(url, str) or not url.strip():
        return {
            "original_url": url,
            "fixed_url": None,
            "title": "",
            "source_domain": "unknown",
            "scraped_text": "",
            "scraped_words": "",
            "scraped_word_count": 0,
            "scrape_status": "missing_url",
        }
    # attempt to use that cool little library to clean up the url and make it more likely to work, but if it fails for some reason we can still try to scrape the original url
    try:
        fixed_url = url_normalize(url)
    except Exception as e:
        return {
            "original_url": url,
            "fixed_url": None,
            "title": "",
            "source_domain": "unknown",
            "scraped_text": "",
            "scraped_words": "",
            "scraped_word_count": 0,
            "scrape_status": f"normalize_error: {str(e)}",
        }

    # Scrape the website using requests and BeautifulSoup. 
    # Ripped most of this from the Jupiter Notebook, but I added some extra error handling and made it a bit more robust to different website structures.

    # actually request the page
    # timeout exists because some sites move like they are being rendered on a microwave
    # at somepoint we just gotta stick a fork in it
    try:
        response = requests.get(fixed_url, headers=HEADERS, timeout=timeout)
        # raise error if we get a bad status code, like 404 or 500, because that means we probably didn't get the content we wanted and it's better to just give up on this url
        response.raise_for_status()

        # parse the mf
        soup = BeautifulSoup(response.text, "html.parser")

        #evicerate foid tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()

        # try to grab title if it exists
        title = ""
        if soup.title and soup.title.string:
            title = clean_website_title(soup.title.string)

        #now we try to find the actual main content
        #this is not perfect, but it is a decent first pass and not completely stupid
        #article is best if it exists
        #main is backup
        #body is the "fine whatever" fallback
        #and soup itself is the last desperate measure
        #pretty proud of myself for this one
        content = soup.find("article")
        if content is None:
            content = soup.find("main")
        if content is None:
            content = soup.body
        if content is None:
            content = soup

        #get all the text from whatever content block we found
        #separator=" " helps stop words from getting smashed together into some bullshit
        text = clean_website_title(content.get_text(separator=" "))
        words = extract_words(text)
        words_joined = " ".join(words)

        parsed = urlparse(fixed_url)
        source_domain = parsed.netloc.lower() if parsed.netloc else "unknown"

        # if we somehow got here but still have no usable text, say so directly
        # no point pretending we successfully scraped farts from the wind man
        if not text:
            return {
                "original_url": url,
                "fixed_url": fixed_url,
                "title": title,
                "source_domain": source_domain,
                "scraped_text": "",
                "scraped_words": "",
                "scraped_word_count": 0,
                "scrape_status": "empty_content",
            }
        # yay scrape worked!!!!!
        return {
            "original_url": url,
            "fixed_url": fixed_url,
            "title": title,
            "source_domain": source_domain,
            "scraped_text": text,
            "scraped_words": words_joined,
            "scraped_word_count": len(words),
            "scrape_status": "success",
        }

    except requests.exceptions.RequestException as e:
        # request-related failure: bad connection, timeout, blocked page, 404, whatever nightmare happened
        return {
            "original_url": url,
            "fixed_url": fixed_url,
            "title": "",
            "source_domain": "unknown",
            "scraped_text": "",
            "scraped_words": "",
            "scraped_word_count": 0,
            "scrape_status": f"request_error: {str(e)}",
        }
    
    # if the code gets here man its becuase EVERYTHING fucked up
    except Exception as e:
        return {
            "original_url": url,
            "fixed_url": fixed_url,
            "title": "",
            "source_domain": "unknown",
            "scraped_text": "",
            "scraped_words": "",
            "scraped_word_count": 0,
            "scrape_status": f"parse_error: {str(e)}",
        }