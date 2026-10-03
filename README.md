# PrivyNLP

**Privacy-Preserving NLP for Sensitive Text**

Micro Project – Data Security and Privacy

## Purpose
Detect selected sensitive identifiers in synthetic healthcare/student text and produce anonymized text using Python, spaCy NER, pandas, and deterministic regular expressions.

## MVP scope
Included:
- PERSON, ORG, GPE/LOC, DATE via spaCy
- EMAIL, PHONE, STUDENT_ID/USN, PATIENT_ID/MRN, synthetic NATIONAL_ID pattern, IP_ADDRESS via regex
- Stable placeholders such as `<PERSON_1>` and `<EMAIL_1>`
- Single-text mode and CSV mode
- Detection report and anonymized CSV output

Out of scope:
- Real patient/PHI data
- OCR, images, voice/video
- passwords/API keys/secrets
- encryption/key management
- legal/compliance certification
- guaranteed detection of every sensitive fact
- re-identification
- custom model training
- cloud/API processing

## Setup
Recommended: Python 3.11.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Run interactive mode:
```bash
python src/anonymizer.py
```

Run CSV mode:
```bash
python src/anonymizer.py --csv data/synthetic_texts.csv --text-column text
```

## Example
Original:
`Patient Maya Rao (MRN-20481) visited Green Valley Clinic on 14/09/2026. Email: maya.rao@example.com.`

Anonymized:
`Patient <PERSON_1> visited <ORG_1> on <DATE_1>. Email: <EMAIL_1>.`

## Academic safety
Use only synthetic text in the classroom demonstration. Automated de-identification is not a guarantee of anonymity.
