# Demystifying the Combination of Dynamic Slicing and Spectrum-based Fault Localization

### Prep. Camera-Ready (w/o Closure) - May, 12-19:

- [x] <del>Add authors</del>
- [x] Acknowledgments (Falta o Marcelo adicionar)

##### Reviewer 1:

- [ ] In this particular case, I would argue that the combination of slicing and spectrum-based fault localization should lead to improvements because of the fact that we can rule out some components that do not influence the computation of wrong values. The study itself is fine but there are some issues the authors should discuss. From Table 3 and Table 4 we see that basically slicing alone leads to improvements, because the values for Tandem-FL and slicing are the same. 

- [ ] I am also wondering why there is a small value for commons-lang in case of k=10 when compared with k=5? I would assume that taking care of more statements should improve debugging performance.

- [ ] There is no discussion of drawbacks behind the approach. Spectrum-based fault localization is successful because it does not require a lot of tools and can be more or less easily adapted for other programming languages. This is not the case for slicing. For slicing we require to know not only that a test case is failing but also to identify all output variables that deliver wrong values. In case of exceptions (as discussed a little bit in the paper) we may also use different slicing approaches to improve the results. There is some work on dynamic slicing in case of exceptions. Moreover, slicing needs more time for analysis and running time might become an issue.

##### Reviewer 2:

- [ ] Formality of the whole paper
- [x] <del>Theorem 1 -> Claim 1</del>
- [ ] Applications of MBSD to localize software faults have demonstrated that it ... -> which it?
- [x] <del>Threats to validity -> Threats to Validity</del>

##### Reviewer 3:

- [x] Theorems -> Claims or observations (?!).
- [ ] Clear indication what properties are related to which part of the combinaition, i.e. which property is due to the ranking algorithm, which due to the slicing.
- [ ] A clear indication what needs to be done and checked in order to test alternative slicing and ranking algorithms.

##### Reviewer 4:

- [ ] My only concern is whether the investigated issue fits the main topics of the conference (no comment of author(s) helps in this sense). - Improve!

##### More points to address:

- [ ] Add MBSD Connection into the conclusion
- [ ] Defects4j Table (review)
- [ ] Coverage (Tab. 2)
- [ ] Review paper to find references to dataset and tool publication (fix them)
- [ ] Prep. Dataset Results for publication
- [ ] Prep. Tool for publication
 
### Prep. Camera-Ready (w/ Closure)  - May, 20-31:

 - [ ] Retrieve Closure Results
 - [ ] Add Closure Results to the paper
 - [ ] Re-do Abstract, Introduction, Evaluation and Conclusions using the new results
