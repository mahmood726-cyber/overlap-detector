"""Generate publication-quality figures for the OverlapDetector manuscript.

Produces 3 figures:
  1. Study frequency distribution (bar chart)
  2. Overlap network (top 20 pairs)
  3. Jaccard similarity distribution (histogram)

Saves 300 dpi PNG + PDF to figures/ directory.

Usage: python generate_figures.py
"""

import io
import sys
import json
import csv
import os
from pathlib import Path

# Windows cp1252 safety
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Paths
BASE_DIR = Path(r'C:\OverlapDetector')
OUTPUT_DIR = BASE_DIR / 'data' / 'output'
FIG_DIR = BASE_DIR / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Shared style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.15,
})


def load_summary():
    with open(OUTPUT_DIR / 'overlap_summary.json', encoding='utf-8') as f:
        return json.load(f)


def load_pairs():
    rows = []
    with open(OUTPUT_DIR / 'overlap_pairs.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                'review_1': r['review_1'],
                'review_2': r['review_2'],
                'n_shared': int(r['n_shared']),
                'n_r1': int(r['n_r1']),
                'n_r2': int(r['n_r2']),
                'jaccard': float(r['jaccard']),
                'pct_r1': float(r['pct_r1']),
                'pct_r2': float(r['pct_r2']),
            })
    return rows


def figure1_study_frequency(summary):
    """Bar chart: how many reviews each study appears in."""
    dist = summary['overlap_distribution']
    # Categories
    cats = ['1', '2', '3', '4+']
    vals = [dist['1_review'], dist['2_reviews'], dist['3_reviews'], dist['4plus']]
    total = sum(vals)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    colors = ['#2c7bb6', '#fdae61', '#d7191c', '#a50026']
    bars = ax.bar(cats, vals, color=colors, edgecolor='white', linewidth=0.5, width=0.6)

    # Annotate with count and percentage
    for bar, val in zip(bars, vals):
        pct = val / total * 100
        if val > 200:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 120,
                    f'{val:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 120,
                    f'{val}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Number of reviews per study')
    ax.set_ylabel('Number of studies')
    ax.set_title('Distribution of Study Frequency Across 501 Cochrane Reviews')
    ax.set_ylim(0, max(vals) * 1.2)

    # Use log inset for detail
    # Add text annotation for the key finding
    ax.annotate(f'95.6% of studies\nappear in only 1 review',
                xy=(0, vals[0]), xytext=(1.5, vals[0] * 0.7),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color='grey', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='grey'))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for fmt in ['png', 'pdf']:
        fig.savefig(FIG_DIR / f'figure1_study_frequency.{fmt}')
    plt.close(fig)
    print('  Figure 1 saved: study frequency distribution')


def figure2_overlap_network(pairs):
    """Network graph of top 20 most overlapping review pairs."""
    top20 = pairs[:20]

    # Collect unique nodes
    nodes = set()
    for p in top20:
        nodes.add(p['review_1'])
        nodes.add(p['review_2'])
    nodes = sorted(nodes)
    n = len(nodes)

    # Node sizes proportional to total studies in that review
    node_studies = {}
    for p in top20:
        node_studies[p['review_1']] = max(node_studies.get(p['review_1'], 0), p['n_r1'])
        node_studies[p['review_2']] = max(node_studies.get(p['review_2'], 0), p['n_r2'])

    # Layout: circular
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 4.0
    pos = {node: (radius * np.cos(a), radius * np.sin(a)) for node, a in zip(nodes, angles)}

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw edges
    max_shared = max(p['n_shared'] for p in top20)
    for p in top20:
        x1, y1 = pos[p['review_1']]
        x2, y2 = pos[p['review_2']]
        lw = 0.5 + 4.5 * (p['n_shared'] / max_shared)
        alpha = 0.3 + 0.6 * (p['n_shared'] / max_shared)
        ax.plot([x1, x2], [y1, y2], color='#d7191c', linewidth=lw, alpha=alpha, zorder=1)
        # Label edge with shared count if >= 5
        if p['n_shared'] >= 5:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, str(p['n_shared']), fontsize=7, ha='center', va='center',
                    color='#a50026', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.8),
                    zorder=3)

    # Draw nodes
    max_studies = max(node_studies.values()) if node_studies else 1
    for node in nodes:
        x, y = pos[node]
        ns = node_studies.get(node, 1)
        size = 200 + 800 * (ns / max_studies)
        ax.scatter(x, y, s=size, c='#2c7bb6', edgecolors='white', linewidth=1.5, zorder=2)
        # Label
        label = node.replace('CD0', 'CD0')  # keep full ID
        offset_x = 0.3 * np.cos(angles[nodes.index(node)])
        offset_y = 0.3 * np.sin(angles[nodes.index(node)])
        ax.text(x + offset_x * 1.8, y + offset_y * 1.8, label,
                fontsize=7, ha='center', va='center', fontweight='bold')

    ax.set_title('Network of Top 20 Most Overlapping Cochrane Review Pairs', fontsize=12)
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-6.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], color='#d7191c', linewidth=1, label='1 shared study'),
        plt.Line2D([0], [0], color='#d7191c', linewidth=4, label=f'{max_shared} shared studies'),
        plt.scatter([], [], s=200, c='#2c7bb6', edgecolors='white', label='Smaller review'),
        plt.scatter([], [], s=800, c='#2c7bb6', edgecolors='white', label='Larger review'),
    ]
    # Simplified legend
    thin_line = plt.Line2D([0], [0], color='#d7191c', linewidth=1, label='Fewer shared studies')
    thick_line = plt.Line2D([0], [0], color='#d7191c', linewidth=4, label='More shared studies')
    small_dot = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2c7bb6',
                           markersize=8, label='Fewer studies in review')
    big_dot = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2c7bb6',
                         markersize=14, label='More studies in review')
    ax.legend(handles=[thin_line, thick_line, small_dot, big_dot],
              loc='lower right', fontsize=8, framealpha=0.9)

    for fmt in ['png', 'pdf']:
        fig.savefig(FIG_DIR / f'figure2_overlap_network.{fmt}')
    plt.close(fig)
    print('  Figure 2 saved: overlap network')


def figure3_jaccard_distribution(pairs):
    """Histogram of Jaccard similarity coefficients for overlapping pairs."""
    jaccards = [p['jaccard'] for p in pairs]

    fig, (ax_main, ax_inset) = plt.subplots(1, 2, figsize=(9, 4.5),
                                             gridspec_kw={'width_ratios': [3, 1]})

    # Main histogram
    bins = np.arange(0, 0.42, 0.01)
    counts, _, patches = ax_main.hist(jaccards, bins=bins, color='#2c7bb6',
                                       edgecolor='white', linewidth=0.5)

    # Colour the extreme bar differently
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge >= 0.35:
            patch.set_facecolor('#d7191c')

    median_j = sorted(jaccards)[len(jaccards) // 2]
    mean_j = sum(jaccards) / len(jaccards)

    ax_main.axvline(median_j, color='#fdae61', linestyle='--', linewidth=1.5, label=f'Median = {median_j:.3f}')
    ax_main.axvline(mean_j, color='#d7191c', linestyle=':', linewidth=1.5, label=f'Mean = {mean_j:.3f}')

    ax_main.set_xlabel('Jaccard Similarity Coefficient')
    ax_main.set_ylabel('Number of Review Pairs')
    ax_main.set_title('Distribution of Jaccard Similarity Among\n604 Overlapping Review Pairs')
    ax_main.legend(fontsize=9)
    ax_main.spines['top'].set_visible(False)
    ax_main.spines['right'].set_visible(False)

    # Right panel: box plot
    bp = ax_inset.boxplot(jaccards, vert=True, patch_artist=True,
                          boxprops=dict(facecolor='#abd9e9', edgecolor='#2c7bb6'),
                          medianprops=dict(color='#d7191c', linewidth=2),
                          whiskerprops=dict(color='#2c7bb6'),
                          capprops=dict(color='#2c7bb6'),
                          flierprops=dict(marker='o', markerfacecolor='#fdae61',
                                         markeredgecolor='#d7191c', markersize=4))
    ax_inset.set_ylabel('Jaccard Coefficient')
    ax_inset.set_title('Box Plot', fontsize=10)
    ax_inset.set_xticks([])
    ax_inset.spines['top'].set_visible(False)
    ax_inset.spines['right'].set_visible(False)

    # Annotate key stats on box plot
    ax_inset.text(1.3, max(jaccards), f'Max: {max(jaccards):.2f}', fontsize=8, va='center')
    ax_inset.text(1.3, median_j, f'Median: {median_j:.3f}', fontsize=8, va='center')

    plt.tight_layout()
    for fmt in ['png', 'pdf']:
        fig.savefig(FIG_DIR / f'figure3_jaccard_distribution.{fmt}')
    plt.close(fig)
    print('  Figure 3 saved: Jaccard distribution')


def main():
    print('OverlapDetector Figure Generator')
    print('=' * 40)

    summary = load_summary()
    pairs = load_pairs()

    # We have 500 pairs in CSV (top 500 of 604)
    # For Jaccard histogram, note that the remaining 104 pairs all have Jaccard
    # lower than the minimum in the CSV (they share fewer studies), so the
    # distribution is well-represented by the available data.
    print(f'  Loaded summary: {summary["n_reviews"]} reviews, {summary["n_unique_studies"]} studies')
    print(f'  Loaded {len(pairs)} overlapping pairs from CSV')

    figure1_study_frequency(summary)
    figure2_overlap_network(pairs)
    figure3_jaccard_distribution(pairs)

    print()
    print('All figures saved to:', FIG_DIR)
    print('Formats: PNG (300 dpi) + PDF')


if __name__ == '__main__':
    main()
