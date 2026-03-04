import csv
from pathlib import Path

import requests


SOURCES = {
    "agri_dataset.07.2020.csv": "https://seshat-db.com/download_oldcsv/agri_dataset.07.2020.csv/",
    "axial_dataset.05.2018.csv": "https://seshat-db.com/download_oldcsv/axial_dataset.05.2018.csv/",
    "mr_dataset.04.2021.csv": "https://seshat-db.com/download_oldcsv/mr_dataset.04.2021.csv/",
    "CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv": "https://seshat-db.com/download_oldcsv/CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv/",
    "sc_dataset.12.2017.xlsx": "https://seshat-db.com/download_oldcsv/sc_dataset.12.2017.xlsx/",
}


def read_header(path: Path):
    raw = path.read_bytes()
    for encoding in ("utf-8", "latin-1"):
        try:
            text = raw.decode(encoding)
            return next(csv.reader(text.splitlines()))
        except Exception:
            continue
    raise RuntimeError(f"Could not decode CSV header for {path.name}")


def download_file(url: str, output: Path):
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    if not response.content:
        raise RuntimeError(f"Empty payload from {url}")

    temp = output.with_name(f".{output.name}.tmp")
    temp.write_bytes(response.content)

    if output.suffix.lower() == ".csv" and output.exists():
        if read_header(output) != read_header(temp):
            raise RuntimeError(f"Schema mismatch for {output.name}")

    temp.replace(output)
    print(f"Updated {output.name}")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    for filename, url in SOURCES.items():
        download_file(url, repo_root / filename)


if __name__ == "__main__":
    main()
