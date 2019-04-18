# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:

** issue 1:**
> The approach itself, i.e., combining the mentioned debugging approaches is not that novel (as also indicated in the paper) and there are other papers describing such improvements. This is definitely a weakness of this paper. However, there is an empirical evaluation that is novel capturing important research questions. 

**issue 2:** Not in the paper. Should be mentioned in the paper (Threats to Validity).
> Of course – and like other similar paper – the study is limited to some programs and generalization is always questionable. 

**issue 3:** 
I think the reviewer is confused because we present the results of DS two times in different tables.
> From Table 3 and Table 4 we see that basically slicing alone leads to improvements, because the values for Tandem-FL and slicing are the same. 

**issue 4:** 
Explain why it can be worse.
> I am also wondering why there is a small value for commons-lang in case of k=10 when compared with k=5? I would assume that taking care of more statements should improve debugging performance.

**issue 5:** 
> In addition, there is no discussion of drawbacks behind the approach. Spectrum-based fault localization is successful because it does not require a lot of tools and can be more or less easily adapted for other programming languages. This is not the case for slicing. For slicing we require to know not only that a test case is failing but also to identify all output variables that deliver wrong values. In case of exceptions (as discussed a little bit in the paper) we may also use different slicing approaches to improve the results. There is some work on dynamic slicing in case of exceptions. Moreover, slicing needs more time for analysis and running time might become an issue.

**Rebuttal:**

We kindly thank the reviewer for the comments and questions raised on our work.

In fact, we did not address the limitation regarding programs and generalization. We will add this discussion to Threats to Validity.


The results k=10 suffer a decrease because the slicer is evaluating 10 full classes instead of only 5. For each k, we evaluate if at least one of the buggy-lines of the k classes is on the slicer report. When the 10 classes (k=10) are evaluated, there might be some of the buggy-lines that were not taken into account for k=5 that are being evaluated now and are not found in the report. 

< not sure yet how to answer issue 5>

Regarding the point about slicing running time needs, we indirectly touch on that in Threats to Validity when it is mentioned that the faults from the Closure compiler project were not evaluated because of the high CPU cost of the technique. Yet, we will clarify it.

### Review 252039:

**Rebuttal:**

We kindly thank the reviewer for its insights and comments on our work. 

We will make sure that the paper's formality will be improved and that minor issues will also be addressed. We will definitely explore the statistical machine learning approach in future work.

### Review 263473:

**Issues:** 
> * An obvious improvement would be to parameterize the approach to  allow plugging in multiple different ranking algorithms. That  immediately raises the question: does the observation that the rank of faulty statements cannot decrease if the slice includes the  faulty statements also work with other ranking algorithms than  Ochiai? It feels that calling the observation a theorem is a bit  ambitious. Perhaps such property is something to characterize the ranking algorithms by?
> * A more labour intensive approach would be to also parameterize  the approach over different slicing implementations, or at least  foresee the need and make it very clear how to change the slicing algorithm. It is very nice that the authors have started with critical slicing as one of the earlier appropriate approaches.
> * Theorem 1 is not a theorem, it is rather an observation, because it  depends on the simplifications used by the slicing  algorithm.
> * Theorem 2 is actually a property of the Ochiai ranking formula, not a theorem.

**Rebuttal:**

We thank the reviewer for the feedback provided on our work. 

Regarding the question about if claim 2 is also true for other ranking algorithms, there is a possibility this might not be true. To answer your question, the present work needs to be extended. We plan to investigate the veracity of claim 2 using other ranking algorithms, such as, Tarantula, Op2, Barinel and etc. This, however remains for future work.

< Still have to justify why have we not compared with other slicing approaches >

< Not sure what to say about the name, do we agree?>

We agree that our theorems are rather observations or properties of the ranking algorithm. Thus, these misconceptions will be addressed on the paper.

## Review 263474:

**Rebuttal:**

We kindly thank the reviewer for the comments on our work. 

As we mention in section 2, applications of model-based diagnosis to localize software faults have demonstrated that can be framed as dynamic slicing by Wolfgang Mayer and Markus Stumptner in previous research which is the technique we propose to improve software fault localization. Model-based diagnosis is a well-known approach that has been proposed by the diagnosis community. This community develops algorithms and techniques that leverage AI to determine the rootcause of observed faults. We agree that this paper will be a good suit in software engineering, validation and testing conferences but we also strongly believe that this paper can be published at IJCAI since we are applying AI to improve SBFL.
