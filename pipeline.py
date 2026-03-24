"""Study Overlap Detector: finds primary studies appearing in multiple Cochrane reviews.

Quantifies the non-independence problem for umbrella reviews / overviews of reviews.
Computes the Corrected Covered Area (CCA) metric.

Usage: python pipeline.py
"""

import json
import csv
import time
import pyreadr
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict

PAIRWISE_DIR = r'C:\Models\Pairwise70\data'
OUTPUT_DIR = r'C:\OverlapDetector\data\output'


def load_all_studies(pairwise_dir):
    """Load all studies from all 501 RDA files, returning study-to-review mapping."""
    study_reviews = defaultdict(set)  # study_key -> set of review_ids
    review_studies = defaultdict(set)  # review_id -> set of study_keys
    review_names = {}

    pairwise_path = Path(pairwise_dir)
    for rda in sorted(pairwise_path.glob('*.rda')):
        review_id = rda.stem.split('_')[0]
        try:
            result = pyreadr.read_r(str(rda))
            df = list(result.values())[0]
            df.columns = df.columns.str.replace(' ', '.', regex=False)

            for _, row in df.iterrows():
                study = str(row.get('Study', ''))
                year = row.get('Study.year', '')
                if not study:
                    continue
                # Normalize study key: "Author Year" format
                key = study.strip().lower()
                study_reviews[key].add(review_id)
                review_studies[review_id].add(key)

            # Store first analysis name
            if 'Analysis.name' in df.columns and len(df) > 0:
                review_names[review_id] = str(df['Analysis.name'].iloc[0])
        except Exception:
            continue

    return study_reviews, review_studies, review_names


def compute_cca(review_studies):
    """Compute Corrected Covered Area (CCA) for the full review set.

    CCA = (N - r) / (rc - r)
    where:
    - N = total citations (sum of study counts across reviews, counting duplicates)
    - r = number of unique studies
    - c = number of reviews
    """
    all_studies = set()
    total_citations = 0
    c = len(review_studies)

    for studies in review_studies.values():
        total_citations += len(studies)
        all_studies.update(studies)

    r = len(all_studies)
    denom = r * c - r
    if denom <= 0:
        return 0.0
    cca = (total_citations - r) / denom
    return cca


def compute_pairwise_overlap(review_studies):
    """Compute overlap matrix between all pairs of reviews."""
    review_ids = sorted(review_studies.keys())
    overlaps = []

    for i in range(len(review_ids)):
        for j in range(i + 1, len(review_ids)):
            r1, r2 = review_ids[i], review_ids[j]
            shared = review_studies[r1] & review_studies[r2]
            if len(shared) > 0:
                # Jaccard: |A intersect B| / |A union B|
                union = review_studies[r1] | review_studies[r2]
                jaccard = len(shared) / len(union) if len(union) > 0 else 0
                overlaps.append({
                    'review_1': r1,
                    'review_2': r2,
                    'n_shared': len(shared),
                    'n_r1': len(review_studies[r1]),
                    'n_r2': len(review_studies[r2]),
                    'jaccard': round(jaccard, 4),
                    'pct_r1': round(len(shared) / len(review_studies[r1]) * 100, 1),
                    'pct_r2': round(len(shared) / len(review_studies[r2]) * 100, 1),
                })

    return sorted(overlaps, key=lambda x: -x['n_shared'])


def main():
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Study Overlap Detector")
    print("=" * 30)

    t0 = time.time()
    study_reviews, review_studies, review_names = load_all_studies(PAIRWISE_DIR)
    elapsed_load = time.time() - t0
    print(f"  Loaded {len(review_studies)} reviews, {len(study_reviews)} unique studies in {elapsed_load:.1f}s")

    # Studies appearing in multiple reviews
    multi_review_studies = {k: v for k, v in study_reviews.items() if len(v) > 1}
    print(f"  Studies in >1 review: {len(multi_review_studies)} ({len(multi_review_studies)/len(study_reviews)*100:.1f}%)")

    # Distribution of overlap
    overlap_counts = [len(v) for v in study_reviews.values()]
    max_overlap = max(overlap_counts) if overlap_counts else 0
    print(f"  Max reviews per study: {max_overlap}")

    # CCA
    cca = compute_cca(review_studies)
    print(f"  Corrected Covered Area (CCA): {cca:.4f}")
    if cca < 0.05:
        cca_class = 'Slight'
    elif cca < 0.10:
        cca_class = 'Moderate'
    elif cca < 0.15:
        cca_class = 'High'
    else:
        cca_class = 'Very High'
    print(f"  CCA classification: {cca_class} overlap")

    # Pairwise overlaps
    print("  Computing pairwise overlaps...")
    overlaps = compute_pairwise_overlap(review_studies)
    n_pairs_with_overlap = len(overlaps)
    total_pairs = len(review_studies) * (len(review_studies) - 1) // 2
    print(f"  Review pairs with shared studies: {n_pairs_with_overlap} / {total_pairs}")

    # Export
    # Top overlapping studies
    top_studies = sorted(multi_review_studies.items(), key=lambda x: -len(x[1]))[:100]
    studies_path = output_path / 'overlap_top_studies.csv'
    with open(studies_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['study', 'n_reviews', 'reviews'])
        for study, revs in top_studies:
            writer.writerow([study, len(revs), ';'.join(sorted(revs))])

    # Top overlapping review pairs
    pairs_path = output_path / 'overlap_pairs.csv'
    with open(pairs_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['review_1', 'review_2', 'n_shared', 'n_r1', 'n_r2', 'jaccard', 'pct_r1', 'pct_r2'])
        writer.writeheader()
        for row in overlaps[:500]:
            writer.writerow(row)

    # Summary
    summary = {
        'n_reviews': len(review_studies),
        'n_unique_studies': len(study_reviews),
        'n_multi_review': len(multi_review_studies),
        'pct_multi_review': round(len(multi_review_studies) / len(study_reviews) * 100, 1),
        'max_reviews_per_study': max_overlap,
        'cca': round(cca, 4),
        'cca_class': cca_class,
        'n_pairs_with_overlap': n_pairs_with_overlap,
        'total_possible_pairs': total_pairs,
        'overlap_distribution': {
            '1_review': sum(1 for c in overlap_counts if c == 1),
            '2_reviews': sum(1 for c in overlap_counts if c == 2),
            '3_reviews': sum(1 for c in overlap_counts if c == 3),
            '4plus': sum(1 for c in overlap_counts if c >= 4),
        },
        'top_5_overlapping_pairs': overlaps[:5],
    }
    with open(output_path / 'overlap_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    elapsed_total = time.time() - t0
    print()
    print("=" * 50)
    print("HEADLINE RESULTS")
    print("=" * 50)
    print(f"  {len(study_reviews):,} unique studies across {len(review_studies)} reviews")
    print(f"  {len(multi_review_studies):,} studies ({len(multi_review_studies)/len(study_reviews)*100:.1f}%) appear in multiple reviews")
    print(f"  CCA = {cca:.4f} ({cca_class} overlap)")
    print(f"  {n_pairs_with_overlap} review pairs share at least one study")
    if overlaps:
        top = overlaps[0]
        print(f"  Most overlapping pair: {top['review_1']}-{top['review_2']} ({top['n_shared']} shared studies)")
    print(f"  Total time: {elapsed_total:.1f}s")


if __name__ == '__main__':
    main()
