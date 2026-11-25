# Design note

This note covers the main trade-offs, the known limitations, and one example of how an LLM harness was used. The setup and invocations are in the [README](README.md).

## Principles

1. **Robustness first.** The tools must work when the data changes, and are designed to work on a different schema. Nothing about TPC-H is hard-coded: it is either discovered from the database or set in config.
2. **The LLM's output must be checkable.** The LLM quotes phrases from a question and links each one to a table, a column (with a value) or a query shape. Code checks every link against the database. Nothing writes SQL to answer a question, which keeps the evaluation independent of any model's SQL skills.
3. **Code does what must be exact:** exactly N questions, unique IDs, schema and value checks, duplicate detection, selection and all score arithmetic.

## Generator: main trade-offs

**1. Over-generate, check, then select.** The LLM writes a pool of candidates: max(2N, 16) targeted at specific query shapes, plus free-form ones. Code drops the ones that fail checks and greedily picks exactly N.

- **For:** the budget is honored by code, not by asking the LLM, and every choice is traceable in `pool.json` and `pick_log.json`. The selection objective has diminishing returns (it is monotone submodular), so greedy is provably within 1 − 1/e ≈ 63% of the best subset of the pool (Nemhauser, Wolsey & Fisher, 1978; proof in Krause & Golovin, 2014). In practice each run measures it: 100% on the demonstration pools, exact at N = 5, via a swap search at N = 15.
- **Against:** the pool is the ceiling. Selection can't cover a column no candidate mentions. At N = 15 the pool reached 35 columns and selection used 26.

**2. Small budgets go to query shapes first.** A candidate's gain is 0.5 × (new shape value) + 0.25 × (new tables) + 0.25 × (new columns), normalized so that covering every shape, table or column once is worth 0.5, 0.25 and 0.25.

- **Why shapes:** query shapes (joins, rankings, ratios, anti-joins, time trends, and so on) are where Text-to-SQL systems differ most. Every table comes back as N grows.
- **The cost:** see case 1 in [reports/demo_analysis.md](reports/demo_analysis.md). At N = 5 the generator traded the `partsupp` table and the simple lookup shape for seven different shapes. Weighting the three dimensions equally would make the opposite trade.
- **These weights are judgment calls.** Every run reports how many picks would change under other settings, so the choice stays visible.

**3. Each shape is weighted by frequency (F) and difficulty (I):** W = (0.4·F + 0.6·I) / 3.

- **F (how often analysts ask for it):** an estimate. No usage data exists for this taxonomy.
- **I (how much it tests a system):** calibrated from the human difficulty labels of BIRD (Li et al., 2023), using its 500-question Mini-Dev set (`calibration/bird_i.py`). The result was stretched to a 1–3 scale, and shapes with fewer than 20 BIRD examples kept their hand-set value.
- **Shape explains little of difficulty:** R² = 0.16. That is consistent with BIRD's own rubric, which rates difficulty on question understanding, knowledge reasoning and data complexity as well as SQL complexity (Li et al., 2023, Appendix B.1). So I is a starting point, to be replaced by measured failure rates once a real Text-to-SQL system is run.
- **Adding rather than multiplying F and I is deliberate.** Risk-based testing usually multiplies likelihood by impact (Felderer & Schieferdecker, 2014), which here would mean "expected failures users would see". This suite is for diagnosis instead: covering a taxonomy of capabilities so that weaknesses show (Ribeiro et al., 2020; Liang et al., 2023). Adding lets rare but hard shapes keep their weight.

**4. Same computation, different wording = duplicate.** Two candidates with the same linked tables, columns and shapes are one computation, even if their filter values differ, so only the first is kept. The weak point: two paraphrases linked differently slip through. The coverage judge's repetition check is the backstop, and the controlled check tests the case on purpose.

**5. Realism vs coverage, as a preset.**

- **The default (`coverage`) rewards questions that combine several shapes,** and that can make them contrived.
- **The `natural` preset** doubles the free-form slots, drops questions with more than 2 shapes, requires at least ⌈0.2·N⌉ free-form picks, and weights frequency above difficulty. The quota is a matroid constraint, under which greedy keeps a 1/2 guarantee (Fisher, Nemhauser & Wolsey, 1978).
- **Measured at N = 5:** 1.6 shapes per question instead of 2.2, and plainer questions, but 5 shapes covered instead of 7.

**6. Coverage is defined by the schema, not the data.** All 61 columns count, including keys, comments and a column that is constant in this data. That keeps the measure stable when the data changes. The cost: the generator's realism rules avoid keys, comments and constants, so column coverage can't exceed about 38 of 61 under the current rules.

**7. A fresh pool every run.** Runs are traceable but not repeatable: the saved pool and pick log explain every choice, but a rerun writes different candidates. That keeps each demonstration case an honest, independent generation from the database, docs and N.

## Generator: known limitations

- **The skills can read files beyond their inputs.**
  - **Why:** they run with the repository as their working directory, and Claude Code lets them read anything in it. The skills' "only run these commands" is an instruction, not an enforced limit.
  - **What happened:** session transcripts show generator runs reading the checker's source code and other runs' candidates. In v2, the `natural` run read the `coverage` run's candidates, so those two aren't fully independent.
  - **What held:** no judge read the labeled question file it was judging; that rule *is* enforced.
  - **The fix,** left for a future version: run each step in a folder holding only its inputs, with code driving the steps.
- **No end-to-end proof that a question is computable,** only that every element exists, every value is real and the tables connect. Links to the wrong-but-existing column (e.g. "revenue" linked to the gross price only) pass the checks.
- **Join inference on very small tables.** Without declared keys, joins are inferred from names and values. On TPC-DS at SF 0.01, single-row tables make every column look like a key, giving 197 inferred joins, many spurious. The TPC-DS run still produced sensible questions on real join paths, but the rule should also require key-like names.
- **Very large N and large schemas.** All candidates are written in one pass (45 at N = 15 worked; around 150 likely wouldn't fit in one response). Every candidate sees the whole schema card. Both would need batching or a narrower context per target.
- **Target assignment is mechanical.** Shapes and focus tables rotate, so some pairings make little sense (e.g. anti-join with the five-row region table), and shapes listed last get one fewer target when slots don't divide evenly.

## Judges: main trade-offs

**1. Judges rebuild the evidence from the text alone.**
- **How:** each judge sees only question IDs and text. Reading the question file is blocked, so the generator's labels never reach it. It writes its own links, code checks them, and code then compares them with the labels.
- **Labels never earn credit.** This follows the finding that a judge which works the task out first and then grades is far more reliable than one that grades directly (Zheng et al., 2023).
- **For:** the judges work on any edited list, and a disagreement with the generator is visible as a contradicted label.
- **Against:** every question is read twice by an LLM (once by the generator, once by each judge), which is where the cost goes.

**2. Four verdicts, tested in a fixed order.**
- **The scale:** `OFF_TOPIC`, `MISSING_DATA`, `AMBIGUOUS`, `ANSWERABLE`. It maps almost one-to-one onto an established Text-to-SQL answerability taxonomy: improper, needs external knowledge, ambiguous, answerable (Zhang et al., 2020). That taxonomy's fifth class, operations SQL can't express, is folded into `MISSING_DATA` here.
- **The order:** the first verdict that applies wins, so a question that is both missing data and ambiguous is `MISSING_DATA`. No reading of it can be answered.
- **The evidence each verdict needs** is checked by code: links for every concept, a `missing` link naming the concept and the closest columns, or two or more readings that each pass the checks. The pattern is "the LLM proposes, sound verifiers check" (Kambhampati et al., 2024). Unfixable evidence problems are accepted only explicitly, and flagged in the report.

**3. Correctness score = (answerable + 0.5 × ambiguous) / N.** An ambiguous question can be answered under some reading but can't be graded reliably, so it gets half credit. The 0.5 is a policy choice; the verdict counts are always in the report, so any other weight can be applied by hand.

**4. An explicit ambiguity checklist.** Models are much better at answering than at noticing a second reading:
- the best model in AMBROSIA found all readings of ambiguous questions only 31% of the time (Saparina & Lapata, 2024);
- GPT-4's disambiguations were right 32% of the time, against 90% for humans (Liu et al., 2023).

So before choosing `ANSWERABLE`, the correctness judge goes through seven ambiguity types drawn from Text-to-SQL ambiguity benchmarks (Bhaskar et al., 2023; Saparina & Lapata, 2024; Dong et al., 2025): which column or table, stored vs computed, join or not, scope, attachment, vague filters, relative time. Both judges also check every column link for another column that fits as well. In the demonstration runs, the rationales name the close second reading they rejected and why. One example: "o_totalprice was rejected since it includes tax and cannot be split by ship mode".

**5. Coverage credit is strict.**
- **What earns credit:** only the coverage judge's own links that pass the checks and point to one target. A phrase that could mean two columns earns nothing, and a question with a concept that has no data earns nothing at all: a question that can't be answered exercises nothing.
- **Eligible items:** every table, column and shape in the schema (generator trade-off 6 above).
- **The score:** (table % + column % + shape %) / 3, with equal thirds, deliberately different from the generator's selection weights.
- **Why the dimensions come first in the report:** tables and shapes fill up within a few questions, so the average hides trade-offs. The v1 and v2 five-question sets both score 65.98, one with 8/8 tables and 6/8 shapes, the other with 7/8 and 7/8.
- **Repetition is shown, not scored:** duplicate pairs, questions covering nothing unique, questions earning nothing. There's no overlap ratio, because it rises with N even when nothing is wasted.

**6. Validated by controlled edits, repeatability and, next, human labels.**
- **The controlled check** replaced two questions with an unanswerable one and a paraphrase. All seven expectations committed before the run were met: the unanswerable question became `MISSING_DATA` and the correctness score fell from 1.00 to 0.93; coverage stayed at 80.87, with a duplicate pair and a question earning nothing flagged.
- **Repeatability:** judging the same file twice gave identical verdicts and coverage.
- **A labeled set:** LLM judges' reliability varies by task and has to be measured against labels (Bavaresco et al., 2025). On 20 questions written to cover all four verdicts (8 missing data, 5 ambiguous, 5 answerable, 2 off-topic), the correctness judge agreed on 19 (Cohen's κ 0.93). It caught all five ambiguous questions. The one disagreement was a case flagged as borderline in advance, "What is the population of GERMANY?": labeled off-topic, judged missing data. Both score 0. The labels were drafted by Claude and approved by the user, so they are not independent human labels (see limitations).

## Judges: known limitations

- **One model family for the generator and both judges.** LLM evaluators recognize and favor their own text (Panickssery et al., 2024), LLM-built benchmarks favor the model that built them (Xu et al., 2025), and strong models make correlated errors even across providers (Kim et al., 2025).
  - So agreement between the generator's labels and the judges' links is not evidence of correctness. Both readings may share a mistake.
  - Skills can only run Claude models, so a second family isn't available here. Human labels are the reference.
- **Judge accuracy is only partly measured.**
  - The controlled check covers two defect types.
  - The 20-question labeled set gives a rough estimate: one disagreement moves agreement by 5 points.
  - Its labels come from the same model family as the judge, approved by the user rather than written independently.
  - It is weighted toward failures (15 of 20), so it measures how well the judge tells failure types apart more than its behavior on typical answerable sets.
  - The coverage judge's links aren't validated against labels.
  - The line between off-topic and missing data is fuzzy for questions that name an entity in the database.
- **Links to the wrong but existing column pass the checks.** For example, "revenue" linked to the gross price alone. Code can check that an element exists, not that it's the right one.
- **Coverage is high by construction.** The generator optimizes something close to what the coverage judge measures, a setup prone to Goodhart effects (Manheim & Garrabrant, 2018). In software testing, coverage correlates only weakly with finding faults once suite size is controlled (Inozemtseva & Holmes, 2014). Coverage is a diagnostic of what the set exercises, not a quality score. The correctness judge and the controlled check are the signals the generator doesn't optimize.
- **Judges can read files beyond their inputs,** as the generator can. In v1, one judge read the checker's source and an earlier run's output. The rule that matters, never reading the labeled question file, is enforced and held.
- **All questions are judged in one session,** so order effects are possible, though they are reported as small for per-question classification.

## How the LLM harness was used: the literature review

**Delegated.** An autonomous research agent wrote a literature review on choosing a small test suite under a budget, and on LLM judges. It was told to check every reference, and produced 101 of them. The review itself stays private; the sources behind what we took from it are cited here and listed below.

**Checked.** Its claims weren't taken at face value. Each one about our generator was rerun as code on the saved candidate pools, with no extra LLM calls:

- **Greedy vs optimum:** the review said greedy is provably near-optimal for our objective, citing the submodular guarantee (Nemhauser, Wolsey & Fisher, 1978; Krause & Golovin, 2014). Computing the exact optimum at N = 5 (20,349 subsets) and a swap search at N = 10–15 put greedy at 98.7–99.9% of the best.
- **The pool as the bottleneck:** the review said the guarantee is relative to the pool, so the pool, not the weights, limits coverage. The pools reached 30–34 columns, and selection used 14–30 of them.
- **Realism:** the review warned that rewarding combined shapes trades away realism. AutoBencher pairs difficulty with an explicit salience goal for that reason (Li et al., 2025). Free-form questions won 0 of 5, 1 of 10 and 4 of 15 picks.
- **Weight sensitivity:** the review called the weights guesses, against risk-based testing's practice of documenting a source for each value (Felderer & Schieferdecker, 2014). Nudging them changed 0–2 picks at N = 5 and up to 4 at N = 15.

**Accepted, changed, rejected.**

- **Accepted:** the realism finding, which became the `natural` preset; per-run diagnostics; reporting coverage by dimension before the summary score; and calibrating I from BIRD.
- **Rejected:** the suggested generation round aimed at uncovered columns. Checking the pools showed that 23 of the 27 columns no pool reached are keys and comments, which the realism rules exclude on purpose.
- **Corrected:** the review described BIRD's difficulty criteria as "question comprehension, schema linking and external knowledge". Reading the paper showed the actual rubric: question understanding, knowledge reasoning, data complexity and SQL complexity (Li et al., 2023, Appendix B.1).
- **Contradicted by the data:** the review's hint that ranking deserves a higher difficulty didn't survive. It rested on the BIRD paper's remark that models differ widely on ranking questions (Li et al., 2023, Section 6.6), but BIRD's own labels put ranking barely above a simple lookup.

## References

- Bavaresco, A., Bernardi, R., Bertolazzi, L., et al. (2025). LLMs instead of human judges? A large scale empirical study across 20 NLP evaluation tasks. *ACL 2025*. https://arxiv.org/abs/2406.18403
- Bhaskar, A., Tomar, T., Sathe, A., & Sarawagi, S. (2023). Benchmarking and improving text-to-SQL generation under ambiguity. *EMNLP 2023*. https://aclanthology.org/2023.emnlp-main.436/
- Dong, M., Kumar, N. A., Hu, Y., et al. (2025). PRACTIQ: A practical conversational text-to-SQL dataset with ambiguous and unanswerable queries. *NAACL 2025*. https://aclanthology.org/2025.naacl-long.13/
- Felderer, M., & Schieferdecker, I. (2014). A taxonomy of risk-based testing. *International Journal on Software Tools for Technology Transfer*, 16(5), 559–568. https://doi.org/10.1007/s10009-014-0332-3
- Fisher, M. L., Nemhauser, G. L., & Wolsey, L. A. (1978). An analysis of approximations for maximizing submodular set functions—II. *Mathematical Programming Studies*, 8, 73–87. https://doi.org/10.1007/BFb0121195
- Inozemtseva, L., & Holmes, R. (2014). Coverage is not strongly correlated with test suite effectiveness. *ICSE 2014*, 435–445. https://doi.org/10.1145/2568225.2568271
- Kambhampati, S., Valmeekam, K., Guan, L., et al. (2024). Position: LLMs can't plan, but can help planning in LLM-Modulo frameworks. *ICML 2024*, PMLR 235. https://proceedings.mlr.press/v235/kambhampati24a.html
- Kim, E., Garg, A., Peng, K., & Garg, N. (2025). Correlated errors in large language models. *ICML 2025*. https://arxiv.org/abs/2506.07962
- Krause, A., & Golovin, D. (2014). Submodular function maximization (survey chapter; the greedy bound is Theorem 1.5). Author copy: https://las.inf.ethz.ch/files/krause12survey.pdf
- Li, J., Hui, B., Qu, G., et al. (2023). Can LLM already serve as a database interface? A BIg bench for large-scale database grounded text-to-SQLs (BIRD). *NeurIPS 2023 Datasets and Benchmarks Track*. https://arxiv.org/abs/2305.03111. Mini-Dev set: https://huggingface.co/datasets/birdsql/bird_mini_dev
- Li, X. L., Kaiyom, F., Liu, E. Z., et al. (2025). AutoBencher: Towards declarative benchmark construction. *ICLR 2025*. https://arxiv.org/abs/2407.08351
- Liang, P., Bommasani, R., Lee, T., et al. (2023). Holistic evaluation of language models. *Transactions on Machine Learning Research*. https://arxiv.org/abs/2211.09110
- Liu, A., Wu, Z., Michael, J., et al. (2023). We're afraid language models aren't modeling ambiguity. *EMNLP 2023*. https://arxiv.org/abs/2304.14399
- Manheim, D., & Garrabrant, S. (2018). Categorizing variants of Goodhart's law. arXiv:1803.04585. https://arxiv.org/abs/1803.04585
- Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming*, 14, 265–294. https://doi.org/10.1007/BF01588971
- Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM evaluators recognize and favor their own generations. *NeurIPS 2024*. https://arxiv.org/abs/2404.13076
- Ribeiro, M. T., Wu, T., Guestrin, C., & Singh, S. (2020). Beyond accuracy: Behavioral testing of NLP models with CheckList. *ACL 2020*. https://aclanthology.org/2020.acl-main.442/
- Saparina, I., & Lapata, M. (2024). AMBROSIA: A benchmark for parsing ambiguous questions into database queries. *NeurIPS 2024 Datasets and Benchmarks Track*. https://arxiv.org/abs/2406.19073
- Xu, W., Agrawal, S., Zouhar, V., et al. (2025). When LLMs benchmark themselves: Deconstructing self-bias in automated evaluation. arXiv:2509.26600. https://arxiv.org/abs/2509.26600
- Zhang, Y., Dong, X., Chang, S., Yu, T., Shi, P., & Zhang, R. (2020). Did you ask a good question? A cross-domain question intention classification benchmark for text-to-SQL. arXiv:2010.12634. https://arxiv.org/abs/2010.12634
- Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*. https://arxiv.org/abs/2306.05685
