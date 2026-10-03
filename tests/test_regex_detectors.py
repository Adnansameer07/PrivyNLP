from src.anonymizer import PATTERNS

def test_email():
    assert PATTERNS["EMAIL"].search("maya.rao@example.com").group(0) == "maya.rao@example.com"

def test_phone():
    assert PATTERNS["PHONE"].search("+91 9876543210").group(0) == "+91 9876543210"

def test_student_id():
    m = PATTERNS["STUDENT_ID"].search("USN: 1DS23AI014")
    assert m.group("id") == "1DS23AI014"

def test_patient_id():
    m = PATTERNS["PATIENT_ID"].search("MRN-20481")
    assert m.group(0) == "MRN-20481"

def test_ip():
    assert PATTERNS["IP_ADDRESS"].search("10.0.0.15").group(0) == "10.0.0.15"
