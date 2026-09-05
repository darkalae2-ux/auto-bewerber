# auto-bewerber


# Ausbildung Scraper & Email Sender

A Python script that automatically searches for apprenticeship positions and training programs from the German Federal Employment Agency (Bundesagentur für Arbeit), saves them to a CSV file, and sends personalized application emails to the providers.

## Features

- **Dual search**  
  - Employer job listings (`/jobboerse/jobsuche-service/pc/v4/jobs`)  
  - Educational provider programs (`/infosysbub/absuche/pc/v1/ausbildungsangebot`)  
- **Automatic pagination** – fetches all results up to defined limits  
- **CSV export** – stores title, provider, email, access, source, status, and link  
- **Draft generation** – creates an individual application email for each result as a text file  
- **Interactive sending** – shows each email before sending; you approve or skip each one  
- **Secure credentials** – email and app password are stored in a `.env` file  

## Technologies Used

- Python 3.x  
- `requests` – HTTP requests to the APIs  
- `csv` – saving results  
- `smtplib` / `email.mime.text` – sending emails  
- `python-dotenv` – loading credentials from `.env`  

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/ausbildung-scraper.git
   cd ausbildung-scraper
---

**Usage**
Run the script: python script.py

Enter the required information
- Location (e.g., Berlin, BE, NW)
- Search term (e.g., Informatiker, Mechatroniker)

**What happens next**
The script searches both APIs one after the other.
All results are saved to bwb.csv.
For every email address found, a draft is created in the drafts/ folder.
The script asks if you want to send the emails.
If you confirm, each draft is displayed; you decide individually whether to send it.


**What I Learned**
• Working with REST APIs
• GET requests with query parameters
• Handling API keys in headers
Pagination and stopping conditions
Error handling
Understanding HTTP status codes (200, 403, 429)
Preventing crashes when data is missing
File I/O
Writing CSV files
Creating and filling folders for drafts
Sending email with Python
SMTP with Gmail and app password
MIMEText for simple text emails
Security
Moving credentials out of the code into .env
Project structure
Reusable functions
Separation of search, saving, and sending

**Future Improvements**
Add a GUI with Tkinter for a more user-friendly experience
Excel export with formatting
Automatically extract email addresses from job postings
Implement logging for better traceability
Create a configuration file for templates and sender details

**Disclaimer**
This project is for learning purposes only. The APIs of the Bundesagentur für Arbeit are publicly accessible, but their use is subject to their terms. Please handle the data responsibly.

   
