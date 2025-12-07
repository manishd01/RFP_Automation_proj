import imaplib
import email
from email.header import decode_header
import re
from sqlalchemy.orm import Session
from datetime import datetime
from . import crud  # adjust relative import
from .deps import get_db
from .config import settings
from .schemas import ProposalCreate
from .crud import get_outbound_log

# ---------------------------
# Helpers
# ---------------------------
def decode_subject(subject_raw):
    decoded_bytes, encoding = decode_header(subject_raw)[0]
    if isinstance(decoded_bytes, bytes):
        return decoded_bytes.decode(encoding or "utf-8")
    return decoded_bytes

def match_rfp_from_subject(subject):
    match = re.search(r"RFP\s*#(\d+)", subject)
    if match:
        return int(match.group(1))
    return None

def process_incoming_email(db: Session, email_from: str, subject: str, raw_email: str):
    vendor = crud.get_vendor_by_email(db, email_from)
    print("Matched vendor:", vendor)
    if not vendor:
        return
    match = re.search(r"#(\d+):", subject)
    rfp_id = None
    if match:
        rfp_id= int(match.group(1))
    if(rfp_id is None):
        print("No RFP ID matched in subject, trying alternative method")
    # rfp_id = match_rfp_from_subject(subject )
    print("Matched RFP ID from subject:", rfp_id)
    if not rfp_id:
        return
    comm_log = crud.get_outbound_log(db, vendor.id, rfp_id)
    print("Processing email from:", email_from, "for RFP ID:", rfp_id,"detaisl", comm_log)
    # if comm_log and not comm_log.reply_received:
    #     crud.mark_reply_received(db, comm_log.id)

    print("automatically creating a  proposal entry in DB (considered as meaningful reply)")

    # Mark reply received
    if comm_log and not comm_log.reply_received:
        crud.mark_reply_received(db, comm_log.id)

    # -----------------------------
    # 🔥 AUTO-CREATE PROPOSAL ENTRY
    # -----------------------------
    print("Going to create proposal now...",comm_log, " ",comm_log.reply_received )
    proposal_in = ProposalCreate(
        vendor_id=vendor.id,
        rfp_id=rfp_id,
        proposal=None,
        raw_email=raw_email,
        score=None
    )
    print("this--line")
    crud.create_proposal(
        db=db,
        vendor_id=vendor.id,
        rfp_id=rfp_id,
        p=proposal_in
    )

    print("✅ Proposal created in DB")
    print("✅ Proposal stored for vendor:", vendor.id, "RFP:", rfp_id)

# ---------------------------
# Main polling function
# ---------------------------
def check_inbox_and_process_replies():
    IMAP_HOST = settings.IMAP_HOST
    IMAP_USER = settings.IMAP_USER
    IMAP_PASS = settings.IMAP_PASS  # use environment variable for security

    db = next(get_db())  

    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")
    print("Checking inbox for replies...")
    status, messages = mail.search(None, '(UNSEEN)')
    print("Search status:", status)
    print("Messages found:", messages)
    if status != "OK":
        return

    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        if status != "OK":
            continue
        
        print("Processing email number:", num)
        msg = email.message_from_bytes(data[0][1])
        from_addr = email.utils.parseaddr(msg.get("From"))[1]
        subject = decode_subject(msg.get("Subject"))

        if msg.is_multipart():
            parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    parts.append(part.get_payload(decode=True).decode())
            raw_email = "\n".join(parts)
        else:
            raw_email = msg.get_payload(decode=True).decode()
        print("From:", from_addr, "Subject:", subject,  "Raw email :",(raw_email))
        process_incoming_email(db, from_addr, subject, raw_email)
        mail.store(num, '+FLAGS', '\\Seen')

    mail.logout()
