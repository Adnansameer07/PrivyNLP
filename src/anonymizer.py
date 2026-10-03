from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import spacy


@dataclass(frozen=True)
class Entity:
    start: int
    end: int
    label: str

    @property
    def length(self) -> int:
        return self.end - self.start


PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "PHONE": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?(?:[6-9]\d{4}[\s-]?\d{5}|[6-9]\d{3}[\s-]?\d{3}[\s-]?\d{4})(?!\d)"
    ),
    "STUDENT_ID": re.compile(
        r"\b(?:USN|STUDENT\s*ID)\s*[:#-]?\s*(?P<id>[A-Z0-9]{6,15})\b", re.I
    ),
    "PATIENT_ID": re.compile(
        r"\b(?:MRN|PATIENT\s*ID)\s*[:#-]?\s*(?P<id>[A-Z0-9-]{5,20})\b", re.I
    ),
    # Academic-demo pattern only; not an identity-number validator.
    "NATIONAL_ID": re.compile(r"(?<!\d)\d{12}(?!\d)"),
    "IP_ADDRESS": re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
    ),
    "DATE": re.compile(
        r"\b(?:0?[1-9]|[12]\d|3[01])[-/](?:0?[1-9]|1[0-2])[-/](?:19|20)\d{2}\b"
        r"|\b(?:19|20)\d{2}[-/](?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12]\d|3[01])\b"
    ),
}

DEFAULT_ANONYMIZE_NER = {"PERSON", "ORG", "GPE", "LOC", "DATE"}


class PrivacyAnonymizer:
    def __init__(
        self,
        model_name: str = "en_core_web_sm",
        anonymize_ner: Iterable[str] = DEFAULT_ANONYMIZE_NER,
    ):
        try:
            self.nlp = spacy.load(model_name)
        except OSError as exc:
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                "Run: python -m spacy download en_core_web_sm"
            ) from exc
        self.anonymize_ner = set(anonymize_ner)

    def detect(self, text: str) -> list[Entity]:
        doc = self.nlp(text)
        entities = [
            Entity(ent.start_char, ent.end_char, ent.label_)
            for ent in doc.ents
            if ent.label_ in self.anonymize_ner
        ]

        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                entities.append(Entity(match.start(), match.end(), label))

        return self._resolve_overlaps(entities)

    @staticmethod
    def _resolve_overlaps(entities: list[Entity]) -> list[Entity]:
        # Structured patterns get priority when spans overlap.
        priority = {
            "EMAIL": 100, "PHONE": 90, "STUDENT_ID": 80, "PATIENT_ID": 80,
            "NATIONAL_ID": 80, "IP_ADDRESS": 70, "DATE": 60
        }
        ordered = sorted(
            entities,
            key=lambda e: (e.start, -e.length, -priority.get(e.label, 10)),
        )
        selected = []
        for candidate in ordered:
            if any(
                candidate.start < current.end and current.start < candidate.end
                for current in selected
            ):
                continue
            selected.append(candidate)
        return sorted(selected, key=lambda e: e.start)

    def anonymize(self, text: str) -> tuple[str, pd.DataFrame]:
        entities = self.detect(text)
        counters = {}
        replacement_by_value = {}
        rows = []
        output_parts = []
        cursor = 0

        for ent in entities:
            value = text[ent.start:ent.end]
            key = (ent.label, value.lower())

            if key not in replacement_by_value:
                counters[ent.label] = counters.get(ent.label, 0) + 1
                replacement_by_value[key] = f"<{ent.label}_{counters[ent.label]}>"

            replacement = replacement_by_value[key]
            output_parts.append(text[cursor:ent.start])
            output_parts.append(replacement)
            cursor = ent.end

            rows.append({
                "label": ent.label,
                "start": ent.start,
                "end": ent.end,
                "placeholder": replacement,
            })

        output_parts.append(text[cursor:])
        report = pd.DataFrame(
            rows, columns=["label", "start", "end", "placeholder"]
        )
        return "".join(output_parts), report


def run_csv(input_path: Path, text_column: str, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path)

    if text_column not in df.columns:
        raise ValueError(
            f"Column '{text_column}' not found. Available: {list(df.columns)}"
        )

    anonymizer = PrivacyAnonymizer()
    anonymized_rows = []
    report_rows = []

    for row_id, text in enumerate(df[text_column].fillna("").astype(str), start=1):
        anonymized_text, report = anonymizer.anonymize(text)
        anonymized_rows.append({
            "row_id": row_id,
            "anonymized_text": anonymized_text,
        })
        if not report.empty:
            report = report.copy()
            report.insert(0, "row_id", row_id)
            report_rows.extend(report.to_dict("records"))

    pd.DataFrame(anonymized_rows).to_csv(
        output_dir / "anonymized_texts.csv", index=False
    )
    pd.DataFrame(
        report_rows,
        columns=["row_id", "label", "start", "end", "placeholder"],
    ).to_csv(output_dir / "detection_report.csv", index=False)

    print(f"Saved: {output_dir / 'anonymized_texts.csv'}")
    print(f"Saved: {output_dir / 'detection_report.csv'}")


def interactive() -> None:
    anonymizer = PrivacyAnonymizer()
    print("Privacy-Preserving NLP for Sensitive Text")
    print("Enter synthetic text. Empty input exits.\n")

    while True:
        text = input("Text: ").strip()
        if not text:
            break

        anonymized, report = anonymizer.anonymize(text)
        print("\nDetected:")
        print(
            "No in-scope sensitive entities detected."
            if report.empty
            else report.to_string(index=False)
        )
        print("\nAnonymized:")
        print(anonymized)
        print("-" * 70)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    if args.csv:
        run_csv(args.csv, args.text_column, args.output_dir)
    else:
        interactive()


if __name__ == "__main__":
    main()
