---
name: db-migration-safety
description: Enforces zero-downtime database migrations and safe schema evolution using the Expand-Contract pattern. Prevents table-locking DDL, unindexed foreign keys, and breaking schema changes in production.
---

# Safe Database Migrations & Zero-Downtime Schema Evolution

A production guide for evolving relational database schemas without downtime, locking production tables, or breaking running application instances.

---

## 1. The Golden Rule: Expand and Contract

Never make a breaking schema change in a single deployment. Every structural change requires multiple phases:

```
Phase 1 (Expand): Add new column/table as nullable or with safe defaults.
Phase 2 (Dual-Write / Migrate): Application writes to both new and old; backfill existing rows.
Phase 3 (Switch Read): Point application reads to the new column/table.
Phase 4 (Contract): Remove old column/table in a subsequent release.
```

---

## 2. PostgreSQL Safe DDL Rules

### A. Lock Timeouts Are Non-Negotiable
Every migration script must set a conservative lock timeout to avoid queuing behind long transactions and starving connection pools:

```sql
SET lock_timeout = '2s';
SET statement_timeout = '30s';
```

### B. Adding Columns Safely
- **PostgreSQL 11+**: `ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT true NOT NULL;` is safe (metadata-only update, no full table rewrite).
- **Older engines**: Add column as nullable first, backfill in batches, then add `NOT NULL` constraint with `NOT VALID`, followed by `VALIDATE CONSTRAINT`.

### C. Creating Indexes Without Locking Reads/Writes
Never run plain `CREATE INDEX` on live tables:

```sql
-- Safe: Does not block concurrent SELECTs, INSERTs, UPDATEs, or DELETEs
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### D. Renaming Columns or Tables
Never run `ALTER TABLE ... RENAME COLUMN ...`. It immediately crashes running application pods executing the old code.
Instead:
1. Add new column.
2. Dual-write in code or database triggers.
3. Backfill data.
4. Deploy code reading from the new column.
5. Drop the old column in the next sprint.

### E. Foreign Key Constraints
Adding a foreign key can lock both tables. Add the constraint without validation first:

```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  NOT VALID;

-- Validate in a separate transaction without table-level lock
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user;
```

---

## 3. Pre-Migration Checklist

- [ ] Lock timeout is explicitly set (`SET lock_timeout = '2s';`).
- [ ] New indexes use `CONCURRENTLY`.
- [ ] Large backfills are batched (e.g. 5,000 rows per batch with pauses) rather than running in one massive transaction.
- [ ] Schema change is backward-compatible with the currently running application version.
- [ ] Down/revert migration script is written and tested.
