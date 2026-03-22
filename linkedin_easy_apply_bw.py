# linkedin_easy_apply_bw.py
import subprocess, json, os, time
from playwright.sync_api import sync_playwright
from sheets_logger import log_application  # Google Sheets helper
from job_analyzer  import analyze_job_fit, resume_skills  # Job description analysis helper

def get_bw_item(item_name):
    """Fetch credentials securely from Bitwarden vault"""
    session = os.getenv("BW_SESSION")
    result = subprocess.run(
        ["bw", "get", "item", item_name, "--session", session],
        capture_output=True, text=True
    )
    item = json.loads(result.stdout)
    return item["login"]["username"], item["login"]["password"]

# Fetch LinkedIn credentials from Bitwarden
EMAIL, PASSWORD = get_bw_item("LinkedIn")

RESUME = "./resume.pdf"
KEYWORDS = ["Databricks"]#, "Data Architect","Data Engineer"]
LOCATIONS = ["Remote"]#, "Pune", "Gurugram", "Delhi"]

def login(page):
    page.goto("https://www.linkedin.com/login")
    page.fill('input#username', EMAIL)
    page.fill('input#password', PASSWORD)
    page.click('button[type="submit"]')
#    page.wait_for_load_state("networkidle")
    page.wait_for_url("https://www.linkedin.com/feed/*")

def search_jobs(page, keyword, loc):
    page.goto("https://www.linkedin.com/jobs")
    page.fill('input[placeholder="Describe the job you want"]', keyword+' '+loc)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)

def try_apply(page, job_card):
    job_card.click()
    page.wait_for_timeout(1500)

    try:
        # Look for the job apply button inside the job detail container
        apply_button = page.query_selector('div[data-view-name="job-detail-page"] a[data-view-name="job-apply-button"]')
        if apply_button:
            aria_label = apply_button.get_attribute("aria-label")
            href = apply_button.get_attribute("href")

            if aria_label and "Easy Apply to this job" in aria_label:
                # For now, just flag availability
                return "Easy Apply Available"
                # --- Existing submit logic (commented for now) ---
                # page.click('a[data-view-name="job-apply-button"]')
                # page.wait_for_timeout(1000)
                # if page.query_selector('input[type="file"]'):
                #     page.set_input_files('input[type="file"]', RESUME)
                # if page.query_selector('button:has-text("Submit application")'):
                #     page.click('button:has-text("Submit application")')
                #     return "Submitted"
                # else:
                #     return "Prepared - manual submit required"

            elif aria_label and "Apply on company website" in aria_label:
                return f"Apply on company site: {href}"

        return "No Apply button found"
    except Exception as e:
        print("Error in try_apply:", e)
        return "Error"


def get_job_description(page):
    """Fetch the full job description text from the job detail container"""
    try:
        # Wait for the job detail container to appear
        page.wait_for_selector('div[data-view-name="job-detail-page"] span[data-testid="expandable-text-box"]', timeout=5000)
        desc_container = page.query_selector('div[data-view-name="job-detail-page"] span[data-testid="expandable-text-box"]')
        if desc_container:
            # Extract all text including <p> and <ul> children
            return desc_container.inner_text().strip()
    except Exception as e:
        print("Description fetch failed:", e)
    return "Description not available"

def load_resume():
    with open("resume.txt", "r", encoding="utf-8") as f:
        return f.read()

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        login(page)
        for kw in KEYWORDS:
            for loc in LOCATIONS:
                search_jobs(page, kw, loc)
                job_cards = page.query_selector_all('div[data-view-name="job-search-job-card"] div[role="button"]')
                print(len(job_cards), "jobs found for", kw, loc)
                resume_text = load_resume()

                for jc in job_cards:
                    status = try_apply(page, jc)
                    job_title = jc.inner_text()[:120]
                    job_url = page.url 
                    job_description = get_job_description(page) 
                    match_pct, found_skills, missing_skills = analyze_job_fit(job_description, resume_text, resume_skills)

                    if match_pct >= 70: 
                        log_application( job_title,
                                         job_url,
                                         status,
                                         notes=job_description,
                                         match_percent=match_pct,
                                         missingSkills=", ".join(missing_skills),
                                         matchedSkills=", ".join(found_skills))
                    else: 
                        print(f"Skipped {job_title[:30]} (Match {match_pct}%, Missing: {', '.join(missing_skills)}), Matched: {', '.join(found_skills)}") 
                    # log_application(job_title, job_url, status, notes=job_description)
                    time.sleep(2)
        browser.close()

if __name__ == "__main__":
    main()
