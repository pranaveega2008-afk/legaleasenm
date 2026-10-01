"""
document_templates.py - Legal Templates for LegalEase
Provides structured, legally formatted document templates in both English and Tamil.
"""

from datetime import datetime

DOCUMENT_TYPES = {
    "Rental Agreement": {
        "en": "Residential Rental Agreement",
        "ta": "குடியிருப்பு வாடகை ஒப்பந்தம் (Rental Agreement)"
    },
    "Non-Disclosure Agreement (NDA)": {
        "en": "Non-Disclosure Agreement (NDA)",
        "ta": "ரகசிய காப்பு ஒப்பந்தம் (Non-Disclosure Agreement)"
    },
    "General Affidavit": {
        "en": "General Sworn Affidavit",
        "ta": "பொது உறுதிமொழி ஆவணம் (General Affidavit)"
    },
    "Freelance Service Agreement": {
        "en": "Freelance & Service Agreement",
        "ta": "சுயாதீன சேவை ஒப்பந்தம் (Freelance Agreement)"
    },
    "Employment Offer Letter": {
        "en": "Employment Offer & Appointment Letter",
        "ta": "பணி நியமனக் கடிதம் (Employment Offer Letter)"
    },
    "Promissory Note": {
        "en": "Demand Promissory Note",
        "ta": "கடன் உறுதிப்பத்திரம் (Promissory Note)"
    }
}


def generate_rental_agreement(data: dict, lang: str = "en") -> str:
    party1 = data.get("party1_name", "Landlord Name")
    addr1 = data.get("party1_address", "Landlord Address")
    party2 = data.get("party2_name", "Tenant Name")
    addr2 = data.get("party2_address", "Tenant Address")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    rent = data.get("rent_amount", "15,000")
    deposit = data.get("deposit_amount", "50,000")
    duration = data.get("duration_months", "11")
    notice = data.get("notice_period_months", "1")
    property_addr = data.get("property_address", addr1)
    extra_terms = data.get("extra_terms", "").strip()

    if lang == "ta":
        extra_clause = f"\nகூடுதல் நிபந்தனைகள்:\n{extra_terms}\n" if extra_terms else ""
        return f"""குடியிருப்பு வாடகை ஒப்பந்த ஆவணம்
================================================================================
தேதி: {date}
இடம்: தமிழ்நாடு, இந்தியா

இந்த வாடகை ஒப்பந்தம் {date} அன்று பின்வரும் நபர்களுக்கு இடையே கையொப்பமிடப்படுகிறது:

முதல் தரப்பினர் (வீட்டு உரிமையாளர் / LANDLORD):
பெயர்: {party1}
முகவரி: {addr1}
(இனிமேல் "உரிமையாளர்" என்று குறிப்பிடப்படுவார்)

இரண்டாம் தரப்பினர் (வாடகைதாரர் / TENANT):
பெயர்: {party2}
முகவரி: {addr2}
(இனிமேல் "வாடகைதாரர்" என்று குறிப்பிடப்படுவார்)

வாடகைக்கு விடப்படும் சொத்தின் விவரம்:
முகவரி: {property_addr}

விதிமுறைகள் மற்றும் நிபந்தனைகள்:
--------------------------------------------------------------------------------
1. ஒப்பந்த காலம்: இந்த வாடகை ஒப்பந்தம் {date} முதல் தொடங்கி மொத்தம் {duration} மாதங்களுக்கு செல்லுபடியாகும். இரு தரப்பினரின் பரஸ்பர சம்மதத்துடன் இதனை நீட்டிக்கலாம்.

2. மாத வாடகை: வாடகைதாரர் ஒவ்வொரு மாதமும் ₹ {rent}/- (ரூபாய் {rent} மட்டும்) ஐ அடுத்த மாதத்தின் 5-ஆம் தேதிக்குள் உரிமையாளருக்கு செலுத்த வேண்டும்.

3. முன்வைப்புத் தொகை (Security Deposit): வாடகைதாரர் உரிமையாளரிடம் வட்டியற்ற முன்பணமாக ₹ {deposit}/- செலுத்தியுள்ளார். வாடகைக்காலம் முடிந்து வீட்டை காலி செய்யும்போது இந்த தொகை முழுமையாக திரும்ப வழங்கப்படும்.

4. பயன்பாட்டுக் கட்டணங்கள்: மின்சார கட்டணம், தண்ணீர் கட்டணம் மற்றும் பிற மாதாந்திர பராமரிப்பு கட்டணங்களை வாடகைதாரரே குறித்த காலத்தில் செலுத்த வேண்டும்.

5. பராமரிப்பு: வாடகைக்கு விடப்பட்ட வீட்டை நல்ல நிலையில் தூய்மையாக வைத்திருக்க வேண்டும். உரிமையாளரின் எழுத்துப்பூர்வ அனுமதியின்றி கட்டட அமைப்பில் எந்தவித மாற்றமும் செய்யக்கூடாது.

6. ஒப்பந்த ரத்து & முன்னறிவிப்பு: இரு தரப்பினரில் எவரேனும் இந்த ஒப்பந்தத்தை ரத்து செய்ய விரும்பினால், {notice} மாதத்திற்கு முன்னதாக எழுத்துப்பூர்வ அறிவிப்பு (Notice) அளிக்க வேண்டும்.
{extra_clause}
7. நீதித்துறை எல்லை: இந்த ஒப்பந்தம் தொடர்பான எந்தவொரு சர்ச்சைக்கும் உள்ளூர் நீதிமன்றங்களின் அதிகார வரம்பிற்கு உட்பட்டது.

சாட்சிகள் முன்னிலையில் இரு தரப்பினரும் மனப்பூர்வமாக ஏற்றுக்கொண்டு கையொப்பமிடுகின்றனர்.

கையொப்பங்கள்:


___________________________                     ___________________________
உரிமையாளர் (Landlord)                           வாடகைதாரர் (Tenant)
பெயர்: {party1}                                 பெயர்: {party2}


சாட்சிகள்:
1. பெயர் & கையொப்பம்: ____________________________________
2. பெயர் & கையொப்பம்: ____________________________________
"""
    else:
        extra_clause = f"\n7. ADDITIONAL TERMS & SPECIAL CONDITIONS:\n{extra_terms}\n" if extra_terms else ""
        return f"""RESIDENTIAL RENTAL AGREEMENT
================================================================================
Date of Execution: {date}
Jurisdiction: Local Civil Jurisdiction

This Residential Rental Agreement ("Agreement") is executed on this {date}, by and between:

FIRST PARTY (LANDLORD / LESSOR):
Name: {party1}
Permanent Address: {addr1}
(Hereinafter referred to as the "LESSOR / LANDLORD")

AND

SECOND PARTY (TENANT / LESSEE):
Name: {party2}
Permanent Address: {addr2}
(Hereinafter referred to as the "LESSEE / TENANT")

SUBJECT PROPERTY:
The premises situated at: {property_addr}

TERMS AND CONDITIONS:
--------------------------------------------------------------------------------
1. TENURE AND COMMENCEMENT:
   The tenancy shall commence on {date} and remain in effect for a period of {duration} months.

2. MONTHLY RENT:
   The Tenant agrees to pay a monthly rent of INR {rent}/- payable on or before the 5th day of every calendar month.

3. SECURITY DEPOSIT:
   The Tenant has deposited an interest-free refundable security deposit of INR {deposit}/- with the Landlord, refundable upon peaceful handover of premises.

4. UTILITY CHARGES:
   Electricity, water, and maintenance fees shall be directly paid by the Tenant according to actual metered consumption.

5. USE AND MAINTENANCE OF PREMISES:
   The premises shall be used exclusively for residential purposes in a clean and peaceful manner.

6. TERMINATION & NOTICE PERIOD:
   Either party may terminate this agreement by providing {notice} month(s) written notice.
{extra_clause}
8. GOVERNING LAW AND DISPUTE RESOLUTION:
   This Agreement shall be construed and governed by the laws of India.

IN WITNESS WHEREOF, the parties hereto have set their hands on {date}.

SIGNATURES:


___________________________                     ___________________________
LANDLORD (Lessor)                              TENANT (Lessee)
Name: {party1}                                 Name: {party2}


WITNESSES:
1. Signature: _______________________ Name & Address: ___________________________
2. Signature: _______________________ Name & Address: ___________________________
"""


def generate_nda(data: dict, lang: str = "en") -> str:
    party1 = data.get("party1_name", "Disclosing Party")
    addr1 = data.get("party1_address", "Disclosing Party Address")
    party2 = data.get("party2_name", "Receiving Party")
    addr2 = data.get("party2_address", "Receiving Party Address")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    purpose = data.get("nda_purpose", "Business discussions and technological collaboration")
    period = data.get("nda_period", "2")
    jurisdiction = data.get("jurisdiction", "Chennai, India")
    extra_terms = data.get("extra_terms", "").strip()

    if lang == "ta":
        extra_clause = f"\nகூடுதல் ஷரத்துக்கள்:\n{extra_terms}\n" if extra_terms else ""
        return f"""ரகசிய காப்பு ஒப்பந்தம் (NON-DISCLOSURE AGREEMENT)
================================================================================
தேதி: {date}
அதிகார வரம்பு: {jurisdiction}

இந்த ரகசிய காப்பு ஒப்பந்தம் {date} அன்று பின்வரும் இரு தரப்பினருக்கு இடையே செய்யப்படுகிறது:

முதல் தரப்பினர் (தகவல் வழங்கும் நபர் / DISCLOSING PARTY):
பெயர்: {party1}
முகவரி: {addr1}

இரண்டாம் தரப்பினர் (தகவல் பெறும் நபர் / RECEIVING PARTY):
பெயர்: {party2}
முகவரி: {addr2}

நோக்கம் (PURPOSE):
{purpose}

ஒப்பந்த நிபந்தனைகள்:
--------------------------------------------------------------------------------
1. ரகசியத் தகவல் வரையறை: தொழில்நுட்பம், வணிகத் திட்டங்கள், மூலக் குறியீடு மற்றும் வாடிக்கையாளர் விவரங்கள் உள்ளிட்ட அனைத்தும் ரகசியத் தகவலாகும்.

2. காப்புப் பொறுப்பு: தகவல் பெறும் நபர், வழங்கும் நபரின் முன் எழுத்துப்பூர்வ அனுமதியின்றி எந்தவொரு ரகசிய தகவலையும் வெளியிடக் கூடாது.

3. கால வரம்பு: கையெழுத்தான தேதியிலிருந்து {period} வருட காலத்திற்கு இந்த ரகசியப் பாதுகாப்பு கடமை நீடிக்கும்.
{extra_clause}
4. சட்ட வரம்பு: இந்த ஒப்பந்தம் {jurisdiction} நீதிமன்ற அதிகார வரம்பிற்கு உட்பட்டது.

கையொப்பங்கள்:


___________________________                     ___________________________
தகவல் வழங்கும் நபர்                              தகவல் பெறும் நபர்
பெயர்: {party1}                                 பெயர்: {party2}
"""
    else:
        extra_clause = f"\n5. ADDITIONAL COVENANTS:\n{extra_terms}\n" if extra_terms else ""
        return f"""NON-DISCLOSURE AGREEMENT (NDA)
================================================================================
Effective Date: {date}
Jurisdiction: {jurisdiction}

DISCLOSING PARTY:
Name: {party1}
Address: {addr1}

RECEIVING PARTY:
Name: {party2}
Address: {addr2}

PURPOSE:
"{purpose}"

TERMS:
--------------------------------------------------------------------------------
1. CONFIDENTIAL INFORMATION:
   Refers to proprietary, technical, and commercial data disclosed by the Disclosing Party.

2. OBLIGATIONS:
   The Receiving Party agrees to maintain strict confidentiality and shall not disclose information to third parties.

3. DURATION:
   Obligations survive for a period of {period} year(s) from the Effective Date.
{extra_clause}
4. GOVERNING LAW:
   Governed by the laws of India, subject to courts in {jurisdiction}.

SIGNATURES:


___________________________                     ___________________________
DISCLOSING PARTY                                RECEIVING PARTY
Name: {party1}                                 Name: {party2}
"""


def generate_affidavit(data: dict, lang: str = "en") -> str:
    party1 = data.get("party1_name", "Deponent / Declarant Name")
    addr1 = data.get("party1_address", "Deponent Address")
    age = data.get("deponent_age", "35")
    father_spouse = data.get("deponent_parent_spouse", "Father / Spouse Name")
    statement = data.get("affidavit_statement", "I state that all information provided is true and accurate.")
    purpose = data.get("affidavit_purpose", "Official submission")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    jurisdiction = data.get("jurisdiction", "Chennai, Tamil Nadu")

    if lang == "ta":
        return f"""பொது உறுதிமொழி ஆவணம் (GENERAL AFFIDAVIT)
================================================================================
தேதி: {date}
இடம்: {jurisdiction}

நான், {party1}, {father_spouse} அவர்களின் மகன்/மகள்/மனைவி, வயது {age} ஆண்டுகள், தற்போது {addr1} என்ற முகவரியில் வசித்து வருகிறேன்.

1. உறுதிமொழி அறிக்கை: {statement}

2. இந்த உறுதிமொழி ஆவணம் {purpose} என்ற நோக்கத்திற்காக சமர்ப்பிக்கப்படுகிறது.

3. இந்த ஆவணத்தில் உள்ள விவரங்கள் முற்றிலும் உண்மை என்று உறுதிசெய்து கீழே கையொப்பமிடுகிறேன்.

___________________________
உறுதிமொழி அளிப்பவர் கையொப்பம் (Deponent)
பெயர்: {party1}
"""
    else:
        return f"""GENERAL SWORN AFFIDAVIT
================================================================================
Date: {date}
Place: {jurisdiction}

I, {party1}, son/daughter/spouse of {father_spouse}, aged approximately {age} years, residing at {addr1}, do hereby solemnly affirm and state on oath:

1. STATEMENT OF FACTS:
   {statement}

2. PURPOSE:
   This Affidavit is made for the purpose of: "{purpose}".

3. VERIFICATION:
   I solemnly declare that statements made above are true and complete to the best of my knowledge.

DEPONENT SIGNATURE:


_____________________________________________
{party1}
"""


def generate_freelance_agreement(data: dict, lang: str = "en") -> str:
    party1 = data.get("party1_name", "Client Name")
    addr1 = data.get("party1_address", "Client Address")
    party2 = data.get("party2_name", "Freelancer Name")
    addr2 = data.get("party2_address", "Freelancer Address")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    scope = data.get("service_scope", "Web development & deployment")
    fee = data.get("service_fee", "45,000")
    deadline = data.get("service_deadline", "30 Days from commencement")

    if lang == "ta":
        return f"""சுயாதீன சேவை ஒப்பந்தம் (FREELANCE SERVICE AGREEMENT)
================================================================================
தேதி: {date}
வாடிக்கையாளர்: {party1} | {addr1}
சேவை வழங்குநர்: {party2} | {addr2}

பணியின் விவரம்: {scope}
கட்டணம்: ₹ {fee}/-
நிறைவு நாள்: {deadline}

இரு தரப்பினரும் ஒப்புக்கொண்டு கையொப்பமிடுகின்றனர்.

___________________________                     ___________________________
வாடிக்கையாளர் (Client)                          சேவை வழங்குநர் (Freelancer)
"""
    else:
        return f"""FREELANCE SERVICE AGREEMENT
================================================================================
Date: {date}
CLIENT: {party1}, {addr1}
CONTRACTOR: {party2}, {addr2}

1. SCOPE: {scope}
2. COMPENSATION: Total INR {fee}/-
3. TIMELINE: On or before {deadline}

SIGNATURES:


___________________________                     ___________________________
CLIENT                                          CONTRACTOR
"""


def generate_employment_letter(data: dict, lang: str = "en") -> str:
    company = data.get("party1_name", "Apex Technologies Pvt. Ltd.")
    comp_addr = data.get("party1_address", "No. 45, Tech Park, Chennai")
    candidate = data.get("party2_name", "Candidate Name")
    cand_addr = data.get("party2_address", "Candidate Address")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    designation = data.get("job_title", "Software Engineer")
    ctc = data.get("annual_ctc", "6,50,000")
    start_date = data.get("joining_date", "1st of next month")
    probation = data.get("probation_months", "3")

    if lang == "ta":
        return f"""பணி நியமனக் கடிதம் (EMPLOYMENT OFFER LETTER)
================================================================================
தேதி: {date}
நிறுவனம்: {company} | பெறுநர்: {candidate}

பதவி: {designation}
ஆண்டு ஊதியம் (CTC): ₹ {ctc}/-
இணையும் தேதி: {start_date}
தகுதிகாண் காலம்: {probation} மாதங்கள்

நன்றி மற்றும் வாழ்த்துகள்,
{company}
"""
    else:
        return f"""OFFER OF EMPLOYMENT & APPOINTMENT LETTER
================================================================================
Date: {date}
ISSUED BY: {company}, {comp_addr}
TO: {candidate}, {cand_addr}

1. POSITION: {designation}
2. COMMENCEMENT DATE: {start_date}
3. ANNUAL CTC: INR {ctc}/-
4. PROBATION PERIOD: {probation} month(s)

Yours sincerely,
For {company}
"""


def generate_promissory_note(data: dict, lang: str = "en") -> str:
    lender = data.get("party1_name", "Lender Name")
    lender_addr = data.get("party1_address", "Lender Address")
    borrower = data.get("party2_name", "Borrower Name")
    borrower_addr = data.get("party2_address", "Borrower Address")
    date = data.get("date", datetime.today().strftime("%d %B, %Y"))
    amount = data.get("loan_amount", "1,00,000")
    interest = data.get("interest_rate", "12")
    place = data.get("jurisdiction", "Chennai")

    if lang == "ta":
        return f"""கடன் உறுதிப்பத்திரம் (DEMAND PROMISSORY NOTE)
================================================================================
தொகை: ₹ {amount}/- | தேதி: {date} | இடம்: {place}

கடன் பெற்றவர்: {borrower} ({borrower_addr})
கடன் கொடுத்தவர்: {lender} ({lender_addr})

நான், {borrower}, கடன் கொடுத்தவரான {lender} அவர்களிடம் பெற்ற தொகையான ₹ {amount}/- ஐ, ஆண்டிற்கு {interest}% வட்டியுடன், அவர் கேட்கும் போது திருப்பிச் செலுத்துவதாக வாக்குறுதி அளிக்கிறேன்.

[ரெவின்யூ ஸ்டாம்ப்]
கடன் பெற்றவர் கையொப்பம்: ____________________________________
"""
    else:
        return f"""DEMAND PROMISSORY NOTE
================================================================================
Principal Amount: INR {amount}/-
Date: {date} | Place: {place}

BORROWER: {borrower}, {borrower_addr}
LENDER: {lender}, {lender_addr}

ON DEMAND, I, {borrower}, promise to pay to {lender}, or order, the principal sum of INR {amount}/-, together with simple interest at {interest}% per annum.

[Affix Revenue Stamp]
Borrower Signature: _________________________________________
"""


def build_legal_document(doc_type: str, data: dict, lang: str = "en") -> str:
    if doc_type == "Rental Agreement":
        return generate_rental_agreement(data, lang)
    elif doc_type == "Non-Disclosure Agreement (NDA)":
        return generate_nda(data, lang)
    elif doc_type == "General Affidavit":
        return generate_affidavit(data, lang)
    elif doc_type == "Freelance Service Agreement":
        return generate_freelance_agreement(data, lang)
    elif doc_type == "Employment Offer Letter":
        return generate_employment_letter(data, lang)
    elif doc_type == "Promissory Note":
        return generate_promissory_note(data, lang)
    return generate_rental_agreement(data, lang)
