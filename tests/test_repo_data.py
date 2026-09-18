# -*- coding: utf-8 -*-
"""Kiem tra toan ven du lieu that trong data/ — bat loi merge hong hoac sua tay."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import vocab_tool  # noqa: E402

DATA_FILES = [
    ("data/vocabulary.en.csv", vocab_tool.VOCAB_FIELDS, "term"),
    ("data/vocabulary.ja.csv", vocab_tool.VOCAB_FIELDS, "term"),
    ("data/books.csv", vocab_tool.BOOK_FIELDS, "title"),
]


def load(relative: str):
    path = REPO_ROOT / relative
    if not path.exists():
        pytest.skip(f"{relative} chưa tồn tại — chạy `vocab_tool.py init`")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


@pytest.mark.parametrize(("relative", "fields", "key"), DATA_FILES)
def test_header_matches_schema(relative: str, fields: list, key: str) -> None:
    header, _ = load(relative)
    assert header == fields, f"{relative}: cột không khớp schema của vocab_tool"


@pytest.mark.parametrize(("relative", "fields", "key"), DATA_FILES)
def test_ids_are_unique_positive_integers(relative: str, fields: list, key: str) -> None:
    _, rows = load(relative)
    ids = [row["id"] for row in rows]
    assert all(value.isdigit() and int(value) > 0 for value in ids), \
        f"{relative}: có id không phải số nguyên dương"
    assert len(set(ids)) == len(ids), f"{relative}: id trùng nhau (merge hỏng?)"


@pytest.mark.parametrize(("relative", "fields", "key"), DATA_FILES)
def test_keys_are_present_and_unique(relative: str, fields: list, key: str) -> None:
    _, rows = load(relative)
    keys = [vocab_tool._norm_key(row[key]) for row in rows]
    assert all(keys), f"{relative}: có dòng thiếu '{key}'"
    assert len(set(keys)) == len(keys), f"{relative}: '{key}' bị trùng"


def test_english_sheet_has_no_japanese_terms() -> None:
    _, rows = load("data/vocabulary.en.csv")
    misplaced = [row["term"] for row in rows if vocab_tool.detect_lang(row["term"]) == "ja"]
    assert not misplaced, f"từ tiếng Nhật nằm nhầm trong file EN: {misplaced}"
