import os
import json
from typing import Dict, Any
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
import re
def _try_parse_json(text: str) -> Dict[str, Any]:
    """Attempt to parse JSON from GPT output, ignoring extra text around it."""
    import json
    try:
        # Remove any leading/trailing text that isn't JSON
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        if json_start == -1 or json_end == -1:
            return None
        json_text = text[json_start:json_end]
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None

# def extract_structured_from_text(text: str) -> Dict[str, Any]:
#     """
#     Convert freeform RFP into structured JSON.
#     Uses OpenAI if API key provided; otherwise heuristic fallback.
#     Returns dict with keys:
#     - requirements: list of short sentences
#     - budget: string or None
#     - timeline: string or None
#     - evaluation_criteria: list
#     - items: list of dicts with name, quantity, specs (if detected)
#     """
#     if OPENAI_API_KEY:
#         try:
#             import openai
#             openai.api_key = OPENAI_API_KEY

#             prompt = f"""
# You are an AI that extracts structured data from RFPs. 
# Return ONLY JSON with the following keys:
# - requirements (array of short strings describing each requirement)
# - budget (number or null)
# - timeline (number of days or null)
# - evaluation_criteria (array)
# - items (array of objects: name, quantity, specs)

# RFP description:
# \"\"\"{text}\"\"\"
# """
#             resp = openai.ChatCompletion.create(
#                 model='gpt-4o-mini',
#                 messages=[{'role':'user','content':prompt}],
#                 temperature=0,
#                 max_tokens=800
#             )
#             content = resp['choices'][0]['message']['content']
#             parsed = _try_parse_json(content)
#             if parsed:
#                 # ensure all expected keys exist
#                 return {
#                     "requirements": parsed.get("requirements", []),
#                     "budget": parsed.get("budget"),
#                     "timeline": parsed.get("timeline"),
#                     "evaluation_criteria": parsed.get("evaluation_criteria", []),
#                     "items": parsed.get("items", [])
#                 }
#         except Exception as e:
#             pass  # fallback to heuristic

#     # --- Heuristic fallback ---
#     parts = {
#         "requirements": [],
#         "budget": None,
#         "timeline": None,
#         "evaluation_criteria": [],
#         "items": []
#     }

#     # Split into sentences
#     sentences = [s.strip() for s in re.split(r'[.\n]', text) if s.strip()]
#     for s in sentences:
#         low = s.lower()
#         if "budget" in low:
#             # extract numbers
#             m = re.search(r'\d[\d,]*', s.replace(',', ''))
#             if m:
#                 parts["budget"] = int(m.group())
#             else:
#                 parts["budget"] = s
#         elif "day" in low or "delivery" in low or "timeline" in low or "within" in low:
#             # extract numbers for timeline
#             m = re.search(r'\d+', s)
#             if m:
#                 parts["timeline"] = int(m.group())
#             else:
#                 parts["timeline"] = s
#         elif "laptop" in low or "monitor" in low or "printer" in low or "computer" in low:
#             # attempt to extract item + quantity
#             m = re.search(r'(\d+)\s+([a-zA-Z ]+)', s)
#             if m:
#                 parts["items"].append({
#                     "name": m.group(2).strip(),
#                     "quantity": int(m.group(1)),
#                     "specs": {}  # you can enhance later
#                 })
#         else:
#             parts["requirements"].append(s)

#     if not parts["requirements"] and sentences:
#         parts["requirements"].append(sentences[0])

#     return parts


def extract_structured_from_text(text: str) -> Dict[str, Any]:
    print("current value:", text)

    data = {
        "items": [],
        "budget": None,
        "timeline": None,
        "payment_terms": None,
        "warranty": None,
        "evaluation_criteria": []
    }

    # Normalize input
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()

    # ------------------- Extract Items Block ------------------- #
    # Find "1." "2." "3." patterns
    item_blocks = re.split(r"\s*\d+\.\s*", text)

    # First block is intro text; skip it
    item_blocks = item_blocks[1:]

    for block in item_blocks:
        item = {}

        # Extract fields using semicolon or period separators
        fields = re.split(r"[;.] ?", block)

        for f in fields:
            f = f.strip()
            if f.lower().startswith("item name"):
                item["item_name"] = f.split(":", 1)[1].strip()

            elif f.lower().startswith("quantity"):
                item["quantity"] = int(re.findall(r"\d+", f)[0])

            elif f.lower().startswith("type"):
                item["type"] = f.split(":", 1)[1].strip()

            elif f.lower().startswith("processor"):
                item["processor"] = f.split(":", 1)[1].strip()

            elif f.lower().startswith("ram"):
                item["ram"] = f.split(":", 1)[1].strip()

            elif f.lower().startswith("storage"):
                item["storage"] = f.split(":", 1)[1].strip()

            elif f.lower().startswith("size"):
                item["size"] = f.split(":", 1)[1].strip()

        if item:
            data["items"].append(item)

    # ------------------- Extract Other Fields ------------------- #
    # BUDGET
    m = re.search(r"Budget[: ]*\$?(\d+)", text, re.I)
    if m:
        data["budget"] = int(m.group(1))

    # TIMELINE
    m = re.search(r"Timeline[: ]*([^.]*)", text, re.I)
    if m:
        data["timeline"] = m.group(1).strip()

    # PAYMENT TERMS
    m = re.search(r"Payment Terms[: ]*([^.]*)", text, re.I)
    if m:
        data["payment_terms"] = m.group(1).strip()

    # WARRANTY
    m = re.search(r"Warranty[: ]*([^.]*)", text, re.I)
    if m:
        data["warranty"] = m.group(1).strip()

    # EVALUATION CRITERIA
    m = re.search(r"Evaluation Criteria[: ]*([^.]*)", text, re.I)
    if m:
        crits = m.group(1).split(",")
        data["evaluation_criteria"] = [c.strip() for c in crits]

    print("Extracted structured:", data)
    return data

def score_proposal_against_rfp(rfp_structured: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    if not rfp_structured:
        return {'score':50, 'explanation':'No structured RFP to compare.'}
    # simple heuristic: match requirement keywords
    reqs = rfp_structured.get('requirements') or []
    text = json.dumps(proposal).lower()
    match = 0
    for r in reqs:
        kws = [w for w in r.lower().split() if len(w)>3]
        for k in kws:
            if k in text:
                match += 1
    score = min(100, 40 + match*7)
    return {'score': score, 'explanation': f'Matched keywords: {match}.'}
