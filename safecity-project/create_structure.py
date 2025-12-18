from pathlib import Path

# Root = current working directory (safecity-dashboard)
ROOT = Path.cwd()

# ------------------------
# Directories to create
# ------------------------
DIRECTORIES = [
    "pipeline",
    "utils",
    "data/raw/crimes",
    "data/raw/population",
    "data/raw/geo",
    "data/processed",
    "reports/examples",
    "reports/exports",
    "notebooks",
    "tests",
    "assets",
]

# ------------------------
# Files to create
# ------------------------
FILES = [
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "README.md",
    "app.py",

    # pipeline
    "pipeline/__init__.py",
    "pipeline/extract.py",
    "pipeline/transform.py",
    "pipeline/enrich.py",
    "pipeline/validate.py",
    "pipeline/run.py",

    # utils
    "utils/__init__.py",
    "utils/data.py",
    "utils/metrics.py",
    "utils/charts.py",
    "utils/geo.py",
    "utils/llm.py",
    "utils/analysis.py",
    "utils/chatbot.py",

    # data (placeholders only – no real data overwritten)
    "data/raw/crimes/.gitkeep",
    "data/raw/population/.gitkeep",
    "data/raw/geo/.gitkeep",

    "data/processed/.gitkeep",

    # reports
    "reports/examples/.gitkeep",
    "reports/exports/.gitkeep",

    # notebooks
    "notebooks/exploration.ipynb",

    # tests
    "tests/test_pipeline.py",
    "tests/test_metrics.py",

    # assets
    "assets/logo.png",
    "assets/styles.css",
]


def create_directories():
    for d in DIRECTORIES:
        path = ROOT / d
        path.mkdir(parents=True, exist_ok=True)


def create_files():
    for f in FILES:
        path = ROOT / f
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            if path.suffix == ".ipynb":
                path.write_text(
                    """{
  "cells": [],
  "metadata": {},
  "nbformat": 4,
  "nbformat_minor": 5
}"""
                )
            else:
                path.touch()


def main():
    print("🚀 Creating SafeCity Dashboard structure...")
    create_directories()
    create_files()
    print("✅ Project structure created successfully")


if __name__ == "__main__":
    main()
