import requests
import csv
import smtplib
import time
from email.mime.text import MIMEText

base_url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
headers = {"X-API-Key": "jobboerse-jobsuche"}

p1 = input('where you wanna work (city): ')
p2 = input('what exactly you wanna work: ')

my_email = "darkalae2@gmail.com"


def classy():
    filename = "bwb.csv"
    entries = []

    with open(filename, "w", newline="", encoding="utf-8") as ordner:
        writer = csv.writer(ordner)
        writer.writerow(["titel", "arbeitgeber", "ort", "refnr", "externeUrl"])

        page = 0
        while True:
            params = {
                "was": p2,
                "wo": p1,
                "angebotsart": 4,   # 4 = Ausbildung, real companies
                "page": page,
                "size": 25
            }
            print(f"Fetching page {page}...")
            response = requests.get(base_url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed to fetch page {page}")
                break

            data = response.json()
            jobs = data.get("stellenangebote", [])

            if not jobs:
                break

            for job in jobs:
                titel = job.get("titel")
                arbeitgeber = job.get("arbeitgeber")
                ort = job.get("arbeitsort", {}).get("ort")
                refnr = job.get("refnr")
                externe_url = job.get("externeUrl") or ""

                writer.writerow([titel, arbeitgeber, ort, refnr, externe_url])
                entries.append({
                    "titel": titel,
                    "arbeitgeber": arbeitgeber,
                    "ort": ort,
                    "externeUrl": externe_url
                })

            page += 1
            time.sleep(0.3)

    print(f"✅ Saved {len(entries)} listings to {filename}")
    return entries


def build_message(entry):
    titel = entry["titel"]
    arbeitgeber = entry["arbeitgeber"]
    ort = entry["ort"]

    subject = f"Bewerbung um einen Ausbildungsplatz als {p2}"
    body = f"""Sehr geehrte Damen und Herren von {arbeitgeber},

mit großem Interesse habe ich Ihre Stellenanzeige für die Position "{titel}" in {ort} gesehen und möchte mich hiermit bewerben.

Mein Name ist Alaeddine Touati, ich bin 20 Jahre alt und komme aus Fès, Marokko. Seit einigen Monaten bereite ich mich intensiv und eigenständig auf eine berufliche Zukunft in Deutschland vor: Ich lerne Deutsch mit dem Ziel B2-Niveau und bringe mir parallel dazu Python und grundlegende Programmierkonzepte selbst bei, unter anderem durch eigene kleine Projekte.

Was mich besonders antreibt, ist die Kombination aus Disziplin und echtem Interesse an der Technik. Mir ist bewusst, dass ich am Anfang meines Weges stehe, doch genau deshalb suche ich eine Ausbildung, in der ich strukturiert lernen und wachsen kann.

Über die Möglichkeit eines persönlichen Gesprächs würde ich mich sehr freuen.

Mit freundlichen Grüßen,
Alaeddine Touati
E-Mail: darkalae2@gmail.com
Telefon: 0770661183"""

    return subject, body


def review_and_send(entries):
    app_password = input("Gmail App Password: ")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, app_password)

    for entry in entries:
        subject, body = build_message(entry)

        print(f"\n--- {entry['arbeitgeber']} — {entry['titel']} ({entry['ort']}) ---")
        if entry["externeUrl"]:
            print(f"⚠️ This listing links to an external application page: {entry['externeUrl']}")
            print("Applying via email may not be the intended method — check the link before sending.")
        print(body)

        choice = input("Send this one? (y/n/skip all): ")

        if choice.lower() == "n":
            print("Skipped.")
            continue
        elif choice.lower() == "skip all":
            break

        receiver_email = input("Enter this company's contact email (leave blank to skip): ")
        if not receiver_email:
            print("No email provided, skipped.")
            continue

        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = my_email
            msg["To"] = receiver_email
            server.sendmail(my_email, receiver_email, msg.as_string())
            print(f"✅ Sent to {receiver_email}")
        except Exception as e:
            print(f"❌ Failed: {e}")

    server.quit()


if __name__ == "__main__":
    entries = classy()
    if entries:
        proceed = input("\nReview and send now? (y/n): ")
        if proceed.lower() == "y":
            review_and_send(entries)



