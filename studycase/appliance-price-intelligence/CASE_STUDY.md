# Case Study: Appliance Retail Price Intelligence Platform

> A portfolio project for a **Data Engineer** role. It builds an end-to-end ELT
> platform that collects product and price data from several appliance retailers,
> processes it with **PySpark** on **GCP**, models it in **BigQuery**, and serves
> insights to business stakeholders.

---

## 1. Business context

**Company (fictional):** *ApplianceIQ*, a market-intelligence startup that sells
competitive pricing data to appliance brands and retailers.

**Stakeholders**

| Stakeholder | What they need |
|---|---|
| Head of Pricing | "Which retailers undercut the brand's MSRP, by how much, and since when?" |
| Category Manager | "How many SKUs does each retailer carry per category, and which are new or discontinued this week?" |
| Data Analyst | Clean, documented, trustworthy tables they can query with SQL without asking engineering. |
| CTO | A pipeline that runs daily without babysitting, costs little, and alerts when something breaks. |

**Problem today:** scraped data lands as loose JSON files on a laptop
(`products_20261006_094348.json`, …). Prices are strings (`"$2,495.00"`), SKUs
carry prefixes (`"SKU: AC-FUSION-19"`), each retailer has a different schema, and
nobody can answer "what was the price last Tuesday?" because files get overwritten.

**Goal:** a daily, automated, tested pipeline that turns raw retailer pages into a
dimensional model with full price history, plus a short insight report.

---

## 2. How this project maps to the job requirements

| Requirement | Where it is demonstrated |
|---|---|
| Strong SQL & relational databases | Star schema in BigQuery, SCD Type 2 price history, window functions, data-quality SQL tests, a Postgres source for reference data |
| Building & maintaining ETL/ELT pipelines | Extract → GCS (bronze) → PySpark (silver) → BigQuery (gold), idempotent daily runs, backfills, orchestration with Airflow |
| Python & PySpark | Scrapers + ingestion in Python; cleaning, deduplication, and SKU matching in PySpark |
| Cloud platform + data warehouse | GCP: Cloud Storage, Dataproc Serverless (or local Spark), BigQuery, Cloud Composer / Airflow in Docker, Secret Manager |
| Maintaining pipelines | Logging, retries, data-quality gates, alerting, CI with tests, runbook |
| English communication & presenting insights | README written for engineers, a 1-page insight memo for business, a 5-slide deck, and a recorded 5-minute walkthrough |

> The cloud is interchangeable. If the target company uses AWS, swap
> GCS → S3, Dataproc → EMR Serverless / Glue, BigQuery → Redshift / Snowflake.
> Mention this in your README; it shows you understand the concepts, not just one vendor.

---

## 3. Data sources

| # | Source | Type | Notes |
|---|---|---|---|
| S1 | Retailer A — Futuro Futuro | Web scrape (existing `scrape/futuro-futuro`) | Range hoods & accessories, price as string |
| S2 | Retailer B — Unique Appliances | Web scrape (existing `scrape/unique-appliances`) | Different field names |
| S3 | Retailer C — White Dove | Web scrape (existing `scrape/white-dove`) | Different field names |
| S4 | Brand MSRP list | CSV dropped weekly into GCS (create a mock file of ~200 SKUs) | Reference price to compare against |
| S5 | Product master | **Postgres** table (Cloud SQL or local Docker) | Canonical brand, model number, category — simulates an internal OLTP system |
| S6 | FX rates | Public REST API (e.g. frankfurter.app) | Normalise CAD/USD prices |

Run the scrapers daily for at least **2–3 weeks** before you write the insight
report, so you have real price history. If you need more volume for Spark to be
meaningful, generate synthetic history with a script (clearly labelled as synthetic).

---

## 4. Target architecture

```
 ┌────────────┐   ┌───────────────────────┐   ┌──────────────────────┐   ┌───────────────────────┐
 │ Scrapers   │   │  GCS  raw/  (bronze)  │   │ PySpark  (silver)    │   │ BigQuery  (gold)      │
 │ S1 S2 S3   │──▶│  json, partitioned by │──▶│ clean, type, dedupe, │──▶│ staging → dims/facts  │
 │ MSRP CSV   │   │  source/ingest_date   │   │ SKU match, parquet   │   │ → marts (SQL / dbt)   │
 │ Postgres   │   └───────────────────────┘   └──────────────────────┘   └───────────┬───────────┘
 │ FX API     │                                                                      │
 └────────────┘                                                                      ▼
        ▲                     Orchestrated by Airflow (Composer or Docker)    Looker Studio dashboard
        └──────────────────── data-quality checks · alerts · logs ──────────  + insight memo
```

**Layer contract**

| Layer | Storage | Format | Rule |
|---|---|---|---|
| Bronze | `gs://<bucket>/raw/source=<s>/ingest_date=YYYY-MM-DD/` | JSON / CSV as received | Append-only, never modified. Add `_ingested_at`, `_source_file`. |
| Silver | `gs://<bucket>/silver/<entity>/ingest_date=…/` | Parquet | Typed, cleaned, deduplicated, one schema across retailers. |
| Gold | BigQuery dataset `gold` | Tables | Star schema + business marts, partitioned & clustered. |

---

## 5. Project phases, deliverables & acceptance criteria

### Phase 1 — Ingestion (Python)

Refactor the existing scrapers into one package with a common interface.

- `BaseScraper.fetch() -> list[dict]` and one subclass per retailer.
- Upload raw output to GCS bronze with the partitioned path above.
- Extract the Postgres product master incrementally (`updated_at > last_watermark`).
- Pull FX rates from the API.
- Retries with backoff, polite rate limiting, structured logging.

**Done when:** running `python -m ingest --source all --date 2026-11-01` twice
produces the same bronze files (idempotent) and logs row counts per source.

### Phase 2 — Transformation (PySpark)

One Spark job per entity, reading bronze and writing silver.

- Parse price strings → `NUMERIC` (`"$2,495.00"` → `2495.00`), strip `"SKU: "` prefixes.
- Unify the three retailer schemas into one `silver.retailer_listing` schema.
- Deduplicate within a day (latest scrape wins) using a window function.
- Convert currency with the FX table (broadcast join).
- **SKU matching:** map each retailer listing to the product master by normalised
  model number; record unmatched rows in a `silver.unmatched_listing` quarantine table.
- Explicit Spark schemas (no `inferSchema` in production).

**Done when:** jobs run on Dataproc Serverless (or `spark-submit` locally),
are unit-tested with `pytest` + a local SparkSession, and the match rate is reported.

### Phase 3 — Data warehouse modelling (SQL, BigQuery)

Load silver into BigQuery and build the gold model (plain SQL or **dbt**, dbt recommended).

```
dim_product      (product_key, model_number, brand, category, ... )
dim_retailer     (retailer_key, retailer_name, country, url)
dim_date         (date_key, date, week, month, is_weekend)
fct_daily_price  (date_key, product_key, retailer_key, price_usd, msrp_usd,
                  in_stock, discount_pct)          -- partitioned by date, clustered by product_key
dim_product_price_scd2 (product_key, retailer_key, price_usd,
                        valid_from, valid_to, is_current)   -- SCD Type 2 history
```

Business marts:

- `mart_msrp_violations` — listings priced more than 5% under MSRP, with days in violation.
- `mart_assortment_changes` — SKUs new or removed per retailer per week.
- `mart_price_index` — average price vs MSRP per retailer and category per week.

**Done when:** every table has a documented grain, primary key tests pass, and
queries scan only the partitions they need (show bytes processed before/after).

### Phase 4 — Orchestration & reliability

- Airflow DAG: `ingest → spark_silver → load_bq → dbt_run → dbt_test → notify`.
- Daily schedule, `catchup` for backfills, retries, SLA.
- Data-quality gates (dbt tests or Great Expectations): not-null keys, unique
  `(date, product, retailer)`, price > 0, row count within ±30% of the 7-day average,
  freshness < 26 hours. A failed gate stops the publish and sends an alert (Slack or email).
- Secrets in Secret Manager or environment variables, never in git.

**Done when:** you can show a DAG run history, one deliberately failed run caught
by a quality check, and a backfill of 7 days.

### Phase 5 — Engineering hygiene

- Infrastructure as code with **Terraform** (bucket, datasets, service account). Optional but valuable.
- GitHub Actions: lint (`ruff`), unit tests, `dbt compile` on every PR.
- `docker-compose.yml` to run Postgres + Airflow locally.
- Cost note: what one month costs (BigQuery free tier, Dataproc Serverless minutes).

### Phase 6 — Communicating insights (English)

1. **README** (for engineers): problem, architecture diagram, how to run, design decisions & trade-offs.
2. **Insight memo**, 1 page, for the Head of Pricing. Example structure:
   - *Headline:* "Retailer B sold 18% of tracked range hoods below MSRP last month."
   - Three findings with one chart each.
   - Recommendation and next step.
3. **Dashboard** in Looker Studio connected to the marts.
4. **5-minute video** walking through architecture → a pipeline run → the dashboard.

---

## 6. Example SQL questions the warehouse must answer

1. Top 10 products with the largest gap between retailer price and MSRP today.
2. For each retailer, how many days in a row has each SKU been below MSRP? *(gaps-and-islands)*
3. Week-over-week price change per category, using `LAG()`.
4. Which SKUs appeared at a retailer this week but not last week?
5. The price of model X at retailer Y on any past date *(uses the SCD2 table)*.
6. Retailer price index: `AVG(price / msrp)` by retailer and month.

Put these in `sql/analysis/` with the result screenshot. Interviewers love reading them.

---

## 7. Suggested repository layout

```
appliance-price-intelligence/
├── README.md
├── docker-compose.yml
├── terraform/
├── ingest/                 # Python scrapers + loaders
│   ├── scrapers/
│   └── loaders/
├── spark_jobs/             # PySpark bronze → silver
├── dbt/                    # staging, dims, facts, marts, tests
├── dags/                   # Airflow
├── sql/analysis/           # the questions in section 6
├── tests/
├── docs/
│   ├── architecture.png
│   ├── data_dictionary.md
│   ├── runbook.md
│   └── insight_memo.pdf
└── .github/workflows/ci.yml
```

---

## 8. Suggested timeline (part-time, ~6 weeks)

| Week | Focus |
|---|---|
| 1 | Refactor scrapers, GCS bronze, Postgres in Docker, start daily collection |
| 2 | PySpark silver jobs + unit tests |
| 3 | BigQuery load, dbt dims/facts, SCD2 |
| 4 | Marts, data-quality tests, analysis SQL |
| 5 | Airflow DAG, alerts, backfill, CI, Terraform |
| 6 | Dashboard, insight memo, README, video |

Start with a working thin slice (one retailer, end to end) in week 1–2, then widen.
A finished small pipeline is worth more than an unfinished big one.

---

## 9. Talking points for the interview

- **Why ELT instead of ETL?** Raw data is kept in bronze so you can reprocess when
  business rules change; heavy modelling happens in the warehouse, where SQL is cheap and auditable.
- **Why PySpark if the data is small?** The job is written to scale horizontally.
  Show a run on synthetic 10M-row history and compare runtime with pandas.
- **Idempotency:** every run overwrites only its own `ingest_date` partition, so retries and backfills are safe.
- **Data quality:** you quarantine bad rows instead of dropping them silently, and
  you can show the match rate trend.
- **Cost:** partitioning + clustering cut bytes scanned by X%. Show the numbers.
- **What you'd do next:** CDC from Postgres with Datastream/Debezium, streaming price
  alerts with Pub/Sub, ML-based fuzzy SKU matching.

---

## 10. Stretch goals

- Replace the batch Postgres extract with CDC (Debezium → Pub/Sub → BigQuery).
- Add an LLM-based enrichment step that classifies product category from the title,
  validated with a Pydantic schema (you already prototyped this in `local-pipeline/`).
- Publish the same gold layer to Snowflake to show warehouse portability.
- Add data lineage with OpenLineage / Marquez.
