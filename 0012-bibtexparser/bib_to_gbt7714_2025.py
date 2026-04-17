# Author: slience_me
# Date: 2026/2/7 23:05
# Blog: https://slienceme.cn
import bibtexparser
from bibtexparser.bparser import BibTexParser

def format_authors(author_field):
    """
    GB/T 7714-2025:
    超过3个作者 -> et al.
    姓在前，名缩写
    """
    authors = [a.strip() for a in author_field.replace('\n', ' ').split(' and ')]
    def format_one(a):
        parts = a.split(',')
        if len(parts) == 2:
            last, first = parts
            initials = ''.join([x[0] for x in first.strip().split() if x])
            return f"{last.strip()} {initials}"
        return a

    formatted = [format_one(a) for a in authors]
    if len(formatted) > 3:
        return ', '.join(formatted[:3]) + ', et al.'
    return ', '.join(formatted)

def format_entry(entry, index):
    entry_type = entry.get('ENTRYTYPE', '')
    title = entry.get('title', '').rstrip('.')
    year = entry.get('year', '')
    authors = format_authors(entry.get('author', ''))

    if entry_type == 'article':
        journal = entry.get('journal', '')
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '').replace('--', '–')

        vol_issue = volume
        if number:
            vol_issue += f"({number})"

        return (
                f"[{index}] {authors}. {title}[J]. "
                f"{journal}, {year}"
                + (f", {vol_issue}" if vol_issue else "")
                + (f": {pages}" if pages else "")
                + "."
        )

    if entry_type in ('inproceedings', 'conference'):
        booktitle = entry.get('booktitle', '')
        pages = entry.get('pages', '').replace('--', '–')

        return (
                f"[{index}] {authors}. {title}[C]//"
                f"{booktitle}. {year}"
                + (f": {pages}" if pages else "")
                + "."
        )

    # arXiv / online
    if 'arxiv' in entry.get('journal', '').lower():
        journal = entry.get('journal', '')
        return (
            f"[{index}] {authors}. {title}[J/OL]. "
            f"{journal}, {year}."
        )

    return f"[{index}] {authors}. {title}. {year}."

def convert_bib(bib_file):
    with open(bib_file, encoding='utf-8') as f:
        parser = BibTexParser(common_strings=True)
        bib_db = bibtexparser.load(f, parser=parser)

    results = []
    for i, entry in enumerate(bib_db.entries, start=1):
        results.append(format_entry(entry, i))

    return results

if __name__ == "__main__":
    bib_path = "references.bib"   # ← 改成你的 bib 文件
    refs = convert_bib(bib_path)

    with open("references_gbt7714_2025.txt", "w", encoding="utf-8") as f:
        for r in refs:
            f.write(r + "\n\n")

    print("已生成 references_gbt7714_2025.txt")
