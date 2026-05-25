# Study Overlap Across 501 Cochrane Reviews: Quantifying Non-Independence for Meta-Research

**Mahmood Ahmad**^1

1. Royal Free Hospital, London, United Kingdom

**Correspondence:** Mahmood Ahmad, mahmood.ahmad2@nhs.net
**ORCID:** 0009-0003-7781-4478

---

## Abstract

**Objective:** To quantify the degree of primary study overlap across Cochrane systematic reviews and assess whether non-independence threatens the validity of methodological meta-research using these reviews.

**Design:** Cross-sectional bibliometric analysis.

**Data source:** 501 Cochrane reviews from the Pairwise70 dataset, containing 10,006 unique primary studies.

**Main outcome measures:** Corrected Covered Area (CCA) index, pairwise Jaccard similarity coefficients, and study frequency distributions across all 125,250 review pairs.

**Results:** Overlap was minimal: CCA was 0.0001 (95% CI 0.00005-0.00018). Only 444 of 10,006 unique studies (4.4%) appeared in more than one review. Of 604 overlapping review pairs, the most overlapping pair shared 43 studies with a Jaccard coefficient of 0.37, while 72% of pairs shared only one study. The median number of reviews per overlapping study was 2 (IQR 2-2), indicating that study sharing was predominantly pairwise rather than network-like.

**Conclusions:** The Pairwise70 Cochrane review collection exhibits negligible study overlap, validating its use as a source of largely independent meta-analyses for large-scale methodological benchmarking. Researchers conducting meta-research across Cochrane reviews can treat individual reviews as independent units without substantive bias from shared primary studies.

**Keywords:** study overlap, meta-research, Cochrane reviews, corrected covered area, non-independence

---

## 1. Introduction

Large-scale meta-research — studying the methods, quality, and reporting of systematic reviews themselves — increasingly relies on collections of Cochrane reviews as a benchmark corpus.^1 Studies examining publication bias prevalence,^2 heterogeneity patterns,^3 and methodological quality^4 across hundreds of reviews implicitly assume that individual reviews represent independent units of analysis. If many reviews share the same primary studies, this non-independence could inflate precision estimates and produce misleading meta-research conclusions.

The extent of primary study overlap across large Cochrane review collections has not been systematically quantified. We addressed this gap by mapping all primary study appearances across 501 Cochrane reviews from the Pairwise70 dataset and computing standard overlap metrics.

---

## 2. Methods

### 2.1 Study Identification

Primary studies within each Cochrane review were identified using normalised first-author-year keys extracted from the Pairwise70 structured data. Keys were normalised by lowercasing, removing diacritics, and standardising name formats. Studies with identical keys across different reviews were flagged as shared.

### 2.2 Overlap Metrics

**Corrected Covered Area (CCA):**^5 The proportion of the study-by-review matrix that contains shared entries, corrected for the matrix size. CCA ranges from 0 (no overlap) to 1 (complete overlap).

**Pairwise Jaccard similarity:** For each pair of reviews (A, B), Jaccard = |A intersection B| / |A union B|. Computed for all 125,250 unique review pairs.

**Study frequency distribution:** The number of reviews in which each primary study appears.

---

## 3. Results

### 3.1 Overall Overlap

The Pairwise70 dataset contained 10,006 unique primary studies across 501 reviews. Only 444 studies (4.4%) appeared in more than one review. The CCA was 0.0001 (95% CI 0.00005-0.00018), indicating negligible overlap.

### 3.2 Pairwise Analysis

Of 125,250 possible review pairs, 604 (0.5%) had any study overlap. Among overlapping pairs:
- 72% shared only 1 study
- 18% shared 2-5 studies
- 10% shared 6 or more studies
- Maximum overlap: 43 shared studies (Jaccard = 0.37)

### 3.3 Study Frequency

Among the 444 overlapping studies:
- Median reviews per study: 2 (IQR 2-2)
- Maximum: 7 reviews
- 89% appeared in exactly 2 reviews

---

## 4. Discussion

The negligible overlap (CCA = 0.0001) validates the Pairwise70 collection as a source of largely independent meta-analyses. The 4.4% shared-study rate is concentrated in closely related topic areas (e.g., multiple reviews on similar interventions in the same clinical domain) rather than reflecting systematic non-independence.

The main limitation is that first-author-year matching may produce false positives when different studies share identical author surnames and publication years. This would overestimate overlap, making our finding of minimal overlap conservative.

---

## References

1. Page MJ, Shamseer L, Altman DG, et al. Epidemiology and reporting characteristics of systematic reviews. *PLoS Med*. 2016;13(5):e1002028. doi:10.1371/journal.pmed.1002028
2. Ioannidis JPA. Why most published research findings are false. *PLoS Med*. 2005;2(8):e124.
3. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. *Stat Med*. 2002;21(11):1539-1558.
4. Shea BJ, Reeves BC, Wells G, et al. AMSTAR 2. *BMJ*. 2017;358:j4008. doi:10.1136/bmj.j4008
5. Pieper D, Antoine SL, Mathes T, et al. Systematic review finds overlapping reviews were not mentioned in every other overview. *J Clin Epidemiol*. 2014;67(4):368-375. doi:10.1016/j.jclinepi.2013.11.007

---

## Data Availability

Code at https://github.com/mahmood726-cyber/overlap-detector (MIT licence).
