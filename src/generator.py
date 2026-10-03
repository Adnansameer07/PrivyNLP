from pathlib import Path
import pandas as pd

SYNTHETIC = [
    {"id":"H01","domain":"healthcare",
     "text":"Patient Maya Rao (MRN-20481) visited Green Valley Clinic on 14/09/2026. Email: maya.rao@example.com. Phone: +91 9876543210."},
    {"id":"H02","domain":"healthcare",
     "text":"Dr. Neha Shah reviewed patient Kabir Mehta on 18/09/2026. The clinic contacted kabir.mehta@example.com at +91 9000000007."},
    {"id":"H03","domain":"healthcare",
     "text":"Patient ID: PAT-55018. Follow-up date: 2026-09-21. The record was created from IP 10.0.0.15."},
    {"id":"S01","domain":"student",
     "text":"Student Arjun Nair (USN: 1DS23AI014) registered for Data Security on 18/09/2026. Contact arjun.nair@example.com."},
    {"id":"S02","domain":"student",
     "text":"Student Priya Menon, STUDENT ID 1DS23AI022, submitted the assignment on 20/09/2026. Phone: +91 9123456789."},
    {"id":"S03","domain":"student",
     "text":"The 12-digit synthetic national identifier 123456789012 is linked to student Rahul Iyer for this academic demonstration only."},
]

def main():
    out = Path("data/synthetic_texts.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(SYNTHETIC).to_csv(out, index=False)
    print(f"Created {out}")

if __name__ == "__main__":
    main()
