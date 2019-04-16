# Paper 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Review 210912:

**issue 1:** Not sure if this point needs comments.
> The approach itself, i.e., combining the mentioned debugging approaches is not that novel (as also indicated in the paper) and there are other papers describing such improvements. This is definitely a weakness of this paper. However, there is an empirical evaluation that is novel capturing important research questions. 

**issue 2:** 
> Of course – and like other similar paper – the study is limited to some programs and generalization is always questionable. 

**issue 3:** 
I think the reviewer is confused because we present the results of DS two times in different tables.
> From Table 3 and Table 4 we see that basically slicing alone leads to improvements, because the values for Tandem-FL and slicing are the same. 

**issue 4:** 
Explain why it can be worse.
> I am also wondering why there is a small value for commons-lang in case of k=10 when compared with k=5? I would assume that taking care of more statements should improve debugging performance.

**issue 5:** 
> In addition, there is no discussion of drawbacks behind the approach. Spectrum-based fault localization is successful because it does not require a lot of tools and can be more or less easily adapted for other programming languages. This is not the case for slicing. For slicing we require to know not only that a test case is failing but also to identify all output variables that deliver wrong values. In case of exceptions (as discussed a little bit in the paper) we may also use different slicing approaches to improve the results. There is some work on dynamic slicing in case of exceptions. 

**issue 6:** 
> Moreover, slicing needs more time for analysis and running time might become an issue.

### Review 252039:

No problems found on this review. 

### Review 263473:

**issue 7:** 
Should we try to address this review?
> The work is important and the authors have been very careful with applying a methodological approach. However, it seems that such refactoring contributions seem to better fit into the journal setting where the reviewers can actually take a look at the proposed implementation and the authors are not so constrained with space.


## Review 263474:

**issue 8:** 
Focus on model-based diagnosis!
> I have not the highest confidence with the field but my feeling is that the problem is interesting and the results are valuable. My only concern is whether the **investigated issue fits the main topics of the conference** (no comment of author(s) helps in this sense). For sure this kind of paper would be more appropriate in conferences on software engineering, validation and testing. In those venues I had proposed acceptance. In this context I’m a little bit puzzled.

### Improvements

* An area for improvement is the formality of the whole paper.

### Minor Issues

* Theorem 1 -> Claim 1

* Applications of MBD to localize software faults have demonstrated that it ... -> which it?

* Threats to validity -> Threats to Validity

### Future Work

* It would be interesting to compare/combine the proposed algorithm with machine learning. Of course, such a study would not fit a 6 pp conference paper. Here is a link that is relevant to the study:

> Baah, George K., Alexander Gray, and Mary Jean Harrold. "On-line anomaly detection of deployed software: a statistical machine learning approach." Proceedings of the 3rd international workshop on Software quality assurance. ACM, 2006.

**note:** this seems to be a point we should address in the rebuttal using Rui's paper (*Evaluating and improving fault localization*).
* An obvious improvement would be to parameterize the approach to  allow plugging in multiple different ranking algorithms. That  immediately raises the question: does the observation that the rank of faulty statements cannot decrease if the slice includes the  faulty statements also work with other ranking algorithms than  Ochiai? 

* It feels that calling the observation a theorem is a bit  ambitious. Perhaps such property is something to characterize the ranking algorithms by?

* A more labour intensive approach would be to also parameterize  the approach over different slicing implementations, or at least  foresee the need and make it very clear how to change the slicing algorithm. 

* Perhaps the approach should be called DS-SBFL instead of Tandem-FL?  The reason being that there are multiple things that could be used  in tandem in the fault localisation context (for example a tandem of  some symbolic FL approach with an additional technique).

* Theorem 1 is not a theorem, it is rather an observation, because it  depends on the simplifications used by the slicing  algorithm.

* Theorem 2 is actually a property of the Ochiai ranking formula, not a theorem.

