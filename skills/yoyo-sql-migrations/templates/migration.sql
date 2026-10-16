-- <what this migration changes and why>
-- Keep it additive and backward-compatible when possible. Put destructive
-- changes (DROP COLUMN/TABLE) in a separate, later migration.

ALTER TABLE <table>
    ADD COLUMN <column> <TYPE> NOT NULL DEFAULT <default>;

CREATE INDEX idx_<table>_<column> ON <table> (<column>);

-- Backfill if needed:
-- UPDATE <table> SET <column> = ... WHERE <column> IS NULL;

-- Seed a lookup/catalog table idempotently:
-- INSERT INTO <lookup_table> (code, label) VALUES
--     ('<CODE>', '<Label>')
-- ON CONFLICT (code) DO NOTHING;
