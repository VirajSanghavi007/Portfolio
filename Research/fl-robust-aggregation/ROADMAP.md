# Research Roadmap: Robust Aggregation vs. Honest Non-IID Clients in Federated Fraud Detection

Restart plan for the DJS Anveshan research topic. Each stage has a concrete output
("Done when") so progress is measurable. Tick boxes as you go.

---

## Stage 1: Find the problem (Week 1)

**Working problem statement**
Byzantine-robust aggregators (Krum, Multi-Krum, Trimmed Mean, Median, FLAME) treat
updates that look unlike the majority as malicious. In cross-institution fraud detection,
an honest bank with a different customer base (non-IID data) also looks unlike the majority.
Its updates get filtered out, the global model looks accurate on aggregate metrics, but it
fails on that bank's fraud patterns. Nobody notices, because the server only sees the
aggregate.

**Tasks**
- [ ] Write the problem in one paragraph (above is a draft) and one sentence.
- [ ] Draw the 3-bank example: 2 similar international banks, 1 regional bank.
- [ ] List who is harmed and how it would be measured (per-client recall, not global accuracy).

**Done when:** one-page problem note (`01_problem.md`) exists.

---

## Stage 2: Check for novelty (Weeks 1-2)

The danger here is that "robust aggregation hurts honest heterogeneous clients" is already
partly known. Your job is to find exactly what is NOT covered.

**Search queries** (Google Scholar, arXiv, Semantic Scholar, connectedpapers.com)
- "Byzantine robust aggregation non-IID honest clients"
- "robust aggregation heterogeneity false positive benign clients"
- "Krum non-IID", "FLAME non-IID", "FLTrust heterogeneity"
- "federated learning fraud detection banks"
- "fairness federated learning robust aggregation"
- "federated learning pre-deployment audit / verification"

**Known papers to read first** (verify citations yourself, do not trust from memory)
- Blanchard et al. 2017, Krum (NeurIPS)
- Yin et al. 2018, Median / Trimmed Mean (ICML)
- Karimireddy, He, Jaggi 2022, "Byzantine-Robust Learning on Heterogeneous Datasets via
  Bucketing" (ICLR). **Closest prior work: it already shows robust aggregators break under
  non-IID data. Read this carefully; your novelty must go beyond it.**
- Nguyen et al. 2022, FLAME (USENIX Security)
- Cao et al. 2021, FLTrust (NDSS)
- Li et al. 2020, q-FFL fairness in FL (ICLR)
- The "Li et al. IEEE 2024" paper from your old report: re-find it and get the exact citation.

**Novelty matrix** (fill one row per paper, in `02_related_work.csv`)
| Paper | Aggregator(s) | Non-IID setting | Measures per-client harm? | Fraud / tabular data? | Proposes detection or audit? |

**Candidate gaps** (keep only those the matrix confirms are open)
1. Per-client harm measurement (which honest clients get excluded, and how often) on tabular
   fraud data, rather than image benchmarks like CIFAR/MNIST.
2. A server-side **diagnostic** that flags "this excluded client is probably honest but
   different", without seeing raw data.
3. A pre-deployment audit protocol: a checklist/test suite to run before an FL consortium
   goes live.

**Done when:** 15-25 papers in the matrix, plus a one-paragraph "what is new" statement.
If the gap is already covered, return to Stage 1 and narrow (e.g. specific aggregator or
specific data shift type).

---

## Stage 3: Create hypotheses (Week 3)

Write them so an experiment can prove each one false.

- **H1 (harm exists):** Under label/feature skew (Dirichlet alpha <= 0.3), Krum and FLAME
  exclude an honest minority client in > X% of rounds, and that client's fraud recall drops
  by >= Y points versus FedAvg, while global accuracy changes by < 1 point.
- **H2 (dose-response):** Exclusion rate and per-client recall loss grow monotonically as
  heterogeneity increases (alpha from 10 down to 0.1).
- **H3 (separability):** Honest-but-different updates and truly malicious updates
  (label flipping, scaling attacks) are distinguishable using update statistics over several
  rounds (e.g. consistency of direction over time), even when single-round distance cannot.
- **H4 (fix, optional):** A diagnostic based on H3 recovers most of the lost minority recall
  while keeping attack success rate within Z% of the original robust aggregator.

Pick X, Y, Z after a pilot run, then freeze them before the main experiments.

**Done when:** `03_hypotheses.md` with each hypothesis, its metric, and the threshold.

---

## Stage 4: Design experiments (Week 3-4)

**Setup**
- Framework: Flower + PyTorch (or plain PyTorch simulation loop, simpler to debug).
- Data: Kaggle Credit Card Fraud (ULB), IEEE-CIS Fraud Detection, PaySim (synthetic).
  Partition into N = 5-20 "banks".
- Non-IID: Dirichlet over labels and/or merchant category / region (feature skew);
  one or more designated "regional" clients with a shifted distribution.
- Model: small MLP (tabular). Keep it simple, the aggregator is the subject, not the model.
- Aggregators: FedAvg (baseline), Krum, Multi-Krum, Median, Trimmed Mean, FLAME.
- Attacks (for H3/H4): label flipping, sign flipping, scaling / model replacement.

**Metrics**
- Global: accuracy, AUPRC (fraud is imbalanced, accuracy alone is misleading).
- Per-client: recall and AUPRC on each client's local test set; worst-client score.
- Exclusion rate: fraction of rounds each client's update is rejected / down-weighted.
- Attack success rate (when attacks are on).

**Experiment grid** (`04_experiments.md`)
| ID | Hypothesis | Aggregator | alpha | Attackers | Seeds |
|----|-----------|------------|-------|-----------|-------|
| E1 | H1 | all | 0.3 | 0 | 5 |
| E2 | H2 | all | 10, 1, 0.5, 0.3, 0.1 | 0 | 5 |
| E3 | H3 | Krum, FLAME | 0.3 | 10-20% | 5 |
| E4 | H4 | proposed vs. all | 0.3 | 0 and 20% | 5 |

**Done when:** grid fixed, seeds fixed, config files written, pilot (1 seed) runs end to end.

---

## Stage 5: Perform experiments (Weeks 5-8)

- [ ] Repo: `uv init`, config-driven runs, one results row per (experiment, seed).
- [ ] Unit/smoke/integration tests for partitioning, aggregators, and metrics.
- [ ] Checkpoint/resume: write each completed run to its own results file; skip runs already on disk.
- [ ] Progress counter + ETA in long sweeps; run detached.
- [ ] Log everything: config, git commit hash, seed, per-round exclusion lists.
- [ ] Report mean +/- std over seeds; significance test (paired t-test or Wilcoxon) for key claims.
- [ ] Record negative results too: if H1 fails, that is a finding.

**Done when:** every row of the grid has results for all seeds, plus plots:
exclusion rate vs. alpha, per-client recall bars, global vs. worst-client gap.

---

## Stage 6: Write the paper (Weeks 9-11)

Target: workshop paper (4-8 pages), e.g. an FL workshop at NeurIPS/ICML/ICLR, or an
IEEE student/Indian conference. Use the venue's LaTeX template from day one.

**Outline**
1. Abstract (write last)
2. Introduction: the 3-bank story, why it matters (GDPR, DPDP Act), contributions list
3. Related work: from the novelty matrix
4. Problem setup and threat model
5. Method (diagnostic/audit, if H4 pursued)
6. Experimental setup
7. Results: one subsection per hypothesis
8. Discussion and limitations (synthetic splits, dataset realism)
9. Conclusion

- [ ] Draft sections 4, 6, 7 first (they come straight from the work).
- [ ] Get mentor / Anveshan review, then revise.
- [ ] Release code on GitHub with a README reproducing every figure.

**Done when:** submitted, and the arXiv preprint is up.

---

## Biodata honesty checklist
Update the Research section of `Resume/latex/biodata.tex` to reflect the current stage only.
Don't claim a report or results until they exist.
