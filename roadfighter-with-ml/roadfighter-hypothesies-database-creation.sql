
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: hypothesies
DROP TABLE IF EXISTS hypothesies;

CREATE TABLE hypothesies (
    id                        INTEGER       PRIMARY KEY AUTOINCREMENT,
    parent_id                               DEFAULT (0),
    keys_history              BLOB,
    hypothesis                BLOB,
    evaluations               TEXT,
    average_evaluation        DOUBLE (8, 2),
    passive_objects           BLOB,
    passive_objects_processed BLOB
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
