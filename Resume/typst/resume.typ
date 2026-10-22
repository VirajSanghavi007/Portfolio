#import "common.typ": *
#show: setup.with(paper: "us-letter", x: 0.5in)
#set document(title: "Viraj Sanghavi - Resume")

#align(center)[
  #text(size: 17pt, weight: "bold")[Viraj Sanghavi]
  #v(0.2em)
  #set text(size: 9pt)
  Mumbai, India #sep #link("mailto:virajsanghavi000@gmail.com")[virajsanghavi000\@gmail.com] #sep +91-8104488190 \
  #link("https://linkedin.com/in/virajsanghavi")[linkedin.com/in/virajsanghavi] #sep
  #link("https://github.com/VirajSanghavi007")[github.com/VirajSanghavi007] #sep
  #link("https://www.kaggle.com/virajsanghavi007")[kaggle.com/virajsanghavi007]
]

= Education
*Dwarkadas J. Sanghvi College of Engineering*, B.Tech in Computer Engineering #h(1fr) Sept 2024 -- present \
CGPA: 9.15 #h(1fr) Mumbai, India

= Experience
#entry([Developer Intern], [Aelius Turbina LLP], [Sept 2026 -- present], sub: [Solar BIPV manufacturer and EPC, Mumbai, India])
- Built a FastAPI pipeline that turns vendor Proforma Invoices (PDFs, scans, chat screenshots) into Zoho Books Purchase Orders via LLM/OCR extraction, GSTIN-verified vendor resolution, item matching, and a submitter + admin review loop
- Built a TallyPrime to Zoho Books sync over Tally's XML gateway with a cached OAuth layer, rate limiting, and GST-aware handling across two state registrations
- Built a self-hosted Tally BI dashboard (Sales, Purchase, Receivables, Cash Flow, P&L) with industry-standard KPIs (DSO, rate variance) over Tally ODBC
- Built an area-based lead engine merging MahaRERA, MCA, MPCB and Google Places into one SQLite store with cross-source dedupe, lead scoring, and human-approved outreach drafts

#entry([Developer Intern], [ITAakash Strategic Software Pvt. Ltd.], [June 2026 -- Aug 2026], sub: [Mumbai, India])
- Built an AI cash-flow forecasting system using Amazon Chronos-2, replacing a legacy XGBoost pipeline, predicting daily net cash flow across thousands of grouped financial records
- Designed a Flask API serving 365-day forecasts per (project, ledger, company) group, integrated into the existing Java EE ERP via PostgreSQL
- Implemented walk-forward backtesting (5 rolling origins, 4-month horizon) with bias correction for right-skewed construction cash flow data

= Projects
#proj([#ulink("https://github.com/VirajSanghavi007/Vigilia")[Vigilia] -- Graph-Native AML Detection], [Jan 2025 -- present])
- Started as Argus at iDEA 2.0 (Union Bank of India PS3, Team Zeta, Top 40+ finalist); continued past the hackathon under the name Vigilia
- Hackathon build detected 8 structural AML typologies plus 7 behavioural signals on 500K+ IBM synthetic transactions; now rebuilding it as a layered, production-target system with a GNN detection layer
- Built a Memgraph graph store with a Neo4j cold archive; cut Elliptic bulk load (204K nodes, 234K edges) from 17 min to 1.6 s via sharded LOAD CSV, benchmarked ingestion to 15M nodes, and fixed a MERGE index bottleneck causing throughput decay

#proj([#ulink("https://github.com/VirajSanghavi007/TinyML")[TinyML] -- CIFAR-10 on a Microcontroller Budget], [Oct 2026 -- present])
- Compressed a ResNet-18 teacher (93.3%) into an int8 model at 84.8% test accuracy in 70.6 KB flash and 16 KB peak RAM (100 KB / 20 KB budget) via Once-for-All supernet training, evolutionary search, structured pruning, and KD + QAT
- Benchmarked every stage against baselines (scratch CE/KD, pruning without fine-tune, PTQ vs QAT); checkpoint-resumable pipeline with unit, smoke and integration tests in GitHub Actions CI

= Research
#entry([Publicity & Research Member], [DJS Anveshan, Research Club], [Jan 2024 -- present], sub: [Dwarkadas J. Sanghvi College of Engineering])
- Authored a problem discovery report on a critical Federated Learning failure mode: robust aggregation filters (Krum, FLAME) silently discarding valid non-IID updates from minority institutions in cross-institutional fraud detection
- Identified an unaddressed gap in FL security literature as of 2025, citing IEEE Transactions on Big Data and JPMorgan's Project Aikya

= Skills
*Languages / Infra:* Python, SQL, TypeScript, Bash, C++, Git, Docker, FastAPI, React, PostgreSQL, SQLite \
*ML / Data:* PyTorch, PyTorch Geometric, NAS, Pruning, Quantization (QAT), scikit-learn, XGBoost, LightGBM, NumPy, Pandas, Hugging Face \
*Integrations:* Zoho Books API, TallyPrime (XML/ODBC), OAuth 2.0, Render
