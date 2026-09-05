import requests
import csv
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API endpoints
job_url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
job_headers = {"X-API-Key": "jobboerse-jobsuche"}

school_url = "https://rest.arbeitsagentur.de/infosysbub/absuche/pc/v1/ausbildungsangebot"
school_headers = {'x-api-key': 'infosysbub-absuche'}


def search_jobs(ort, sw):
    results = []
    page = 0
    while page < 10:
        params = {"was": sw, "wo": ort, "angebotsart": 4, "page": page, "size": 25}
        response = requests.get(job_url, headers=job_headers, params=params)
        if response.status_code != 200:
            break
        jobs = response.json().get("stellenangebote", [])
        if not jobs:
            break
        for job in jobs:
            results.append({
                "titel": job.get("titel"),
                "name": job.get("arbeitgeber"),
                "email": job.get("email"),
                "zugang": job.get("zugang"),
                "link": job.get("externeUrl"),
                "quelle": "arbeitgeber"
            })
        print(f'job pages num {page}')
        page += 1
    return results


def search_schools(ort, sw):
    results = []
    page = 0
    while page < 25:
        url = school_url + "?ort=" + ort + "&sw=" + sw + "&page=" + str(page)
        response = requests.get(url, headers=school_headers)
        if response.status_code != 200:
            break
        termine = response.json().get("_embedded", {}).get("termine", [])
        if not termine:
            break
        for stelle in termine:
            angebot = stelle["angebot"]
            results.append({
                "titel": angebot.get("titel"),
                "name": angebot.get("bildungsanbieter", {}).get("name"),
                "email": angebot.get("bildungsanbieter", {}).get("email"),
                "zugang": angebot.get("zugang") or "keine Angabe",
                "link": angebot.get("link"),
                "quelle": "bildungsanbieter"
            })
        print(f'school pages num {page}')
        page += 1
    return results


def save_to_csv(entries, filename="bwb.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["titel", "name", "email", "zugang", "quelle", "status", "link"])
        for e in entries:
            writer.writerow([e["titel"], e["name"], e["email"], e["zugang"], e["quelle"], e.get("status", "not sent"), e["link"]])
    print(f"Saved {len(entries)} entries to {filename}")


git = input('paste your github profil link\n')
lnk = input('paste your linkedin profil\n')
cv = input('insert ur CV')

def build_message(entry):
    signature = f"""Mit freundlichen Grüßen,
Alaedine Touati
E-Mail: darkalae2@gmail.com
Telefon: 0770661183
GitHub: {git}
LinkedIn: {lnk}"""

    intro = f"""Mein Name ist Alaeddine Touati, ich bin 20 Jahre alt und komme aus Fès, Marokko. Seit einigen Monaten bereite ich mich intensiv und eigenständig auf eine berufliche Zukunft in Deutschland vor: Ich lerne Deutsch mit dem Ziel B2-Niveau und bringe mir parallel dazu Python und grundlegende Programmierkonzepte selbst bei, unter anderem durch eigene kleine Projekte wie ein Tool zur automatisierten Suche und Verwaltung von Ausbildungsangeboten.

Was mich besonders antreibt, ist die Kombination aus Disziplin und echtem Interesse an der Technik – ich arbeite regelmäßig mehrere Stunden täglich an meinen Programmierkenntnissen und bin bereit, diese Energie in eine praxisnahe Ausbildung wie diese einzubringen. Mir ist bewusst, dass ich am Anfang meines Weges stehe, doch genau deshalb suche ich eine Ausbildung, in der ich strukturiert lernen und wachsen kann. Auf GitHub und LinkedIn dokumentiere ich meinen Werdegang und meine Projekte öffentlich."""

    if entry["quelle"] == "arbeitgeber":
        return f"""Sehr geehrte Damen und Herren von {entry['name']},

mit großem Interesse habe ich Ihre Ausbildungsanfrage für die Position "{entry['titel']}" gesehen und möchte mich hiermit bewerben.

{intro}

Über die Möglichkeit eines persönlichen Gesprächs würde ich mich sehr freuen.

{signature}"""
    else:
        return f"""Sehr geehrte Damen und Herren von {entry['name']},

ich interessiere mich für Ihr Bildungsangebot "{entry['titel']}" und würde mich über weitere Informationen freuen.

{intro}

Zugangsvoraussetzungen laut Ihrer Anzeige: {entry['zugang']}

Über die Möglichkeit eines persönlichen Gesprächs würde ich mich sehr freuen.

{signature}"""

def generate_drafts(entries, output_folder="drafts"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    count = 0
    for e in entries:
        if not e["email"]:
            continue
        draft = build_message(e)
        safe_name = e["name"].replace("/", "-").replace(" ", "_") if e["name"] else "unknown"
        path = f"{output_folder}/{e['quelle']}_{safe_name}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(draft)
            print(f"the page {count}")
        count += 1
    print(f"Generated {count} draft(s) in ./{output_folder}/")


def send_reviewed_emails(entries, my_email, app_password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, app_password)

    for e in entries:
        if not e["email"]:
            e["status"] = "no email"
            continue

        safe_name = e["name"].replace("/", "-").replace(" ", "_") if e["name"] else "unknown"
        draft_path = f"drafts/{e['quelle']}_{safe_name}.txt"
        if not os.path.exists(draft_path):
            continue

        with open(draft_path, "r", encoding="utf-8") as f:
            body = f.read()

        print(f"\n--- [{e['quelle']}] {e['name']} ({e['email']}) ---")
        print(body)
        confirm = input("Send this one? (y/n): ")

        if confirm.lower() == "y":
            msg = MIMEText(body)
            msg["Subject"] = f"Bewerbung: {e['titel']}"
            msg["From"] = my_email
            msg["To"] = e["email"]
            server.sendmail(my_email, e["email"], msg.as_string())
            e["status"] = "sent"
            print("✅ Sent.")
        else:
            e["status"] = "skipped"
            print("Skipped.")

    server.quit()


if __name__ == "__main__":
    ort = input("Where you wanna work (city or region code): ")
    sw = input("What exactly you wanna work: ")

    jobs = search_jobs(ort, sw)
    schools = search_schools(ort, sw)
    entries = jobs + schools

    print(f"Found {len(jobs)} employer listings, {len(schools)} school/program listings.")

    if entries:
        save_to_csv(entries)
        generate_drafts(entries)

        proceed = input("\nReview and send emails now? (y/n): ")
        if proceed.lower() == "y":
            # Load email and app password from environment variables
            my_email = os.getenv("EMAIL")
            app_password = os.getenv("APP_PASSWORD")

            if not my_email or not app_password:
                print("Error: EMAIL and APP_PASSWORD must be set in .env file.")
            else:
                send_reviewed_emails(entries, my_email, app_password)
                save_to_csv(entries)
