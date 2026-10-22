#import "common.typ": *
#show: setup.with(paper: "a4", x: 0.6in)
#set document(title: "Viraj Sanghavi - Biodata")

#let fields(..rows) = grid(
  columns: (1.3in, 1fr),
  row-gutter: 0.55em,
  ..rows.pos().map(((k, v)) => ([*#k*], v)).flatten(),
)

#align(center)[
  #text(size: 12pt, weight: "bold")[BIODATA]
  #v(0.5em)
  #text(size: 17pt, weight: "bold")[Viraj Sanghavi]
  #v(0.2em)
  #text(size: 9pt)[Computer Engineering Undergraduate #sep AI/ML and Federated Learning Research]
]

= Personal Details
#fields(
  ([Full Name], [Viraj Sanghavi]),
  ([Location], [Mumbai, India]),
  ([Email], link("mailto:virajsanghavi000@gmail.com")[virajsanghavi000\@gmail.com]),
  ([Phone], [+91-8104488190]),
  ([LinkedIn], link("https://linkedin.com/in/virajsanghavi")[linkedin.com/in/virajsanghavi]),
  ([GitHub], link("https://github.com/VirajSanghavi007")[github.com/VirajSanghavi007]),
  ([Kaggle], link("https://www.kaggle.com/virajsanghavi007")[kaggle.com/virajsanghavi007]),
)

= Education
#fields(
  ([Degree], [B.Tech in Computer Engineering (expected 2028)]),
  ([Institution], [Dwarkadas J. Sanghvi College of Engineering, Mumbai]),
  ([Current Status], [Semester 5 (ongoing), Sept 2024 to present]),
  ([CGPA], [9.15]),
  ([Coursework], [Data Structures, Algorithms, Statistics, Machine Learning]),
)

= Research
#proj([Publicity & Research Member, DJS Anveshan (Research Club), DJSCE], [Ongoing]) \
_Topic: Failure Modes in Federated Learning for Cross-Institutional Fraud Detection_ \
_Status: early stage; problem framing and literature review in progress_

#v(0.4em)
*Problem being studied*
- Byzantine-robust aggregators (Krum, FLAME) filter client updates that look unlike the majority. An honest institution with non-IID data can look the same as an attacker, so its valid updates may be discarded.
- The global model can then report high aggregate accuracy while failing on that institution's fraud patterns, with no signal at the server.

*Current work*
- Refining the problem statement and threat model (e.g. two similar international banks and one regional bank in a joint fraud model).
- Building a literature map of robust aggregation under heterogeneous data to identify what remains open.

*Planned next steps:* form testable hypotheses, then run federated simulations on public fraud datasets comparing FedAvg, Krum, Median, Trimmed Mean and FLAME using per-client metrics.

*Keywords:* Federated Learning, Byzantine Robustness, Non-IID Data, Fraud Detection

= Research-Oriented Projects
#proj([#ulink("https://github.com/VirajSanghavi007/Vigilia")[Vigilia], Graph-Native AML Detection], [Jan 2025 to present])
- Started as Argus at iDEA 2.0 (Union Bank of India, Top 40+ finalist); detected 8 structural AML typologies and 7 behavioural signals on 500K+ synthetic transactions; being rebuilt with a GNN detection layer.

#proj([TinyML, CIFAR-10 on a Microcontroller Budget], [Oct 2026 to present])
- Compressed a ResNet-18 teacher (93.3%) to an int8 model at 84.8% accuracy in 70.6#sym.space.thin KB flash and 16#sym.space.thin KB peak RAM via Once-for-All NAS, structured pruning, and KD + QAT, with every stage benchmarked against baselines.

= Professional Experience
- *Developer Intern*, Aelius Turbina LLP, Mumbai #h(1fr) Sept 2026 to present
- *Developer Intern*, ITAakash Strategic Software Pvt. Ltd., Mumbai #h(1fr) June 2026 to Aug 2026

= Technical Skills
*Languages / Infra:* Python, SQL, TypeScript, Bash, C++, Git, Docker, FastAPI, PostgreSQL \
*ML / Data:* PyTorch, PyTorch Geometric, NAS, Pruning, Quantization (QAT), scikit-learn, XGBoost, LightGBM, Hugging Face

#v(1fr)
*Declaration:* I hereby declare that the information furnished above is true to the best of my knowledge.

#v(18pt)
*Place:* Mumbai #h(1fr) *Viraj Sanghavi* \
*Date:* #box(width: 1.2in, line(length: 100%, stroke: 0.4pt))
