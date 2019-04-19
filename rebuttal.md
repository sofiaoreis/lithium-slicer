# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:


**Rebuttal:**

Thank you for the constructive review. 

This paper is not intended to propose a new approach, but, instead, to reassess the impact of an existing approach that combines dynamic slicing and Spectrum-based Fault Localization. Previous works show the effect of combining both techniques. However, results were inconclusive---they used rather small programs (because of limitations on their infrastructure), small number of faults, and evaluation metrics that can inflate diagnosis performance. The central contribution of our paper is to demonstrate that combining both techniques work for real and large programs.

We agree with the reviewer that the conclusions we can draw from our empirical study are limited to the used programs and therefore generalization is always questionable. We will improve our discussion in the Threats to Validity section regarding this issue.

Tables 3 and 4 show different views we thought were adequate to answer RQ2, but we realize that they should be further clarified. Dynamic slicing produces a set of components (e.g., statements). As such, it is not possible to rank results and select the top-k components. For that reason, Table 3 reports the results of Tandem-FL. Our decision to call it dynamic slicing alone was unfortunate and leads to confusion. Perhaps the best is to only include current table 4.

After double-checking the empirical results, we found that the decrease in value pointes on tables 3 and 4 for commons-lang is due to a typo. The percentage of faults for k=5 is also 96.9%. We double-checked all other values, and confirm that are correct. This will be clarified.

It is a fact that the implementation of our approach does not come without practical limitations. We can only ensure that the current implementation works with Defects4j programs only because we generalized our function of interest according to the type of failing messages that exist on the dataset. This generalization does not cover all cases. Although this can be customized, as it is, lithium-slicer may not produce valid results in other datasets. However, we intend to make clear what type of observed faults the tool is able to evaluate and turn the tool open-source after publishing the paper. Analysis and running time may be an issue, especially for programs where the codebases are rather large. Therefore, we also plan to take action on this point and add parallelization mechanisms to this type of techniques.

### Review 252039:

**Rebuttal:**

We kindly thank the reviewer for its insights and comments on our work.

We will ascertain that the paper's formality will be improved as well as the minor issues will be addressed. Exploring the statistical machine learning approach remains as future work, though.

### Review 263473:

**Rebuttal:**

We kindly thank the reviewer for the feedback provided on our work.

We agree that the "theorems" are rather claims/observations or properties of the ranking algorithm. Following the suggestion of one of reviewers, we will rename them as "claims".

Regarding the question whether claim 2 is also valid for other ranking algorithms, there is a possibility this might not be true. For now, we decided to only focus on the ranking algorithm that provided the best results in previous research - Ochiai. To answer the reviewer question accurately, the present work needs to be extended. We plan to investigate the veracity of claim 2 using other ranking algorithms, such as Tarantula, Op2, Barinel. This, however, remains for future work.

The focus of the paper is to show that dynamic slicing considerably improves SBFL (we found an improvement of 73.7%). We decided to start with a very simple approach (critical slicing) for its generality, simplicity, and scalability. We argue that if we are able to show that CS works, then the results could be further improved by using more accurate slicing techniques. It is also important to notice that the numbers of tools implementing slicing is rather limited.


## Review 263474:

**Rebuttal:**

We kindly thank the reviewer for the comments on our work.

As we mentioned in section 2, previous studies have demonstrated that Model-based software diagnosis (MBSD) can be framed as dynamic slicing. MBSD is a well-known approach that has been proposed by the diagnosis community, an AI sub-community. We agree that this paper will also be a good suit in software engineering, validation, and testing conferences but we also strongly argue that this paper is of interest of the IJCAI audience.
