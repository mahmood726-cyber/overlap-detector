"""Tests for Overlap Detector pipeline."""
import sys, json, pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import compute_cca, compute_pairwise_overlap, main, resolve_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / 'data' / 'output'


class TestCCA:
    def test_no_overlap(self):
        """Completely disjoint reviews → CCA = 0."""
        reviews = {'R1': {'a', 'b', 'c'}, 'R2': {'d', 'e', 'f'}}
        assert compute_cca(reviews) == 0.0

    def test_complete_overlap(self):
        """Identical review sets → CCA > 0."""
        reviews = {'R1': {'a', 'b', 'c'}, 'R2': {'a', 'b', 'c'}}
        cca = compute_cca(reviews)
        assert cca > 0
        # CCA = (6-3)/(3*2-3) = 3/3 = 1.0
        assert abs(cca - 1.0) < 1e-10

    def test_partial_overlap(self):
        """Some shared studies → 0 < CCA < 1."""
        reviews = {'R1': {'a', 'b', 'c'}, 'R2': {'b', 'c', 'd'}}
        cca = compute_cca(reviews)
        assert 0 < cca < 1
        # N=6, r=4, c=2 → CCA = (6-4)/(4*2-4) = 2/4 = 0.5
        assert abs(cca - 0.5) < 1e-10

    def test_single_review(self):
        """Single review → denom is 0 → CCA = 0."""
        reviews = {'R1': {'a', 'b', 'c'}}
        assert compute_cca(reviews) == 0.0

    def test_many_reviews_slight(self):
        """Many reviews with tiny overlap → CCA < 0.05."""
        reviews = {f'R{i}': {f's{i}_{j}' for j in range(10)} for i in range(20)}
        # Add one shared study to 2 reviews
        reviews['R0'].add('shared')
        reviews['R1'].add('shared')
        cca = compute_cca(reviews)
        assert cca < 0.05

    def test_cca_formula_manual(self):
        """Manual CCA computation check."""
        reviews = {
            'R1': {'a', 'b', 'c', 'd'},
            'R2': {'c', 'd', 'e'},
            'R3': {'a', 'f', 'g'},
        }
        # N = 4+3+3 = 10, r = 7, c = 3
        # CCA = (10-7)/(7*3-7) = 3/14 ≈ 0.2143
        cca = compute_cca(reviews)
        assert abs(cca - 3/14) < 1e-10


class TestPairwiseOverlap:
    def test_no_overlap_returns_empty(self):
        reviews = {'R1': {'a', 'b'}, 'R2': {'c', 'd'}}
        result = compute_pairwise_overlap(reviews)
        assert len(result) == 0

    def test_one_shared_study(self):
        reviews = {'R1': {'a', 'b', 'c'}, 'R2': {'c', 'd', 'e'}}
        result = compute_pairwise_overlap(reviews)
        assert len(result) == 1
        assert result[0]['n_shared'] == 1
        # Jaccard: 1/5 = 0.2
        assert abs(result[0]['jaccard'] - 0.2) < 0.01

    def test_multiple_pairs(self):
        reviews = {
            'R1': {'a', 'b', 'c'},
            'R2': {'b', 'c', 'd'},
            'R3': {'d', 'e', 'f'},
        }
        result = compute_pairwise_overlap(reviews)
        # R1-R2 share {b,c}, R2-R3 share {d}, R1-R3 share nothing
        assert len(result) == 2
        # Sorted by n_shared desc
        assert result[0]['n_shared'] == 2  # R1-R2
        assert result[1]['n_shared'] == 1  # R2-R3

    def test_jaccard_perfect_overlap(self):
        reviews = {'R1': {'a', 'b'}, 'R2': {'a', 'b'}}
        result = compute_pairwise_overlap(reviews)
        assert len(result) == 1
        assert abs(result[0]['jaccard'] - 1.0) < 1e-10

    def test_proportional_overlap(self):
        reviews = {'R1': {'a', 'b', 'c', 'd'}, 'R2': {'a', 'b'}}
        result = compute_pairwise_overlap(reviews)
        assert result[0]['pct_r1'] == 50.0  # 2/4
        assert result[0]['pct_r2'] == 100.0  # 2/2


class TestResultsIntegrity:
    """Verify actual pipeline results match expected values."""

    @pytest.fixture
    def summary(self):
        path = OUTPUT_DIR / 'overlap_summary.json'
        if not path.exists():
            pytest.skip('Pipeline results not found')
        with open(path) as f:
            return json.load(f)

    def test_review_count(self, summary):
        assert summary['n_reviews'] >= 500

    def test_unique_studies(self, summary):
        assert summary['n_unique_studies'] > summary['n_reviews']

    def test_multi_review_count(self, summary):
        assert 0 < summary['n_multi_review'] < summary['n_unique_studies']
        expected_pct = round(summary['n_multi_review'] / summary['n_unique_studies'] * 100, 1)
        assert abs(summary['pct_multi_review'] - expected_pct) < 0.1

    def test_cca_slight(self, summary):
        assert summary['cca'] < 0.05
        assert summary['cca_class'] == 'Slight'

    def test_overlap_pairs(self, summary):
        assert summary['n_pairs_with_overlap'] > 0
        assert summary['n_pairs_with_overlap'] <= summary['total_possible_pairs']

    def test_distribution_sums(self, summary):
        d = summary['overlap_distribution'].copy()
        total = d['1_review'] + d['2_reviews'] + d['3_reviews'] + d['4plus'].copy()
        assert total == summary['n_unique_studies']

    def test_top_pair(self, summary):
        top = summary['top_5_overlapping_pairs'][0].copy()
        assert top['n_shared'] >= 1
        assert top['review_1'].startswith('CD')
        assert top['review_2'].startswith('CD')


def test_main_uses_repo_relative_sibling_projects(tmp_path, monkeypatch):
    projects_root = tmp_path / 'projects'
    project_root = projects_root / 'OverlapDetector'
    project_root.mkdir(parents=True)

    paths = resolve_paths(project_root=project_root, projects_root=projects_root)
    paths['pairwise_dir'].mkdir(parents=True, exist_ok=True)

    synthetic_study_reviews = {
        'alpha 2001': {'CD000001', 'CD000002'},
        'beta 2002': {'CD000001'},
        'gamma 2003': {'CD000002'},
    }
    synthetic_review_studies = {
        'CD000001': {'alpha 2001', 'beta 2002'},
        'CD000002': {'alpha 2001', 'gamma 2003'},
    }
    synthetic_review_names = {
        'CD000001': 'Review one',
        'CD000002': 'Review two',
    }
    monkeypatch.setattr(
        'pipeline.load_all_studies',
        lambda _: (synthetic_study_reviews, synthetic_review_studies, synthetic_review_names),
    )

    output_dir = main(project_root=project_root, projects_root=projects_root)

    summary = json.loads((output_dir / 'overlap_summary.json').read_text(encoding='utf-8'))
    assert output_dir == project_root / 'data' / 'output'
    assert summary['n_reviews'] == 2
    assert summary['n_unique_studies'] == 3
    assert summary['n_pairs_with_overlap'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
