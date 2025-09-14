#!/usr/bin/env python3
import json
import csv
from datetime import datetime

def load_analysis_results():
    with open('british_modernism_analysis.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_csv_for_analysis(results):
    """Create CSV format suitable for text analysis tools like R, Python pandas, etc."""
    csv_data = []

    for paper in results['all_metadata']:
        row = {
            'id': paper['id'],
            'title': paper['title'],
            'authors': '; '.join(paper['authors']),
            'year': paper['year'],
            'era': paper['era'],
            'journal': paper['journal'],
            'publisher': paper['publisher'],
            'country': paper['country'],
            'medium': paper['medium'],
            'keywords': '; '.join(paper['keywords']),
            'abstract': paper['abstract'].replace('\n', ' ').replace('\r', ' '),
            'doi': paper.get('doi', ''),
            'full_text_links': '; '.join(paper['full_text_links']),
            'subjects': '; '.join(paper['subjects']),
            'abstract_length': len(paper['abstract']),
            'has_doi': 'Yes' if paper.get('doi') else 'No',
            'has_full_text': 'Yes' if paper['full_text_links'] else 'No',
            'keyword_count': len(paper['keywords'])
        }
        csv_data.append(row)

    with open('british_modernism_for_analysis.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = csv_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

def create_structured_output(results):
    """Create comprehensive structured output"""
    output = {
        'metadata': {
            'extraction_date': datetime.now().isoformat(),
            'total_papers_in_doaj': 84,
            'papers_analyzed': len(results['all_metadata']),
            'search_query': 'modernism British',
            'database': 'DOAJ (Directory of Open Access Journals)',
            'categories': {
                'by_era': list(results['era_categories'].keys()),
                'by_medium': list(results['medium_categories'].keys())
            }
        },
        'summary_statistics': {
            'era_distribution': {era: len(papers) for era, papers in results['era_categories'].items()},
            'medium_distribution': {medium: len(papers) for medium, papers in results['medium_categories'].items()},
            'year_range': {
                'earliest': min(int(p['year']) for p in results['all_metadata'] if p['year'].isdigit()),
                'latest': max(int(p['year']) for p in results['all_metadata'] if p['year'].isdigit())
            },
            'countries_represented': len(set(p['country'] for p in results['all_metadata'] if p['country'])),
            'journals_represented': len(set(p['journal'] for p in results['all_metadata'] if p['journal'])),
            'papers_with_full_text': len([p for p in results['all_metadata'] if p['full_text_links']]),
            'papers_with_doi': len([p for p in results['all_metadata'] if p.get('doi')])
        },
        'organized_by_era': results['era_categories'],
        'organized_by_medium': results['medium_categories'],
        'text_analysis_ready': {
            'all_abstracts': [{'id': p['id'], 'title': p['title'], 'abstract': p['abstract'],
                              'era': p['era'], 'year': p['year']} for p in results['all_metadata']],
            'all_keywords': [{'id': p['id'], 'title': p['title'], 'keywords': p['keywords'],
                             'era': p['era'], 'year': p['year']} for p in results['all_metadata']],
            'full_text_available': [p for p in results['all_metadata'] if p['full_text_links']]
        }
    }

    with open('british_modernism_comprehensive.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def create_era_specific_files(results):
    """Create separate files for each era"""
    for era, papers in results['era_categories'].items():
        filename = f"era_{era.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')}.json"
        era_data = {
            'era': era,
            'paper_count': len(papers),
            'papers': papers
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(era_data, f, indent=2, ensure_ascii=False)

def create_readme():
    """Create README explaining the data structure"""
    readme_content = """# British Modernist Literature Papers from DOAJ

## Files Created:

1. **british_modernism_comprehensive.json** - Complete dataset with metadata and analysis
2. **british_modernism_for_analysis.csv** - CSV format for statistical analysis
3. **era_*.json** - Separate files for each modernist era
4. **modernism_search.json** - Original DOAJ API response

## Data Structure:

### Era Categories:
- **Early Modernism (1890s-1910s)**: Pre-war experimental beginnings
- **High Modernism (1910s-1920s)**: Peak experimental period
- **Late Modernism (1930s-1950s)**: Institutionalization and response to crisis
- **General Modernism**: Papers that don't fit specific era categories

### Publication Medium Categories:
- **Academic Journal**: Scholarly peer-reviewed journals
- **Literary Magazine**: Literary and cultural magazines
- **Other Publication**: Books, series, and other publication types

### Metadata Fields:
- **Bibliographic**: title, authors, year, journal, publisher, country
- **Content**: abstract, keywords, subjects
- **Access**: DOI, full-text links
- **Categorization**: era, medium classification

## Usage for Text Analysis:

### CSV File (british_modernism_for_analysis.csv):
- Import into R, Python pandas, Excel, or other analysis tools
- Ready for statistical analysis and visualization
- All text fields cleaned for analysis

### JSON Files:
- Programmatic access to structured data
- Preserve original data types and nested structures
- Full metadata preservation

### Text Corpus:
- Abstracts available for content analysis
- Keywords extracted for topic modeling
- Full-text links provided where available

## Search Details:
- Source: DOAJ (Directory of Open Access Journals)
- Query: "modernism British"
- Total papers in DOAJ: 84
- Papers analyzed: 84
- Extraction date: [timestamp in comprehensive.json]

## Next Steps for Analysis:
1. Topic modeling using abstracts and keywords
2. Citation network analysis using DOIs
3. Temporal analysis of modernist scholarship trends
4. Geographic distribution of modernist research
5. Full-text analysis where available
"""

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    results = load_analysis_results()

    print("Creating analysis-ready formats...")
    create_csv_for_analysis(results)
    print("✓ CSV file created: british_modernism_for_analysis.csv")

    create_structured_output(results)
    print("✓ Comprehensive JSON created: british_modernism_comprehensive.json")

    create_era_specific_files(results)
    print("✓ Era-specific files created")

    create_readme()
    print("✓ README.md created with documentation")

    print("\nFiles ready for text analysis:")
    print("- british_modernism_for_analysis.csv (for statistical tools)")
    print("- british_modernism_comprehensive.json (complete dataset)")
    print("- era_*.json files (era-specific subsets)")
    print("- README.md (documentation)")