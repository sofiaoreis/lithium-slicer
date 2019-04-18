# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:

**issue 1:** Not sure if this point needs comments.
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
> In addition, there is no discussion of drawbacks behind the approach. Spectrum-based fault localization is successful because it does not require a lot of tools and can be more or less easily adapted for other programming languages. This is not the case for slicing. For slicing we require to know not only that a test case is failing but also to identify all output variables that deliver wrong values. In case of exceptions (as discussed a little bit in the paper) we may also use different slicing approaches to improve the results. There is some work on dynamic slicing in case of exceptions. 

**issue 6:** This issue is addressed in threats to validity...
> Moreover, slicing needs more time for analysis and running time might become an issue.

**Rebuttal:**

### Review 252039:

**Rebuttal:**

We kindly thank the reviewer for its insights and comments on our work. 

We will make sure that the paper's formality will be improved and that minor issues will also be addressed. We will definitely explore the statistical machine learning approach in future work.

### Review 263473:

**Issues:** 
> * An obvious improvement would be to parameterize the approach to  allow plugging in multiple different ranking algorithms. That  immediately raises the question: does the observation that the rank of faulty statements cannot decrease if the slice includes the  faulty statements also work with other ranking algorithms than  Ochiai? It feels that calling the observation a theorem is a bit  ambitious. Perhaps such property is something to characterize the ranking algorithms by?
> * A more labour intensive approach would be to also parameterize  the approach over different slicing implementations, or at least  foresee the need and make it very clear how to change the slicing algorithm. It is very nice that the authors have started with critical slicing as one of the earlier appropriate approaches.
> * Perhaps the approach should be called DS-SBFL instead of Tandem-FL?  The reason being that there are multiple things that could be used  in tandem in the fault localisation context (for example a tandem of  some symbolic FL approach with an additional technique).
> * Theorem 1 is not a theorem, it is rather an observation, because it  depends on the simplifications used by the slicing  algorithm.
> * Theorem 2 is actually a property of the Ochiai ranking formula, not a theorem.

**Rebuttal:**

We thank the reviewer for the feedback provided on our work. 

Regarding the question about if claim 2 is also true for other ranking algorithms, there is a possibility this might not be true. To answer your question, the present work needs to be extended. We plan to investigate the veracity of claim 2 using other ranking algorithms, such as, Tarantula, Op2, Barinel and etc. This, however remains for future work.

< Still have to justify why have we not compared with other slicing approaches >

< Not sure what to say about the name, do we agree?>

We agree that our theorems are rather observations or properties of the ranking algorithm. Thus, these misconceptions will be addressed on the paper.

## Review 263474:

**issue 8:** 
> I have not the highest confidence with the field but my feeling is that the problem is interesting and the results are valuable. My only concern is whether the **investigated issue fits the main topics of the conference** (no comment of author(s) helps in this sense). For sure this kind of paper would be more appropriate in conferences on software engineering, validation and testing. In those venues I had proposed acceptance. In this context I’m a little bit puzzled.

**Rebuttal:**

We kindly thank the reviewer for the comments on our work. 

As we mention in section 2, applications of model-based diagnosis to localize software faults have demonstrated that can be framed as dynamic slicing which is the technique proposed to improve software fault localization. Model-based diagnosis is a well-known approach that has been proposed by the diagnosis community. This community develops algorithms and techniques that leverage AI to determine the rootcause of observed faults. We agree that this paper will be a good suit in software engineering, validation and testing conferences but we also strongly believe that this paper can be published at IJCAI since we are applying AI to improve SBFL.

## Other points

### Improvements

* An area for improvement is the formality of the whole paper.

### Minor Issues

* Theorem 1 -> Claim 1

* Applications of MBD to localize software faults have demonstrated that it ... -> which it?

* Threats to validity -> Threats to Validity

### Future Work

* It would be interesting to compare/combine the proposed algorithm with machine learning. Of course, such a study would not fit a 6 pp conference paper. Here is a link that is relevant to the study:

> Baah, George K., Alexander Gray, and Mary Jean Harrold. "On-line anomaly detection of deployed software: a statistical machine learning approach." Proceedings of the 3rd international workshop on Software quality assurance. ACM, 2006.

**note:** Should the next point be addressed in the rebuttal using Rui's paper (*Evaluating and improving fault localization*) ?
* An obvious improvement would be to parameterize the approach to  allow plugging in multiple different ranking algorithms. That  immediately raises the question: does the observation that the rank of faulty statements cannot decrease if the slice includes the  faulty statements also work with other ranking algorithms than  Ochiai? 

* It feels that calling the observation a theorem is a bit  ambitious. Perhaps such property is something to characterize the ranking algorithms by?

* A more labour intensive approach would be to also parameterize  the approach over different slicing implementations, or at least  foresee the need and make it very clear how to change the slicing algorithm. 

* Perhaps the approach should be called DS-SBFL instead of Tandem-FL?  The reason being that there are multiple things that could be used  in tandem in the fault localisation context (for example a tandem of  some symbolic FL approach with an additional technique).

* Theorem 1 is not a theorem, it is rather an observation, because it  depends on the simplifications used by the slicing  algorithm.

* Theorem 2 is actually a property of the Ochiai ranking formula, not a theorem.

