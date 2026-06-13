# Data Architecture Blueprint — Commercial Alfa LTDA

This document outlines the technical infrastructure, data pipeline design, and visualization architecture implemented for the Commercial Alfa LTDA analytics platform. The system is engineered to support structured data ingestion, automated relational processing, database-level schema enforcement, and multi-tier business intelligence deployment.

---

## 1. Pipeline Flow & Layer Segmentation

The platform architecture follows a decoupled, multi-layer data pipeline pattern to separate computing concerns and ensure strict metadata control:

* **Raw Layer (`data/raw/`):** Hosts the immutable source file (`cosmetics_sales_data.csv`). This layer represents the cold, unrefined transactional history.
* **Processing & Transformation Layer (`scripts/`):** Governed by the `etl_postgres.py` script. This Python engine handles stream reading, dynamic type casting, high-performance chunk loading, data cleaning, and establishes binary communication with the database engine via the `psycopg2` adapter.
* **Storage Layer (PostgreSQL Warehouse):** A relational database management system hosting a normalized Star Schema. This layer enforces entity integrity, domain check constraints, and referential integrity with cascading deletions.
* **Semantic & Analytical Layer (SQL Views):** Comprises virtualized pre-aggregations (`v_monthly_revenue`, `v_customer_performance`, `v_product_ranking`) optimized to minimize execution costs during business reporting.
* **Presentation Layer:** Houses the compiled enterprise visualization layouts. Even when handled within a development ecosystem where local desktop rendering is constrained, the repository physically embeds the distribution binaries to ensure downstream deployment readiness.

---

## 2. Infrastructure Component Matrix

| Pipeline Stage | Technology / Asset | Implementation Scope |
| :--- | :--- | :--- |
| Ingestion & ETL | `etl_postgres.py` (Python 3.x) | Type safety, data casting, and atomic transaction control. |
| Database Adapter | psycopg2 | Low-level binary communication with the PostgreSQL engine. |
| Storage Database | PostgreSQL 14+ | Relational data hosting, Star Schema layout, and indexing. |
| Performance Tuning | B-Tree Indexes | Query acceleration on foreign keys and geographical fields. |
| IDE & Client Client | DBeaver Enterprise | Schema management, query execution, and database auditing. |
| Executive Interface | `executive_dashboard.pbix` | Strategic visualization binary containing C-level macro insights. |
| Operational Interface | `operational_dashboard.pbix` | Tactical visualization binary containing day-to-day metrics. |

---

## 3. Transactional Integrity & Fail-Safe Mechanisms

The `etl_postgres.py` engine treats data loading as an atomic block. 
* **Isolation Level:** The pipeline operates under default transactional isolation, ensuring concurrent sessions do not read uncommitted telemetry.
* **Error Handling:** If a single row violates database check constraints (such as a negative price or quantity value), a database-side exception is caught by Python, triggering a complete `rollback` command. This ensures zero data corruption in the production environment.


