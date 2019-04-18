# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:

**issue 4:** 
Explain why it can be worse.
> I am also wondering why there is a small value for commons-lang in case of k=10 when compared with k=5? I would assume that taking care of more statements should improve debugging performance.

**Rebuttal:**

We kindly thank the reviewer for the comments and questions raised on our work.

As the title states, we intend to demystify the combination of Dynamic Slicing with Spectrum-based Fault Localization. Previous research have already shown impact and importance of both techniques - combined and separated. However, from the studies available about combining these two techniques, it was not yet clear if DS could help SBFL on obtaining more accurate results and how great would that improvement be. Thus, we find that our research questions and results might be important to guide researchers on performing research based on the combination of both techniques.

We have not address the limitation regarding programs and generalization. Thus, we will fix and add this discussion to Threats to Validity.

In table 3, we present the results for dynamic slicing alone whereas in table 4 we present the results of SFL vs. Tandem-FL for each k. Dynamic slicing in table 3 is the same as Tandem-FL in table 4. Thus, the values are the same. We only presented the same results in different views. On table 3, we intend to show the evolution of Tandem-FL/dynamic slicing between different k's (k=5 and k=10) and focus solely on the dynamic slicing performance on finding faulty statements for different k's. Whereas, in table 4, our goal is to show the difference between SFL and Tandem-FL for each k. We understand that this might create some confusion. Thus, we will try to improve it.

_The results k=10 suffer a decrease because the slicer is evaluating 10 full classes instead of only 5. For each k, we evaluate if at least one of the buggy-lines of the k classes is on the slicer report. When the 10 classes (k=10) of fault are evaluated, there might be some of the buggy-lines that were not taken into account for k=5 that are being evaluated now and are not found in the report._ (!! not finished yet)

These techniques have a few pratical limitations. We can only ensure that the proposed technique will work with defects4j programs because we generalized our function of interess according with the type of failling tests messages that exist on the dataset. Thus, some messages with very specific characteristics may not provide valide results. However, we intend to make clear what type of observed faults the tools is able to evaluate and turn the tool open-source after publishing it. Analysis and running time it is an issue, specially, in programs where the codebases are larger such as the Closure Compiler. Therefore, we also plan to take action on this point and add parallelization mechanisms to this type of techniques.

### Review 252039:

**Rebuttal:**

We kindly thank the reviewer for its insights and comments on our work. 

We will make sure that the paper's formality will be improved and that the minor issues will be addressed. We will definitely explore the statistical machine learning approach in future work. Thank you for the hint!

### Review 263473:

**Rebuttal:**

We kindly thank the reviewer for the feedback provided on our work. 

We agree that our "theorems" are rather claims/observations or properties of the ranking algorithm. Thus, these misconceptions will be addressed on the paper. 

Regarding the question about if claim 2 is also true for other ranking algorithms, there is a possibility this might not be true. For now we decided to only focus on the ranking algorithm that provided the best results in previous research - ochiai. To answer the reviewer question precisely, the present work needs to be extended. We plan to investigate the veracity of claim 2 using other ranking algorithms, such as, Tarantula, Op2, Barinel and etc. This, however remains for future work.

Our focus in the paper was to show that dynamic slicing may considerable improve SBFL (we found an improvement of 73.7%). We decided to start with a very simple approach (critical slicing) due to its generalization, simplicity and scalability. Our idea was that if we were able to show that CS works, then later we could leverage more accurate slicing techniques to improve our results. It is also important to notice that the numbers of tools implementing this type of techniques is very small. However, we will explore this in more detail in the future.


## Review 263474:

**Rebuttal:**

We kindly thank the reviewer for the comments on our work. 

As we mention in section 2, applications of model-based diagnosis (MBDS) to localize software faults by Wolfgang Mayer and Markus Stumptner in previous research have demonstrated that MBDS can be framed as dynamic slicing which is the technique we propose to improve software fault localization. MBDS is a well-known approach that has been proposed by the diagnosis community. This community develops algorithms and techniques that leverage AI to determine the rootcause of observed faults. We agree that this paper will be a good suit in software engineering, validation and testing conferences but we also strongly believe that this paper can be published at IJCAI since we are applying AI to improve SBFL.
