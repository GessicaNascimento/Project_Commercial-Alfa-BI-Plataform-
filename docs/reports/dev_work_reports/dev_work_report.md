# Development Work Report: Data Infrastructure & Pipeline Engineering

## 1. Executive Summary
This report documents the architectural transition of the Commercial Alfa LTDA data pipeline from a localized prototyping environment (SQLite) to an enterprise-grade production relational database management system (PostgreSQL 14). The pipeline enforces strict data integrity constraints, implements performance optimization structures, and provides a semantic view layer designed for seamless downstream consumption by Business Intelligence platforms.

## 2. Pipeline Architecture & Data Flow
The data processing pipeline is structured across decoupled operational layers to ensure maintainability and scalability:

* **Raw Layer:** Ingestion of unrefined transactional data from the flat file (`cosmetics_sales_data.csv`).
* **Processing Layer:** Python ETL engine utilizing the `psycopg2` driver. The engine maps strings, standardizes dates, manages isolation levels, and executes atomic transactions using database-side cursors.
* **Storage Layer (PostgreSQL):** A Star Schema (Dimensional Model) consisting of three dimension tables (`dim_clientes`, `dim_produtos`, `dim_tempo`) and one central fact table (`fato_vendas`).
* **Semantic Layer (SQL Views):** Virtualized abstraction layer that pre-aggregates business logic, mitigating query performance degradation on the client side.

## 3. Database Schema & Integrity Constraints
Data governance is enforced directly at the database engine level via Data Definition Language (DDL) constraints:

* **Entity Integrity:** Primary keys are declared on all tables. Dimensions utilize auto-incrementing `SERIAL` sequences to guarantee unique surrogate keys.
* **Referential Integrity:** Foreign keys on `fato_vendas` map directly to respective dimensions with `ON DELETE CASCADE` triggers to prevent orphaned records.
* **Domain Integrity:** Strict type casting (`NUMERIC(12,2)` for financial fields, `DATE` for timestamps).
* **Business Rules Enforcement:** Database-level `CHECK` constraints prevent non-positive values on operational fields:
  * `CHECK (quantidade > 0)`
  * `CHECK (valor_total >= 0)`

## 4. Performance Tuning & Optimization
To optimize read operations and eliminate high-cost Sequential Scans (Table Scans) during complex relational joins, B-Tree indices were implemented on high-cardinality foreign keys and frequently filtered predicates:
* `idx_fato_data` ON `fato_vendas(data_venda)`
* `idx_fato_cliente` ON `fato_vendas(id_cliente)`
* `idx_fato_produto` ON `fato_vendas(id_produto)`
* `idx_clientes_pais` ON `dim_clientes(pais_cliente)`
