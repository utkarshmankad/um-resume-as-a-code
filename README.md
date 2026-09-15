# Utkarsh Mankad — Resume as Code

One canonical resume for engineering-management roles in platform, data, and applied AI.

## Content

`main.tex` defines the document order. `resume.sty` owns the layout; `sections/` contains each section exactly once. Edit these sources rather than maintaining company-specific resumes.

The Executive Summary reproduces **UM-SEM-5-2 verbatim**. The **Professional Experience Snapshot is retained**. The validator protects both requirements. Its summary hash ignores line-wrap whitespace, but detects wording and punctuation changes.

The employment content uses the approved conservative wording: Oracle ends April 2026; Fynd's team growth is 5 to 20 without the inconsistent per-function breakdown; CDAC's INR 300 crore figure describes proposal/opportunity scope; the M.Tech year follows the latest PDF (2019). Independent projects are ISHA, ReportAPI Self-Hosted, and ClaudeWatch. Project code supports implementation claims, not adoption or revenue claims.

## Build locally

Requirements: **Tectonic 0.17.0**, Python 3.10+, and **pypdf 6.10.0**. Install the compiler from the [official release](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0). The workflow verifies the Linux archive checksum. Tectonic supplies the XeTeX engine and downloads its versioned v33 LaTeX/font bundle on first use; subsequent builds use the local cache. No system-font dependency is required.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pypdf==6.10.0
bash scripts/build.sh
```

For a compiler outside PATH, set `TECTONIC=/absolute/path/to/tectonic`. Set `PYTHON` to choose the Python executable.

Outputs (ignored by Git):

- `build/Utkarsh-Mankad-Resume.pdf`
- `build/resume.txt`
- `build/main.log`

The validator checks two A4 pages, exact summary wording, snapshot presence, section ordering, embedded Unicode fonts, required contact/date content, no obsolete variants, no overflow/missing characters, and a single occurrence of the 70% result.

## Visual review

On a system with Poppler:

```sh
pdftoppm -scale-to 1600 -png build/Utkarsh-Mankad-Resume.pdf build/page
```

Inspect both pages at readable size. Check headings, line breaks, whitespace, contact links, and the Fynd page break. Automated text checks do not replace visual review or verify the underlying career claims.

## Pull requests and publication

Open a PR against `main`. GitHub Actions uses the same build script, validates the PDF, and uploads a **resume-review** bundle with the PDF, extracted text, and page images. Review artifacts expire after one day; rerun a build for a fresh preview. No generated PDF is committed.

After reviewing and merging the resume, run **Build Resume → Run workflow → main**, selecting **publish**. The publish job verifies that main has not moved and replaces the PDF on the single `latest` release. Ordinary pushes and PRs only build; they do not publish. The build has read-only permissions; only the manually requested publish job has write access.

The stable download after first publication is:

[Current resume](https://github.com/utkarshmankad/um-resume-as-a-code/releases/latest/download/Utkarsh-Mankad-Resume.pdf)

## One-resume policy

Do not add a variants directory, archived PDFs, company copies, or dated backup tags. Keep only the current published resume. The approved transition removes the old application branches, nine historical releases and their tags after the replacement is accepted. Normal Git commit history is not rewritten; it remains the change history, not a maintained alternate resume.

Other repositories and portfolio downloads are outside this repository's build and cleanup scope.
