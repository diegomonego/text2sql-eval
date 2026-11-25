"""Build benchmark databases with DuckDB's data generators, and fetch the TPC-H specification."""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

from .config import Config
from .meta import sha256_file

GENERATORS = {"tpch": ("tpch", "dbgen"), "tpcds": ("tpcds", "dsdgen")}


def build_database(benchmark: str, sf: float, out: Path) -> str:
    import duckdb

    if benchmark not in GENERATORS:
        raise ValueError(f"unknown benchmark '{benchmark}' (choose from {', '.join(GENERATORS)})")
    ext, fn = GENERATORS[benchmark]
    out.parent.mkdir(parents=True, exist_ok=True)
    for p in (out, out.with_suffix(out.suffix + ".wal")):
        if p.exists():
            p.unlink()
    con = duckdb.connect(str(out))
    con.execute(f"INSTALL {ext}; LOAD {ext}; CALL {fn}(sf = {float(sf)});")
    tables = con.execute("SELECT table_name, estimated_size FROM duckdb_tables() ORDER BY 1").fetchall()
    con.close()
    lines = [f"Built {benchmark} sf={sf} with DuckDB {duckdb.__version__} into {out}"]
    lines += [f"  {t}: ~{n:,} rows" for t, n in tables]
    return "\n".join(lines)


# Sections of the TPC-H spec given to the agents: business environment, entities and table layouts
# (clause 1.1-1.4) and the data generation rules that define every column's values (clause 4.2.2-4.2.3).
# Clause 2 (the 22 benchmark queries) is deliberately left out.
SPEC_SECTIONS = [
    ("clause1_database_design.md", "1.1 Business and Application Environment", "1.5 Implementation Rules",
     "Clause 1.1-1.4: business environment, entities, relationships, datatypes and table layouts"),
    ("clause4_data_generation.md", "4.2.2 Definition Of Terms", "4.2.4 Refresh Function Data Generation",
     "Clause 4.2.2-4.2.3: definition of terms and the rules that generate every column's values"),
]
FOOTER = re.compile(r"TPC Benchmark\s*TM\s*H Standard Specification Revision [\d.]+\s*Page \d+", re.I)


def fetch_spec(cfg: Config) -> str:
    from pypdf import PdfReader

    if not cfg.spec_url:
        raise ValueError("no [spec] url in config/eval.toml")
    pdf = cfg.root / "downloads" / Path(cfg.spec_url).name
    pdf.parent.mkdir(parents=True, exist_ok=True)
    if not pdf.exists():
        urllib.request.urlretrieve(cfg.spec_url, pdf)
    sha = sha256_file(pdf)
    if cfg.spec_sha256 and sha != cfg.spec_sha256:
        raise ValueError(f"checksum mismatch for {pdf.name}: got {sha}, expected {cfg.spec_sha256}")
    reader = PdfReader(str(pdf))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = FOOTER.sub("", text)
    out_dir = cfg.docs_dir / "spec"
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for fname, start, end, title in SPEC_SECTIONS:
        i, j = text.find(start), text.find(end, text.find(start) + 1)
        if i < 0 or j < 0:
            raise ValueError(f"could not find section '{start}' in {pdf.name}")
        body = re.sub(r"\n{3,}", "\n\n", text[i:j]).strip()
        header = (
            f"# TPC-H specification excerpt: {title}\n\n"
            f"Source: {cfg.spec_url} (sha256 {sha}). Text extracted automatically from the PDF, so tables "
            f"may have lost their layout. The 22 benchmark queries (clause 2) are deliberately not included.\n\n"
        )
        (out_dir / fname).write_text(header + body + "\n")
        lines.append(f"Wrote {out_dir / fname} ({len(body):,} characters)")
    return "\n".join(lines)
