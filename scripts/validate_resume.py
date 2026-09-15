#!/usr/bin/env python3
"""Validate the deliverable and the two explicitly preserved user requirements."""
from pathlib import Path
import hashlib
import re
import sys

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_SHA256 = "80e4346f960394b1a0edd6b02e3014d3469210cef29bb71cb5f16e700c6bb828"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(text):
    return " ".join(text.split())


def validate():
    source = (ROOT / "sections/summary.tex").read_text()
    summary = source.split("\\section{Executive Summary}\n", 1)[1]
    summary = re.sub(r"\\textbf\{([^}]+)\}", r"\1", summary).replace(r"\&", "&")
    check(hashlib.sha256(normalize(summary).encode()).hexdigest() == SUMMARY_SHA256,
          "The approved UM-SEM-5-2 summary changed. Restore its exact wording.")
    check(not (ROOT / "resumes").exists(), "Obsolete resume variants must not return.")
    check(not (ROOT / ".github/workflows/compile-resume.yml").exists(), "Old release workflow remains.")

    pdf = ROOT / "build/Utkarsh-Mankad-Resume.pdf"
    reader = PdfReader(pdf)
    check(len(reader.pages) == 2, f"Expected two pages, got {len(reader.pages)}.")
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)
    (ROOT / "build/resume.txt").write_text(text)
    flat = normalize(text)
    for token in ["Utkarsh Mankad", "utkarsh.mankad@gmail.com", "+91 8095173074",
                  "Professional Experience Snapshot", "Independent AI Engineering Projects",
                  "Jan 2025", "Apr 2026", "ISHA", "ReportAPI Self-Hosted", "ClaudeWatch",
                  "Scientist D", "2019", "2009", "AWS", "TypeScript"]:
        check(token in flat, f"Missing PDF content: {token}")
    headings = ["Executive Summary", "Professional Experience Snapshot", "Core Competencies",
                "Independent AI Engineering Projects", "Professional Experience\n",
                "Earlier Experience", "Education"]
    positions = [text.index(h) for h in headings]
    check(positions == sorted(positions), "PDF section reading order is incorrect.")
    extracted = text.split("Executive Summary", 1)[1].split("Professional Experience Snapshot", 1)[0]
    check(re.sub(r"\s", "", extracted) == re.sub(r"\s", "", summary),
          "PDF summary differs from approved source text.")
    check("\ufffd" not in text and "\x00" not in text, "PDF contains broken/replacement glyphs.")
    check(len(re.findall(r"70\s*%", text)) == 1, "70% achievement must appear exactly once.")
    oracle = (ROOT / "sections/oracle.tex").read_text()
    check("Present" not in oracle, "Oracle must end in Apr 2026.")
    check("Fynd" in pages[1].splitlines()[0], "Fynd must start cleanly on page two.")
    for page in reader.pages:
        check(abs(float(page.mediabox.width) - 595.28) < 2, "Expected A4 paper.")
        fonts = page["/Resources"]["/Font"].get_object()
        for ref in fonts.values():
            font = ref.get_object()
            check("/ToUnicode" in font, "A font lacks Unicode text mapping.")
            base = font.get("/DescendantFonts", [ref])[0].get_object()
            descriptor = base.get("/FontDescriptor")
            check(descriptor is not None, "A font lacks its descriptor.")
            check(any(k in descriptor.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3")),
                  "A font is not embedded.")
    all_tex = "\n".join(p.read_text() for p in (ROOT / "sections").glob("*.tex"))
    items = [normalize(x) for x in re.findall(r"\\item (.*)", all_tex)]
    check(len(items) == len(set(items)), "Duplicate resume bullets detected.")
    log = (ROOT / "build/main.log").read_text(errors="replace")
    check(not re.search(r"Overfull \\[hv]box|Missing character:", log), "Layout overflow or missing glyph: review main.log.")
    print("PASS: two A4 pages; exact summary; snapshot retained; ordered text; embedded Unicode fonts; no overflow; one 70% claim.")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, KeyError, IndexError) as exc:
        sys.exit(f"Resume validation failed: {exc}")
