# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:


**Rebuttal:**

We kindly thank the reviewer for the comments and questions raised on our work.

This paper is not intended to propose a new approach, but, instead, to demystify the combination of dynamic slicing and SFL. There are previous works which show the value of combining both techniques. However, the applicability of the techniques proposed by related work are questionable because they used rather small programs and seeded faults. The contribution of our paper is to demonstrate that combining both techniques work for real and large programs.

We agree with the reviewer that our empirical study is limited to some programs and therefore the generalization is always questionable. We will improve our discussion in the Threats to Validity section regarding this issue.

Table 3 and 4 are present different views to answer RQ2. [missing 2nd part of DS vs Tandem-FL and DS being a set]

We double-checked the empirical results and the decrease observed in table 3 and 4 for commons-lang is a typo. The percentage of faults for k=5 is also 96.9%. We have double-checked all other values, they stand correct. This will be fixed.

These techniques have a few practical limitations. We can only ensure that the proposed technique will work with Defects4j programs because we generalized our function of interest according to the type of failing tests messages that exist on the dataset. Thus, some messages with very specific characteristics may not provide valid results. However, we intend to make clear what type of observed faults the tool is able to evaluate and turn the tool open-source after publishing it. Analysis and running time it is an issue, especially, in programs where the codebases are larger such as the Closure Compiler. Therefore, we also plan to take action on this point and add parallelization mechanisms to this type of techniques.

### Review 252039:

**Rebuttal:**

We kindly thank the reviewer for its insights and comments on our work.

We will ascertain that the paper's formality will be improved as well as the minor issues will be addressed. Exploring the statistical machine learning approach remains as future work.

### Review 263473:

**Rebuttal:**

We kindly thank the reviewer for the feedback provided on our work.

We agree that the "theorems" are rather claims/observations or properties of the ranking algorithm. Following the suggestion of one of reviewers, we will rename them as "claims".

Regarding the question whether claim 2 is also valid for other ranking algorithms, there is a possibility this might not be true. For now, we decided to only focus on the ranking algorithm that provided the best results in previous research - Ochiai. To answer the reviewer question accurately, the present work needs to be extended. We plan to investigate the veracity of claim 2 using other ranking algorithms, such as Tarantula, Op2, Barinel. This, however, remains for future work.

The focus of the paper is to show that dynamic slicing considerably improves SBFL (we found an improvement of 73.7%). We decided to start with a very simple approach (critical slicing) due to its generalization, simplicity, and scalability. We argue that if we are able to show that CS works, then the results could be further improved by using more accurate slicing techniques. It is also important to notice that the numbers of tools implementing slicing is rather limited.


## Review 263474:

**Rebuttal:**

We kindly thank the reviewer for the comments on our work.

As we mentioned in section 2, a previous studies have demonstrated that Model-based software diagnosis can be framed as dynamic slicing. This is a well-known approach that has been proposed by the diagnosis community, an AI sub-community. We agree that this paper will also be a good suit in software engineering, validation, and testing conferences but we also strongly argue that this paper is of interest of the IJCAI audience, since we are applying an AI-based technique to improve SBFL.
