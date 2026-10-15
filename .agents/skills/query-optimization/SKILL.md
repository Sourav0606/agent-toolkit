---
name: query-optimization
description: Diagnoses and resolves database performance bottlenecks, slow queries, missing indexes, and N+1 patterns. Use when tuning SQL queries, analyzing EXPLAIN plans, or configuring connection pools.
---

# Database Query Optimization & Indexing

A technical manual for analyzing query performance, designing optimal indexes, and eliminating N+1 queries in production.

---

## 1. Query Plan Analysis with `EXPLAIN (ANALYZE, BUFFERS)`

Always inspect the actual execution plan, not assumptions:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE status = 'pending' AND created_at > NOW() - INTERVAL '7 days';
```

### Key Red Flags in Query Plans
1. **`Seq Scan on <table>` (Sequential Scan)**: Scans every row in the table. On large tables ($>10,000$ rows), this usually means a missing index.
2. **`Rows Removed by Filter: <large number>`**: The database had to read many rows only to discard them. An index covering the filter conditions is needed.
3. **`Buffers: shared read=<large>`**: Reading from disk instead of memory (cache misses).
4. **`Sort Method: external merge Disk`**: Sorting exceeded `work_mem` and spilled to disk. Increase `work_mem` for the query or optimize sorting with an index.

---

## 2. Index Design Rules

### A. The B-Tree Ordering Rule (Equality First, Range Second)
When creating composite indexes for queries with multiple `WHERE` or `ORDER BY` clauses:

```sql
-- Query: WHERE status = 'active' AND created_at >= '2026-01-01' ORDER BY created_at DESC
-- Column order: Equality column (status) FIRST, Range/Order column (created_at) SECOND
CREATE INDEX idx_orders_status_created ON orders (status, created_at DESC);
```

### B. Partial Indexes for Low-Cardinality Filters
If you frequently query a small subset of rows (e.g. unpaid orders or active jobs), index only that subset to save space and write overhead:

```sql
-- Indexes only unfulfilled orders (typically <5% of table)
CREATE INDEX idx_orders_unfulfilled ON orders (created_at) WHERE status = 'unfulfilled';
```

### C. Covering Indexes (Index-Only Scans)
Use `INCLUDE` to satisfy read queries directly from the index without reading table heap blocks:

```sql
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (full_name, avatar_url);
```

---

## 3. Eliminating N+1 Query Patterns

### The Anti-Pattern
Looping through records and executing one query per child record ($N$ queries + $1$ parent query):

```python
# BAD: 100 posts = 101 database queries
posts = db.query(Post).limit(100).all()
for post in posts:
    comments = db.query(Comment).filter(Comment.post_id == post.id).all()
```

### The Fix: Eager Loading / Batching
Fetch all child entities in a single batch query:

```python
# GOOD: Exactly 2 queries regardless of count
posts = db.query(Post).options(joinedload(Post.comments)).limit(100).all()

# Or manual batching:
post_ids = [p.id for p in posts]
comments = db.query(Comment).filter(Comment.post_id.in_(post_ids)).all()
```

---

## 4. Connection Pool Sizing Formula

Over-allocating connections degrades database throughput via CPU context switching and disk thrashing.

$$\text{Max Connections} = ((\text{Core Count} \times 2) + \text{Effective Spindle Count})$$

- On modern SSD cloud instances (e.g. AWS RDS), a small pool (10–30 connections per worker process) consistently outperforms a 200-connection pool.
- Use a connection proxy (PgBouncer, Prisma Accelerate) for serverless environments.
