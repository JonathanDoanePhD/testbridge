# TestBridge

**Source-grounded semiconductor test planning, instrument simulation, and reproducible retrieval research.**

Author: Jonathan Doane, Ph.D. Independent portfolio project; not affiliated with Cohu, Vishay, or Tektronix.

## Live demo

https://testbridge-research.jonathandoanephd.chatgpt.site

The hosted demo currently requires owner access. This repository is standalone. Follow the local quick start to run the interface independently.

## What works

- A browser workbench accepts engineering questions, retrieves page/section-linked evidence, identifies test families, and asks for clarification when terminology is ambiguous.
- A structured 2N7000 IDSS form validates explicit device, bias, temperature, acceptance limit, compliance, settling, sample count, and logical connections.
- A stateful illustrative SMU simulator produces seeded readings and command traces. Nominal, excessive device leakage, fixture contamination, and compliance faults are supported.
- Plans, Python procedures, and readings can be downloaded.
- A 60-query, 20-group synthetic development benchmark compares keyword overlap, BM25, and BM25 with explicit terminology expansion.
- A Python CLI implements the same retriever and simulator. Tests verify retrieval parity across all 180 query/method combinations.
- An optional OpenAI-compatible model adapter supports experimental evidence-conditioned JSON answers. It is not called by the hosted demo or evaluated by the reported benchmark.

## Quick start

The core Python workflow uses Python 3.10+ and the standard library. The benchmark harness needs Node.js 18+.

```sh
python research/testbridge.py retrieve "How do I determine settling time?"
python research/testbridge.py simulate research/example-plan.json
python research/testbridge.py simulate research/example-plan.json --scenario fixture
python -m unittest discover -s research -v
node research/evaluate.mjs
python -m http.server 8000 --directory dist
```

Open http://localhost:8000 for the workbench. No API key is required. Downloaded Python procedures import `testbridge`; run them from the `research` directory, or set `PYTHONPATH` to that directory.

## A cohesive portfolio workflow

The opening workflow follows one customer scenario from request through clarification, source evidence, structured plan, and simulated result. Short definitions explain the transistor, off-state current, units, and decisions where they first appear. The final result connects directly to an expandable configuration form for custom requests and test settings. Source library, evaluation, and methods are supporting research views. There is no interview-preparation content in the product.

The visual treatment follows the public Cohu site's Arial/Helvetica typography, blue (#0053a1 / #005baa), orange (#ffa700), white surfaces, and restrained square geometry. It uses TestBridge's own identity and indicates that it is an independent prototype. Brand colors and typography were inspected in Cohu's public stylesheets on 8 October 2026.

## Demo walkthrough

1. Analyze the initial off-state leakage request. Its customer acceptance limit is not supplied and will not be invented.
2. Inspect linked IDSS evidence. The source document is Vishay 70226, Rev. F, PDF page 2, with the 2N7000 row visually checked against the original table.
3. Load documented demo conditions. VDS 48 V, VGS 0 V, default ambient 25°C, and the 1 µA maximum come from that selected row. Compliance 100 µA, delay 1 s, and 20 samples are explicitly illustrative user-editable simulation choices.
4. Confirm logical connections, then validate. Physical package pinout and actual instrument configuration are outside this simulator.
5. Run nominal, leaky, fixture, and compliance scenarios. Review output-off shutdown in the command trace.
6. Inspect evaluation failures for the baselines and download all query-level results.

No parameters are silently extracted from natural-language requests. The form is the explicit source of procedure parameters. Editing the request or parameters invalidates any previously validated plan.

## Experiment

**Question:** Does a small explicit terminology map improve evidence retrieval over lexical baselines on synthetic semiconductor-measurement queries?

**Corpus:** Four publisher sources, represented by fourteen human-written editorial paraphrases. This is not full-document RAG over thousands of pages. Original PDFs and publisher HTML are not redistributed. Evidence IDs link to page or section locators; the source is displayed alongside each passage.

**Baselines:** Keyword overlap ranks by query-token matches. BM25 ranks titles and summary bodies using k1=1.2 and b=0.75. Expanded retrieval adds editorial tags and an 8-point boost for matching domain aliases. It is lexical retrieval, not a learned model, embedding search, or neural reranking. Tags and boosts are both changed, so this comparison does not isolate their individual contributions.

**Metrics:** Recall@3 is the fraction of queries with labeled evidence among the top three. MRR@3 is reciprocal rank of the first labeled record, or zero when absent. Each query currently has one author-labeled relevant record; alternative acceptable passages have not been exhaustively judged.

| Method | Recall@3 | MRR@3 |
| --- | --- | --- |
| Keyword overlap | 86.7% | 0.772 |
| BM25 | 91.7% | 0.836 |
| BM25 + terminology expansion | 100.0% | 0.992 |

Paired Recall@3 difference versus BM25: +8.3 percentage points. The percentile 95% interval is +3.3 to +15.0 points using 5,000 seeded cluster-bootstrap resamples over twenty three-query groups. Resampling paraphrases together accounts for within-group dependence; related groups may remain dependent.

**Interpretation:** These are development results on a small, author-created corpus and query set. The same author designed the map, questions, and labels. A 100% score does not establish generalization, production quality, answer factuality, or statistical certainty about unseen engineer requests. The confidence interval only describes resampling variation within this constructed dataset.

**Next experiment:** Freeze the implementation, collect unseen engineer-authored requests, and obtain independent multi-relevance judgments. Add hard negatives, true unknowns, customer aliases, conflicting document revisions, and multiple devices. Measure abstention quality and claim-level citation support separately from retrieval. Compare workflow completion time and correctness in a randomized, counterbalanced study. Do not claim weeks-to-hours savings without observing them.

## Simulation model

The generated current is an illustrative base current scaled by bias, plus a decaying transient, seeded uniform noise, and an optional fixture term. The mean is displayed for inspection; PASS requires every sampled current to meet the chosen limit. A compliance event aborts acquisition and reports INVALID rather than a valid measurement. Shutdown occurs in `finally` in Python and JavaScript.

These outputs are synthetic, not measured semiconductor data or a calibrated device model. A 1 s settling delay may be inadequate on real hardware. No instrument driver or hardware connection exists. Custom limits/biases do not imply datasheet conformance. Only the selected 48 V / 0 V / 25°C / 1 µA condition is labeled a match to the source comparison.

## Optional model adapter

Set `TESTBRIDGE_API_KEY`, `TESTBRIDGE_MODEL`, and optionally `TESTBRIDGE_API_BASE` in your environment, then run:

```sh
python research/testbridge.py answer "Why does fixture leakage matter?"
```

The default endpoint is OpenAI-compatible `/v1/chat/completions`. The adapter sends only retrieved editorial summaries and the question. Output must contain an answer, evidence IDs, and a clarification flag. Schema and ID membership checks do not verify semantic support. No model output is passed to the simulator. API access and usage costs are the user's responsibility; no credentials are embedded in the project.

## Full-document ingestion extension

`research/ingest_pdf.py` optionally extracts a local PDF into page-linked word windows, records its SHA-256, and writes a separate local JSON corpus. Install `pypdf` to use it. Inspect tables and OCR before relying on extraction. This utility is not connected to the hosted curated corpus and was not used for the reported results. Review publisher permissions before distributing extracted text.

## Files

- `dist/`: deployed browser interface, pure JavaScript engine, corpus, benchmark, and measured results.
- `research/testbridge.py`: Python CLI, BM25, validation, simulator, optional model adapter.
- `research/evaluate.mjs`: deterministic evaluation and operational checks.
- `research/test_testbridge.py`: Python tests and JS/Python retrieval parity checks.
- `research/build_corpus.py`: reproducible editorial corpus construction.
- `research/create_benchmark.py`: synthetic queries and grouped labels.
- `research/ingest_pdf.py`: optional local PDF extraction utility.

Browser WebMCP tools are feature-detected for request analysis and validated-plan read-back. Unsupported browsers use the normal interface. Live WebMCP/browser validation was unavailable in the build environment; engine and Python checks were completed.

## Sources

- Vishay Siliconix, 2N7000/2N7002 datasheet, document 70226, Rev. F, 16 July 2001: https://www.vishay.com/docs/70226/70226.pdf
- Keithley, Optimizing Low Current Measurements with the 4200A-SCS: https://www.tek.com/en/documents/application-note/optimizing-low-current-measurements-4200a-scs-parameter-analyzer
- Keithley, Low Level Measurements Handbook, 7th edition: https://www.tek.com/en/documents/product-article/keithley-low-level-measurements-handbook---7th-edition
- Keithley, Breakdown and Leakage Current Measurements, 1KW-61601-0: https://download.tek.com/document/1KW-61601-0_Breakdown-Leakage_Current_2470_Application_Note_080619.pdf

Retrieved 8 October 2026. Publisher copyrights remain with their owners. Source code is released under MIT; original publisher materials are excluded.
