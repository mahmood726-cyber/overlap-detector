Mahmood Ahmad
Tahir Heart Institute
author@example.com

Study Overlap Across 501 Cochrane Reviews: Quantifying Non-Independence for Meta-Research

How much primary study overlap exists across large collections of Cochrane systematic reviews, and does this non-independence threaten the validity of methodological meta-research? We mapped all primary studies across 501 Cochrane reviews from the Pairwise70 dataset using normalized first-author-year keys to identify shared studies across reviews. The pipeline computed the Corrected Covered Area index, pairwise Jaccard similarity coefficients, and study frequency distributions across all 125,250 review pairs. The prevalence of overlap was minimal: CCA was 0.0001 (95% CI 0.00005-0.00018), with only 444 of 10,006 unique studies (4.4%) appearing in more than one review. Of 604 overlapping pairs, the most overlapping pair shared 43 studies with a Jaccard coefficient of 0.37, while 72% of pairs shared only one study. These results validate the Pairwise70 dataset as a source of largely independent meta-analyses suitable for large-scale methodological benchmarking. A limitation is that first-author-year matching may produce false positives when different studies share identical author surnames and publication years.

Outside Notes

Type: meta-research
Primary estimand: Corrected Covered Area (CCA)
App: Overlap Detector v1.0
Data: 501 Cochrane reviews from Pairwise70 dataset (10,006 unique studies)
Code: https://github.com/mahmood726-cyber/overlap-detector
Version: 1.0
Validation: Author reviewed draft

References

1. Barendregt JJ, Doi SA, Lee YY, Norman RE, Vos T. Meta-analysis of prevalence. J Epidemiol Community Health. 2013;67(11):974-978.
2. Nyaga VN, Arbyn M, Aerts M. Metaprop: a Stata command to perform meta-analysis of binomial data. Arch Public Health. 2014;72:39.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
