#!/usr/bin/env python3
import json
import re
from collections import defaultdict
from datetime import datetime

def load_doaj_results(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def categorize_by_era(paper):
    abstract = paper.get('bibjson', {}).get('abstract', '').lower()
    keywords = ' '.join(paper.get('bibjson', {}).get('keywords', [])).lower()
    title = paper.get('bibjson', {}).get('title', '').lower()
    year = paper.get('bibjson', {}).get('year', '')
    content = f"{title} {abstract} {keywords}".lower()

    early_indicators = ['wilde', 'aestheticism', 'decadence', 'fin de siècle', 'symbolism', 'pater', 'beardsley', 'symons']
    high_indicators = ['pound', 'eliot', 'joyce', 'woolf', 'yeats', 'imagism', 'vorticism', 'stream of consciousness', 'waste land', 'ulysses']
    late_indicators = ['auden', 'spender', 'isherwood', 'macneice', 'thirties', '1930s', 'spanish civil war', 'world war ii']

    early_count = sum(1 for indicator in early_indicators if indicator in content)
    high_count = sum(1 for indicator in high_indicators if indicator in content)
    late_count = sum(1 for indicator in late_indicators if indicator in content)

    if early_count > high_count and early_count > late_count:
        return 'Early Modernism (1890s-1910s)'
    elif high_count > early_count and high_count > late_count:
        return 'High Modernism (1910s-1920s)'
    elif late_count > early_count and late_count > high_count:
        return 'Late Modernism (1930s-1950s)'
    else:
        return 'General Modernism'

def categorize_by_medium(paper):
    journal_info = paper.get('bibjson', {}).get('journal', {})
    journal_title = journal_info.get('title', '').lower()
    publisher = journal_info.get('publisher', '').lower()
    content = f"{journal_title} {publisher}"

    if any(word in content for word in ['journal', 'review', 'studies', 'quarterly', 'university', 'research']):
        return 'Academic Journal'
    elif any(word in content for word in ['magazine', 'letters', 'writing', 'poetry', 'literature', 'arts']):
        return 'Literary Magazine'
    else:
        return 'Other Publication'

def extract_metadata_for_analysis(paper):
    bibjson = paper.get('bibjson', {})
    return {
        'id': paper.get('id'),
        'title': bibjson.get('title', ''),
        'authors': [author.get('name', '') for author in bibjson.get('author', [])],
        'year': bibjson.get('year', ''),
        'journal': bibjson.get('journal', {}).get('title', ''),
        'publisher': bibjson.get('journal', {}).get('publisher', ''),
        'country': bibjson.get('journal', {}).get('country', ''),
        'keywords': bibjson.get('keywords', []),
        'abstract': bibjson.get('abstract', ''),
        'doi': next((id['id'] for id in bibjson.get('identifier', []) if id.get('type') == 'doi'), None),
        'full_text_links': [link['url'] for link in bibjson.get('link', []) if link.get('type') == 'fulltext'],
        'subjects': [subj.get('term', '') for subj in bibjson.get('subject', [])]
    }

def analyze_doaj_modernism(filename):
    data = load_doaj_results(filename)
    era_categories = defaultdict(list)
    medium_categories = defaultdict(list)
    all_papers_metadata = []

    for paper in data['results']:
        era = categorize_by_era(paper)
        medium = categorize_by_medium(paper)
        metadata = extract_metadata_for_analysis(paper)

        era_categories[era].append(metadata)
        medium_categories[medium].append(metadata)
        all_papers_metadata.append({**metadata, 'era': era, 'medium': medium})

    print(f"Total papers found: {data['total']}")
    print(f"\n=== BY MODERNIST ERA ===")
    for era, papers in era_categories.items():
        print(f"\n{era}: {len(papers)} papers")
        for paper in papers[:2]:
            print(f"  • {paper['title'][:60]}... ({paper['year']})")

    print(f"\n=== BY PUBLICATION MEDIUM ===")
    for medium, papers in medium_categories.items():
        print(f"\n{medium}: {len(papers)} papers")
        journals = set(paper['journal'] for paper in papers if paper['journal'])
        for journal in sorted(journals)[:3]:
            print(f"  - {journal}")

    return {'era_categories': dict(era_categories), 'medium_categories': dict(medium_categories), 'all_metadata': all_papers_metadata}

if __name__ == "__main__":
    results = analyze_doaj_modernism('modernism_search.json')
    with open('british_modernism_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nAnalysis saved to 'british_modernism_analysis.json'")