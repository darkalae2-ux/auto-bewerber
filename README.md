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


## Usage
Run the script: python script.py

Enter the required information
- Location (e.g., Berlin, BE, NW)
- Search term (e.g., Informatiker, Mechatroniker)

## What happens next
<li>The script searches both APIs one after the other.</li>
<li>All results are saved to bwb.csv.</li>
<li>For every email address found, a draft is created in the drafts/ folder.</li>
<li>The script asks if you want to send the emails.</li>
<li>If you confirm, each draft is displayed; you decide individually whether to send it.</li>
<li></li>

## What I Learned
○ Working with REST APIs (GET requests, query parameters, API keys)  
○ Pagination and stopping conditions  
○ Handling HTTP status codes (200, 403, 429)  
○ Writing CSV files and creating draft folders  
○ Sending email with SMTP and Gmail app passwords  
○ Moving credentials out of the code into `.env` for security  
○ Structuring a Python project with reusable functions  

## Future Improvements
<li>Add a GUI with Tkinter for a more user-friendly experience</li>
<li>Excel export with formatting</li>
<li>Automatically extract email addresses from job postings</li>
<li>Implement logging for better traceability</li>
<li>Create a configuration file for templates and sender details</li>

## Disclaimer
This project is for learning purposes only. The APIs of the Bundesagentur für Arbeit are publicly accessible, but their use is subject to their terms. Please handle the data responsibly.

   
