import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import json
from typing import List, Dict
from ..config import settings
from ..crud import create_communication_log
from ..schemas import CommunicationLogCreate
from sqlalchemy.orm import Session


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from core.config import settings



# def send_rfp_email(vendor_id: int, rfp_id: int, to_email: str, subject: str, body: str) -> bool:
def send_rfp_email(db: Session, vendor_id: int, rfp_id: int, to_email: str, subject: str, body: str, raw_text_mail: str) -> bool:
    host = settings.SMTP_HOST
    port = settings.SMTP_PORT
    user = settings.SMTP_USER
    passwd = settings.SMTP_PASS

    if not user or not passwd:
        print("SMTP credentials not provided; skipping send.")
        return False

    # Try parsing JSON string
    try:
        data = json.loads(body)
    except Exception:
        # fallback if plain text
        data = {
            "items": [],
            "budget": None,
            "timeline": None,
            "payment_terms": None,
            "warranty": None,
            "evaluation_criteria": []
        }
        # If plain text, show it as a single "description" row
        data["items"].append({"item_name": body, "quantity": "", "type": "", "processor": "", "ram": "", "storage": "", "size": ""})

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f6f6f6; padding:20px; margin:0;">
        <div style="max-width:700px; margin:0 auto; background:white; padding:25px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.08);">

        <!-- Header -->
        <h2 style="color:#2c3e50; border-bottom:2px solid #eee; padding-bottom:8px; margin-bottom:20px;">
            Request For Proposal (RFP)
        </h2>

        <!-- Items Table -->
        <table style="width:100%; border-collapse: collapse; margin-bottom:20px; font-size:14px;">
            <thead>
            <tr style="background:#3498db; color:white; text-align:left;">
                <th style="padding:8px; border:1px solid #ddd;">Item Name</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td style="padding:8px; border:1px solid #ddd;">
                Desktop PC<br>
                Quantity: 25<br>
                Type: Computing Hardware<br>
                Processor: Intel Core i5<br>
                RAM: 8GB<br>
                Storage: SSD 256GB
                </td>
            </tr>
            <tr>
                <td style="padding:8px; border:1px solid #ddd;">
                Keyboard & Mouse Combo<br>
                Quantity: 25<br>
                Type: Accessories<br>
                Processor: N/A<br>
                RAM: N/A<br>
                Storage: N/A<br>
                Size: Standard
                </td>
            </tr>
            </tbody>
        </table>

        <!-- Details Section -->
        <div style="margin-top:20px; line-height:1.6; font-size:15px; color:#333;">
            <p><strong>Budget:</strong> $40,000</p>
            <p><strong>Timeline:</strong> 20 days</p>
            <p><strong>Payment Terms:</strong> Net 30</p>
            <p><strong>Warranty:</strong> 1 year</p>
            <p><strong>Evaluation Criteria:</strong> Performance, Cost, Delivery Speed</p>
        </div>

        <!-- Footer -->
        <div style="margin-top:30px; padding:15px; background:#f1f1f1; border-left:4px solid #3498db; border-radius:5px;">
            <strong style="color:#2c3e50;">Regards,<br>Procurement Team</strong>
        </div>

        </div>
    </body>
    </html>
    """



    # Send email
    msg = MIMEMultipart("alternative")
    msg["From"] = user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(json.dumps(data, indent=2), "plain"))  # plain fallback
    msg.attach(MIMEText(html_body, "html"))                    # HTML version

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, passwd)
        server.send_message(msg)
    
    # db = SessionLocal()
    log_data = CommunicationLogCreate(
        vendor_id=vendor_id,
        rfp_id=rfp_id,
        direction="outbound",
        subject=subject,
        raw_email=raw_text_mail,
        extracted = json.dumps(body) 

    )

    create_communication_log(
        db=db,
        vendor_id=vendor_id,
        rfp_id=rfp_id,
        c=log_data
    )

    print("Email sent to", to_email, "for RFP ID", rfp_id, "to vendor ID", vendor_id)

    print("Outbound communication log created.")

    return True

def fetch_unseen_emails_imap(host: str, user: str, password: str, folder: str='INBOX') -> List[Dict]:
    '''
    Connects to IMAP, fetches unseen messages and returns list of dicts with raw email strings.
    '''
    mails = []
    try:
        M = imaplib.IMAP4_SSL(host)
        M.login(user, password)
        M.select(folder)
        typ, data = M.search(None, 'UNSEEN')
        if typ != 'OK':
            return mails
        for num in data[0].split():
            typ, msgdata = M.fetch(num, '(RFC822)')
            if typ != 'OK':
                continue
            raw = msgdata[0][1].decode('utf-8', errors='ignore')
            mails.append({'raw': raw})
            # mark as seen
            M.store(num, '+FLAGS', '\\Seen')
        M.close()
        M.logout()
    except Exception as e:
        print('IMAP fetch failed:', e)
    return mails
