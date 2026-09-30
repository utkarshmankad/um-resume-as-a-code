#!/usr/bin/env python3
"""Validate the deliverable and the explicitly protected user requirements."""
from pathlib import Path
import hashlib
import re
import sys
import unicodedata

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
COMPETENCIES_SHA256 = "edcfe8d26637132e899ca722879db35db597ab99bc23b520b7f6734d3f865862"
SUMMARY_SHA256 = "80e4346f960394b1a0edd6b02e3014d3469210cef29bb71cb5f16e700c6bb828"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(text):
    return " ".join(text.split())


def validate_protected_sources(root=ROOT):
    """Check approved wording before compiling or reading a PDF.

    Hashes ignore source line wrapping only. An intentional content change needs
    owner review before its baseline is updated.
    """
    competencies = (root / "sections/competencies.tex").read_text()
    check(hashlib.sha256(normalize(competencies).encode()).hexdigest() == COMPETENCIES_SHA256,
          "The approved Core Competencies changed. Restore its complete wording and order.")
    source = (root / "sections/summary.tex").read_text()
    summary = source.split("\\section{Executive Summary}\n", 1)[1]
    summary = re.sub(r"\\textbf\{([^}]+)\}", r"\1", summary).replace(r"\&", "&")
    check(hashlib.sha256(normalize(summary).encode()).hexdigest() == SUMMARY_SHA256,
          "The approved UM-SEM-5-2 summary changed. Restore its exact wording.")
    return summary


def validate():
    summary = validate_protected_sources()
    check(not (ROOT / "resumes").exists(), "Obsolete resume variants must not return.")
    check(not (ROOT / ".github/workflows/compile-resume.yml").exists(), "Old release workflow remains.")

    pdf = ROOT / "build/Utkarsh-Mankad-Resume.pdf"
    reader = PdfReader(pdf)
    check(len(reader.pages) == 2, f"Expected two pages, got {len(reader.pages)}.")
    # Layout extraction respects CM-Super kerning; NFKC expands standard fi/fl ligatures.
    pages = ["\n".join(line.strip() for line in unicodedata.normalize(
        "NFKC", page.extract_text(extraction_mode="layout") or "").splitlines())
        for page in reader.pages]
    text = "\n".join(pages)
    (ROOT / "build/resume.txt").write_text(text)
    flat = normalize(text)
    # Protect the corrections agreed during review, including PDF extraction.
    check("Senior Engineering Manager | Platform, Data & Applied AI" in flat,
          "The approved Senior Engineering Manager headline changed.")
    snapshot = normalize(text.split("Professional Experience Snapshot", 1)[1]
                         .split("Core Competencies", 1)[0])
    for entry in [
        "Oracle – Jan 2025 to Apr 2026 – Engineering Manager (Software Development Manager)",
        "Fynd (Reliance Industries Ltd) – Dec 2021 to Dec 2024 – Engineering Manager, Platform & Integrations",
        "CDAC (Ministry of Electronics & IT, Government of India) – Aug 2010 to Nov 2021 – SDE2 to SDE3 to Engineering Manager",
    ]:
        check(entry in snapshot, f"Approved snapshot entry changed: {entry}")
    experience = text.split("Professional Experience\n", 1)[1]
    oracle_text, later = experience.split("Fynd (Reliance Industries Ltd)", 1)
    fynd_text, cdac_text = later.split("Earlier Experience", 1)
    for employer, section, facts in [
        ("Oracle", oracle_text, ["14 production", "2 sub-teams", "VECTOR and JSON", "CRUD API",
                                "70%", "FIPS 140-3 certification", "US and UK", "85%+",
                                "Jira Service Desk", "issues 30%", "burden 30%", "customer calls",
                                "Jira epics and stories", "Apr 2026"]),
        ("Fynd", fynd_text, ["Directly managed 20", "8 EMs", "without formal authority", "3M+ SKUs",
                            "5M+ active merchants", "zero downtime", "5 to 20", "less than 5%",
                            "bronze layer", "velocity 20%", "detection 40%", "24 months",
                            "one-year roadmap", "Product Listing Page (PLP)", "Coralogix",
                            "NewRelic", "Sentry", "PagerDuty", "OpenTelemetry"]),
        ("CDAC", cdac_text, ["40 locations", "4 states", "1.2M+", "12 engineers", "PIPs",
                            "separations", "Rs.300 Cr+", "5 concurrent", "Rs.250 Cr", "NASSCOM",
                            "10+", "50+ institutions", "3 cities", "Rs.50L+", "8,000 sensors",
                            "45GB/day", "2-person team to 7", "Smart Post Kiosk", "EPFO",
                            "SDE2 & SDE3 – Individual Contributor to Technical Architect"]),
    ]:
        section = normalize(section)
        for fact in ["Product Summary:", "Leadership Scope:", "Tech Stack:"] + facts:
            check(fact in section, f"Protected {employer} content missing: {fact}")
    check("supported Docker Compose deployment" in flat and
          "experimental/incomplete Helm configuration" in flat,
          "ReportAPI deployment maturity must be explicit.")
    for token in ["Utkarsh Mankad", "utkarsh.mankad@gmail.com", "+91 8095173074",
                  "Professional Experience Snapshot", "Independent AI Engineering Projects",
                  "Jan 2025", "Apr 2026", "ISHA", "ReportAPI Self-Hosted", "ClaudeWatch",
                  "SDE2 to SDE3 to Engineering Manager", "2019", "2009", "AWS", "TypeScript"]:
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
