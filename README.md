# Project_Commercial-Alfa-BI-Plataform-

# Enterprise B2B Data Platform — Commercial Alfa LTDA

An end-to-end data engineering and analytics platform that transforms raw commercial transactional records into a structured, production-ready PostgreSQL dimensional warehouse. This project implements strict database-level data governance, performance-tuned B-Tree indexing, virtualized analytical views, automated analytics modeling, and a decoupled multi-layer architecture optimized for Business Intelligence consumption.

---

##  Executive Summary & Key Insights
Operational analysis proves that Commercial Alfa LTDA operates exclusively within the high-ticket B2B (Business-to-Business) wholesale market, maintaining a gross revenue baseline of **$2,909,104.12** across 374 major contracts, with a global **Average Ticket of $7,778.35**.

* **Strategic Core:** Out of all global transactions, only three records fell below $200.00 (two in the USA, one in Australia). This refutes any hypothesis of localized market volatility, identifying these anomalies purely as promotional product samples or initial client trial runs.
* **Top Revenue Drivers:** The portfolio is heavily anchored by *Tea Tree Moisturizer* ($260,905.44) and *Hydrating Face Serum* ($250,323.33). Low-performing lines like *Charcoal Face Wash* ($102,733.42) occupy the baseline.
* **Key Account Concentration:** A highly concentrated client base was isolated via structural monetization mapping, identifying top-tier global revenue nodes such as *Olivia D'Souza* (UK/USA) and *Ananya Gupta* (New Zealand/Australia), who combine for over $445,000.00 in gross revenue.

---

## System Architecture & Data Layers
The platform rejects monolithic processing, enforcing a clean decoupling of concerns across a modern multi-layer pipeline:

```text
[Raw Layer]           [Processing Layer]          [Storage Layer]          [Semantic Layer]         [Presentation Layer]
 ┌─────────┐            ┌────────────┐             ┌────────────┐             ┌───────────┐             ┌──────────────┐
 │   CSV   │ ──(ETL)──> │ Python +   │ ──(Load)──> │ PostgreSQL │ ──(Views)──> │ SQL Views │ ──(Fetch)──>│   Power BI   │
 │ Source  │            │ psycopg2   │             │ Star Schema│             │  & KPIs   │             │  Dashboards  │
 └─────────┘            └────────────┘             └────────────┘             └───────────┘             └──────────────┘
