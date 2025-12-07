from mailparser import parse_from_string

def parse_vendor_email(raw_email: str) -> dict:
    '''
    Uses python-mail-parser to extract text and basic attachments.
    Returns a dict with keys 'text' and 'attachments' (filenames).
    '''
    try:
        mail = parse_from_string(raw_email)
        text = mail.body or mail.text_plain or ''
        attachments = [a['filename'] for a in mail.attachments or []]
        return {'text': text, 'attachments': attachments}
    except Exception as e:
        return {'text': raw_email, 'attachments': []}
