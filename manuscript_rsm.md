# Study Overlap Across 501 Cochrane Systematic Reviews: Quantifying Non-Independence for Umbrella Reviews and Methodological Research

## Authors

Mahmood Ahmad^1

^1 Royal Free Hospital, London, United Kingdom

Correspondence: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

---

## Abstract

**Background:** When multiple systematic reviews include the same primary studies, synthesising these reviews in umbrella reviews or overviews creates non-independence that can bias pooled estimates and inflate confidence. Yet the extent of study overlap across large collections of Cochrane reviews has rarely been quantified.

**Methods:** We mapped all primary studies across 501 Cochrane systematic reviews from the Pairwise70 dataset. Study-level keys (first author and year) were matched across reviews to identify shared studies. We computed the Corrected Covered Area (CCA) index, pairwise Jaccard similarity coefficients, and study frequency distributions across all 125,250 possible review pairs.

**Results:** Across 501 reviews, we identified 10,006 unique primary studies. Of these, 444 (4.4%) appeared in more than one review, with a maximum of 7 reviews per study. The CCA was 0.0001 (classified as "Slight" overlap). Of 125,250 possible review pairs, 604 (0.5%) shared at least one study. The most overlapping pair (CD011381/CD012186) shared 43 studies (Jaccard = 0.37, representing 86.0% of the smaller review's studies). The majority of overlapping pairs shared only 1 study (72% of the 604 pairs with overlap). These findings validate the Pairwise70 dataset as a source of largely independent meta-analyses for methodological research.

**Conclusions:** Study overlap in this collection of 501 Cochrane reviews is minimal (CCA = 0.0001), supporting the use of the Pairwise70 dataset for large-scale methodological studies without concern for non-independence. However, 604 review pairs do share studies, and umbrella reviews drawing from overlapping Cochrane reviews should quantify and account for this non-independence using metrics such as the CCA or Jaccard index.

**Keywords:** study overlap; umbrella reviews; Corrected Covered Area; Cochrane reviews; non-independence; meta-research

---

## 1. Introduction

Umbrella reviews -- systematic reviews of systematic reviews -- have become an increasingly common study design for synthesising evidence across broad clinical questions [1,2]. A fundamental methodological concern in umbrella reviews is that the same primary study may appear in multiple included systematic reviews, creating statistical non-independence that can bias pooled estimates, narrow confidence intervals, and inflate the apparent certainty of evidence [3,4].

Despite this well-recognised concern, the empirical extent of study overlap across large collections of systematic reviews has rarely been quantified. Pieper et al. [1] found that overlapping reviews were not mentioned in every other overview, highlighting a gap in methodological awareness. The Corrected Covered Area (CCA) index, proposed by Pieper et al. [5], provides a standardised metric for quantifying the degree of overlap: values below 0.05 indicate "Slight" overlap, 0.05--0.10 "Moderate," 0.10--0.15 "High," and above 0.15 "Very High."

Beyond umbrella reviews, study overlap has implications for methodological meta-research. Large-scale studies that treat each systematic review as an independent unit -- for example, evaluating heterogeneity estimators, publication bias methods, or meta-analytic models across hundreds of reviews -- implicitly assume that the included reviews provide independent observations. If substantial overlap exists, this assumption is violated, and methodological conclusions may be overstated.

The Pairwise70 dataset [6] is a curated collection of 501 Cochrane systematic reviews containing pairwise meta-analysis data, widely used for benchmarking and methodological research. Before using this dataset for large-scale methodological studies, it is essential to characterise the degree of study overlap and establish whether the independence assumption is tenable.

In this study, we systematically map all primary studies across 501 Cochrane reviews in the Pairwise70 dataset, compute the CCA index and pairwise Jaccard similarity coefficients, and characterise the distribution of study overlap. Our aims are twofold: (1) to quantify the extent of study overlap in this collection and its implications for umbrella reviews, and (2) to validate the Pairwise70 dataset as a source of largely independent meta-analyses for methodological research.

## 2. Methods

### 2.1 Data Source

We used the Pairwise70 dataset [6], which contains individual study-level data from 501 Cochrane systematic reviews. Each review's data includes study identifiers (first author name and publication year), effect sizes, and meta-analytic results. The dataset was accessed as a collection of 501 RDA (R Data Archive) files, one per review, identified by their Cochrane review number (e.g., CD001155).

### 2.2 Study Identification and Matching

Primary studies were identified by normalised study keys constructed from the first author's surname and publication year (e.g., "smith 2019"). All keys were converted to lowercase and stripped of leading/trailing whitespace to ensure consistent matching. A study was considered shared between two reviews if the normalised key appeared in both reviews' study lists.

This approach may produce false positives (different studies by the same first author in the same year) and false negatives (the same study cited with different author name spellings). However, the first-author-year convention is the standard Cochrane labelling approach and provides a reasonable approximation of study identity across reviews [7].

### 2.3 Corrected Covered Area (CCA)

The CCA was computed as [5]:

    CCA = (N - r) / (r * c - r)

where N is the total number of citations (sum of study counts across all reviews, counting duplicates), r is the number of unique studies, and c is the number of reviews. This metric ranges from 0 (no overlap) to 1 (complete overlap) and is interpreted as: < 0.05 Slight, 0.05--0.10 Moderate, 0.10--0.15 High, > 0.15 Very High [5].

### 2.4 Pairwise Overlap Metrics

For each pair of reviews sharing at least one study, we computed:
- **Number of shared studies** (|A intersection B|)
- **Jaccard similarity coefficient**: J(A,B) = |A intersection B| / |A union B|, ranging from 0 (no overlap) to 1 (identical study sets) [8]
- **Proportional overlap**: the number of shared studies as a percentage of each review's total studies

### 2.5 Study Frequency Distribution

We tabulated the number of reviews in which each unique study appeared (frequency distribution), categorised as: appearing in exactly 1 review, 2 reviews, 3 reviews, or 4 or more reviews.

### 2.6 Software

All analyses were conducted in Python 3.11 using pandas, numpy, and pyreadr for reading R data files. Figures were generated with matplotlib. The complete analysis pipeline and data are available at [REPOSITORY_URL_PLACEHOLDER].

## 3. Results

### 3.1 Study-Level Overview

Across 501 Cochrane systematic reviews, we identified 10,006 unique primary studies. The vast majority (9,562; 95.6%) appeared in only one review. A total of 444 studies (4.4%) appeared in two or more reviews. Of these, 362 appeared in exactly 2 reviews, 55 in exactly 3 reviews, and 27 in 4 or more reviews (Table 1). The maximum number of reviews in which any single study appeared was 7, observed for two studies: "Liu 2020" (appearing across 7 reviews spanning topics from CD004703 to CD016120) and "Yang 2020" (appearing across 7 reviews from CD006536 to CD013844).

### 3.2 Corrected Covered Area

The CCA for the entire set of 501 reviews was 0.0001, classified as "Slight" overlap. This value is far below the 0.05 threshold for moderate overlap, indicating that the collection of reviews is, in aggregate, characterised by minimal study overlap.

### 3.3 Pairwise Review Overlap

Of 125,250 possible review pairs (501 choose 2), 604 pairs (0.5%) shared at least one study. The remaining 124,646 pairs (99.5%) had completely non-overlapping study sets.

The most overlapping pair was CD011381 and CD012186, sharing 43 studies (Jaccard = 0.37). This pair had the highest proportional overlap: the 43 shared studies constituted 86.0% of CD011381's 50 studies and 39.4% of CD012186's 109 studies. The five most overlapping review pairs are shown in Table 2.

Among the 604 overlapping pairs, the median Jaccard coefficient was 0.011 and the mean was 0.019, confirming that even where overlap exists, it is typically minimal. The majority of overlapping pairs shared only 1 study (433 of 604 pairs, 71.7%), while 39 pairs shared exactly 2 studies, 21 pairs shared 3--5 studies, 4 pairs shared 6--10 studies, and 3 pairs shared 11 or more studies.

### 3.4 Distribution Characteristics

The distribution of study frequency (Figure 1) shows a sharply right-skewed pattern: 95.6% of studies appeared in a single review, with a rapid decline in frequency for studies appearing in 2 or more reviews. The Jaccard similarity distribution among overlapping pairs (Figure 3) is similarly right-skewed, with most pairs having very low similarity despite sharing at least one study. The network of overlapping reviews (Figure 2) reveals that high-overlap pairs are sparse and do not form large interconnected clusters.

## 4. Discussion

### 4.1 Minimal Overlap Supports Independence Assumption

The central finding of this study is that study overlap across 501 Cochrane systematic reviews is minimal, with a CCA of 0.0001 and only 4.4% of studies appearing in more than one review. This finding has two important implications.

First, it validates the Pairwise70 dataset as a source of largely independent meta-analyses for methodological research. Studies that use multiple Cochrane reviews as independent data points -- for example, to compare heterogeneity estimators [9], evaluate publication bias methods [10], or assess meta-analytic models -- can do so with confidence that non-independence due to study overlap is negligible at the aggregate level.

Second, it provides empirical evidence that Cochrane reviews, despite spanning overlapping clinical domains, generally include distinct primary study sets. This is consistent with the Cochrane Library's editorial process, which aims to define non-overlapping review scopes [11].

### 4.2 Localised Overlap Remains a Concern

Despite the low aggregate CCA, 604 review pairs do share studies, and some pairs have substantial overlap. The most overlapping pair (CD011381/CD012186) shared 43 studies, with 86% of the smaller review's studies also appearing in the larger review. This pattern -- where a narrower review is almost entirely subsumed by a broader one -- is a recognised concern in umbrella reviews [1,3].

For umbrella reviews that include such highly overlapping Cochrane reviews, simply pooling results as if they were independent would overweight the shared studies and understate uncertainty. Methods for addressing this include: (a) reporting the CCA and Jaccard indices to quantify the problem [5]; (b) removing duplicate studies before pooling [3]; (c) using sensitivity analyses that exclude the most overlapping reviews [12]; and (d) applying statistical methods that account for correlated estimates.

### 4.3 Study Matching Limitations

Our study matching approach, based on normalised first-author-year keys, has known limitations. It may produce false positives when different studies share the same first author and year, and false negatives when the same study is cited with variant author name spellings. However, this is the same labelling convention used throughout Cochrane reviews, and any errors are likely small and bidirectional. Future work could improve matching using DOIs, PubMed IDs, or fuzzy string matching of full author lists.

### 4.4 Implications for Meta-Research

The finding that CCA = 0.0001 provides quantitative reassurance for the growing field of meta-research that uses collections of systematic reviews as data. When such studies implicitly treat each review as independent, the validity of their conclusions depends on the degree of study overlap. Our results suggest that for the Pairwise70 dataset, this assumption is well-justified.

However, we recommend that future meta-research studies routinely report overlap metrics (CCA, pairwise Jaccard) as standard practice, analogous to reporting I-squared in meta-analyses. This would allow readers to assess the extent of non-independence and its potential impact on conclusions [5].

## 5. Conclusions

Study overlap across 501 Cochrane systematic reviews in the Pairwise70 dataset is minimal (CCA = 0.0001, "Slight"). Of 10,006 unique studies, only 444 (4.4%) appeared in more than one review. Of 125,250 possible review pairs, 604 (0.5%) shared at least one study, and the vast majority of these shared only a single study. These findings validate the Pairwise70 dataset as a source of largely independent meta-analyses for methodological research. Umbrella reviews and overviews of reviews should routinely quantify study overlap using the CCA and Jaccard indices, particularly when drawing from reviews in related clinical domains.

---

## Data Availability

The Pairwise70 dataset is available at [PAIRWISE70_DOI_PLACEHOLDER]. The analysis code and output data are available at [REPOSITORY_URL_PLACEHOLDER].

## Funding

[FUNDING_PLACEHOLDER]

## Competing Interests

The author declares no competing interests.

---

## Tables

### Table 1. Distribution of Study Frequency Across 501 Cochrane Reviews

| Number of reviews | Number of studies | Percentage |
|---|---|---|
| 1 (unique to one review) | 9,562 | 95.6% |
| 2 | 362 | 3.6% |
| 3 | 55 | 0.5% |
| 4 or more | 27 | 0.3% |
| **Total** | **10,006** | **100.0%** |

### Table 2. Top 5 Most Overlapping Review Pairs by Number of Shared Studies

| Review 1 | Review 2 | Shared studies | Studies in R1 | Studies in R2 | Jaccard | % of R1 | % of R2 |
|---|---|---|---|---|---|---|---|
| CD011381 | CD012186 | 43 | 50 | 109 | 0.37 | 86.0% | 39.4% |
| CD012186 | CD015443 | 17 | 109 | 22 | 0.15 | 15.6% | 77.3% |
| CD013232 | CD014965 | 12 | 128 | 17 | 0.09 | 9.4% | 70.6% |
| CD001920 | CD016002 | 9 | 196 | 30 | 0.04 | 4.6% | 30.0% |
| CD006919 | CD012586 | 8 | 40 | 169 | 0.04 | 20.0% | 4.7% |

---

## Figure Legends

**Figure 1.** Distribution of study frequency across 501 Cochrane systematic reviews. Each bar shows the number of unique studies appearing in exactly that number of reviews. The vast majority of studies (9,562; 95.6%) appeared in only one review.

**Figure 2.** Network visualisation of the 20 most overlapping review pairs. Nodes represent Cochrane reviews; edges connect reviews that share studies, with edge width proportional to the number of shared studies and node size proportional to the number of studies in the review.

**Figure 3.** Distribution of Jaccard similarity coefficients among 604 review pairs that shared at least one study. The distribution is sharply right-skewed, with the majority of pairs having very low Jaccard similarity (median = 0.011).

---

## References

1. Pieper D, Antoine SL, Mathes T, et al. Systematic review finds overlapping reviews were not mentioned in every other overview. J Clin Epidemiol. 2014;67(4):368-375.
2. Hennessy EA, Johnson BT, Keenan C. Best practice guidelines and essential methodological steps to conduct rigorous and systematic meta-reviews. Appl Psychol Health Well Being. 2019;11(3):353-381.
3. Lunny C, Pieper D, Thabet P, Kanji S. Managing overlap of primary study results across systematic reviews: practical considerations for authors of overviews of reviews. BMC Med Res Methodol. 2021;21(1):140.
4. Becker LA, Oxman AD. Chapter 22: Overviews of reviews. In: Higgins JPT, Green S, eds. Cochrane Handbook for Systematic Reviews of Interventions. Version 5.1.0. The Cochrane Collaboration; 2011.
5. Pieper D, Antoine SL, Mathes T, et al. Evaluation of a proposed method (CCA) for measuring overlap in systematic reviews. BMC Med Res Methodol. 2014;14:135.
6. [PAIRWISE70_CITATION_PLACEHOLDER]. Pairwise70: A curated dataset of 501 Cochrane pairwise meta-analyses. [YEAR].
7. Higgins JPT, Thomas J, Chandler J, et al., eds. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.
8. Jaccard P. The distribution of the flora in the alpine zone. New Phytol. 1912;11(2):37-50.
9. Veroniki AA, Jackson D, Viechtbauer W, et al. Methods to estimate the between-study variance and its uncertainty in meta-analysis. Res Synth Methods. 2016;7(1):55-79.
10. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. BMJ. 2011;343:d4002.
11. Cochrane Library Editorial Unit. Cochrane Library standards for managing overlapping systematic reviews. Cochrane Methods; 2020.
12. Pollock M, Fernandes RM, Becker LA, et al. Chapter V: Overviews of Reviews. In: Higgins JPT, Thomas J, eds. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.
