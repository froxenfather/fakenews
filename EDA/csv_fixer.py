import pandas as pd

input_file = "FakeNewsNet_scraped.csv"
output_file = "FakeNewsNet_scraped_FIXED.csv"


# god dammit
burger = pd.read_csv(input_file)

# reassing column types to avoid issues with shifted rows
for col in ["scraped_text", "scraped_words", "scrape_status", "fixed_url"]:
    burger[col] = burger[col].astype("string")

# force scraped_word_count to numeric so integers can be assigned into it
burger["scraped_word_count"] = pd.to_numeric(burger["scraped_word_count"], errors="coerce")

# detect shifted rows:
# scrape_status is just a number, and fixed_url contains the real status
doinked = (
    burger["scrape_status"].astype(str).str.fullmatch(r"\d+")
    & burger["fixed_url"].astype(str).str.match(
        r"^(success|missing_url|request_error)", case=False, na=False
    )
)

print("Shifted rows found:", doinked.sum())

# everything fking exploded so we need to temporarily store the shifted values before we can reassign them
tmp_scraped_text = burger.loc[doinked, "scraped_text"].copy()
tmp_scraped_words = burger.loc[doinked, "scraped_words"].copy()
tmp_scraped_word_count = burger.loc[doinked, "scraped_word_count"].copy()
tmp_scrape_status = burger.loc[doinked, "scrape_status"].copy()
tmp_fixed_url = burger.loc[doinked, "fixed_url"].copy()

# fix the rows
burger.loc[doinked, "fixed_url"] = tmp_scraped_text
burger.loc[doinked, "scraped_text"] = tmp_scraped_words
burger.loc[doinked, "scraped_words"] = tmp_scraped_word_count.astype("string")
burger.loc[doinked, "scraped_word_count"] = pd.to_numeric(tmp_scrape_status, errors="coerce")
burger.loc[doinked, "scrape_status"] = tmp_fixed_url

# status helper rebuilder thingy
def status_group(john_hellyah):
    s = str(john_hellyah).lower().strip()
    if s == "success":
        return "success"
    if "missing_url" in s:
        return "missing_url"
    if "timeout" in s or "read timed out" in s:
        return "request_timeout"
    if "404" in s:
        return "request_error_404"
    if "request_error" in s:
        return "other_request_error"
    return "other"

burger["status_group"] = burger["scrape_status"].apply(status_group)

# Save fixed file
burger.to_csv(output_file, index=False)

print("\nSaved fixed file as:", output_file)
print("\nUpdated status counts:")
print(burger["status_group"].value_counts(dropna=False))

# i pray to God that this works