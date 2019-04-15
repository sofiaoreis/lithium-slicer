# Paper\# 6364: Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization}

###Review \#210912
**Summary:** This paper deals with combining dynamic slicing with spectrum-based fault localization with the purpose of improving the overall debugging quality, i.e., providing a better ranking that allows programmers to more quickly find faults responsible for detected failures. The paper tackles an interesting challenge, i.e., automated debugging, that is still active. The paper is well written and structured. The ideas behind the approach are well explained and the paper also includes an empirical evaluation that is based on well-known example programs that are often used for evaluating debugging approaches.

**Weakness (1):** The approach itself, i.e., combining the mentioned debugging approaches is not that novel (as also indicated in the paper) and there are other papers describing such improvements. This is definitely a weakness of this paper.

However, there is an empirical evaluation that is novel capturing important research questions. 

**Weakness (2):** Of course – and like other similar paper – the study is limited to some programs and generalization is always questionable. In this particular case, I would argue that the combination of slicing and spectrum-based fault localization should lead to improvements because of the fact that we can rule out some components that do not influence the computation of wrong values. The study itself is fine but there are some issues the authors should discuss. From Table 3 and Table 4 we see that basically slicing alone leads to improvements, because the values for Tandem-FL and slicing are the same. I am also wondering why there is a small value for commons-lang in case of k=10 when compared with k=5? I would assume that taking care of more statements should improve debugging performance.


In addition, there is no discussion of drawbacks behind the approach. Spectrum-based fault localization is successful because it does not require a lot of tools and can be more or less easily adapted for other programming languages. This is not the case for slicing. For slicing we require to know not only that a test case is failing but also to identify all output variables that deliver wrong values. In case of exceptions (as discussed a little bit in the paper) we may also use different slicing approaches to improve the results. There is some work on dynamic slicing in case of exceptions. Moreover, slicing needs more time for analysis and running time might become an issue.


In summary, the paper provides a novel evaluation of a not so novel debugging approach. The paper is well written but there is still room for improvement. The main issues are regarding missing discussions about limitations and drawback, and the empirical evaluation, which may need more detailed explanations.

###Review \#252039

> This paper proposes a novel approach to automated debugging: dynamic slicing + software fault localization. The paper is empirical in nature and shows good degree of scholarship: it is actually rare to see such comprehensive empirical study published at a conference. The results from study are promising and the reader is convinced that the combination of the two approaches yields better fault isolation compared to each approach separately.

> It would be interesting to compare/combine the proposed algorithm with machine learning. Of course, such a study would not fit a 6 pp conference paper. Here is a link that is relevant to the study:

> Baah, George K., Alexander Gray, and Mary Jean Harrold. "On-line anomaly detection of deployed software: a statistical machine learning approach." Proceedings of the 3rd international workshop on Software quality assurance. ACM, 2006.

> An area for improvement is the formality of the whole paper.

> Some minor issues:

> 1. Theorem 1 -> Claim 1

> 2. Applications of MBD to localize software faults have demonstrated that it ... -> which it?

> 3. Threats to validity -> Threats to Validity


###Review \#263473


The paper titled "Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization" provides an account of a comprehensive amount of experiments using a combination of dynamic slicing and Ochiai ranking based spectrum-based fault localization on Java benchmarks available in the Defects4J project.

The idea of proposing a baseline approach combining dynamic slicing with spectrum-based fault localisation makes sense, as many authors seem to have discovered and explored it to some extent in numerous publications, many of which are cited by the authors. The fact that recent surveys on fault localisation have not had such a benchmark on record confirms the need.

However it seems that the goal is rather ambitious because many people have tried the combination and the authors of the current paper are left with the tedious task of sifting though all previous results to make sure the new baseline is a comprehensive summary of previous results. The authors say in the Related Work section on page 6 that many authors have previously investigated the combination of DS and SBFL, but their approaches were evaluated on rather small set of benchmarks. The main contribution of the current paper is running DS-SBFL on a larger set of benchmarks.

Thus the contribution of the paper is a an extensive experiment of how well the combination of Ochiai ranking performs with respect to the combination of dynamic slicing together with Ochiai ranking.

The work is important and the authors have been very careful with applying a methodological approach. However, it seems that such refactoring contributions seem to better fit into the journal setting where the reviewers can actually take a look at the proposed implementation and the authors are not so constrained with space.

Some suggestions for future work:

* An obvious improvement would be to parameterize the approach to  allow plugging in multiple different ranking algorithms. That  immediately raises the question: does the observation that the rank of faulty statements cannot decrease if the slice includes the  faulty statements also work with other ranking algorithms than  Ochiai? It feels that calling the observation a theorem is a bit  ambitious. Perhaps such property is something to characterize the ranking algorithms by?

* A more labour intensive approach would be to also parameterize  the approach over different slicing implementations, or at least  foresee the need and make it very clear how to change the slicing algorithm. It is very nice that the authors have started with critical slicing as one of the earlier appropriate approaches.

* Perhaps the approach should be called DS-SBFL instead of Tandem-FL?  The reason being that there are multiple things that could be used  in tandem in the fault localisation context (for example a tandem of  some symbolic FL approach with an additional technique).

* Theorem 1 is not a theorem, it is rather an observation, because it  depends on the simplifications used by the slicing  algorithm.

* Theorem 2 is actually a property of the Ochiai ranking formula, not a theorem.


###Review \#263474

The topic of the paper is software debugging. In particular, a methodology for locating the faulty code is experimentally evaluated. The considered methodology combines two well know techniques: (a) Dynamic  (DS) which reduce the code by removing the parts which not contribute to the fault; (b) Spectrum-based Fault Localization (SFL) which computes suspiciousness values associated with program components based on coverage information. The two techniques are suitable combined (DS is exploited to enhance the results of SFL). As correctly reported in the paper the idea of combining the two techniques is not new and it has already checked for effectiveness. The claim of the author(s) is that the more extended experimental setting provided in the this paper and the more rigorous methodological approach allow to reassess the results of the previous investigation in favor of the combination.

The paper is well structured and it is well written. I have not the highest confidence with the field but my feeling is that the problem is interesting and the results are valuable. My only concern is whether the investigated issue fits the main topics of the conference (no comment of author(s) helps in this sense). For sure this kind of paper would be more appropriate in conferences on software engineering, validation and testing. In those venues I had proposed acceptance. In this context I’m a little bit puzzled.

