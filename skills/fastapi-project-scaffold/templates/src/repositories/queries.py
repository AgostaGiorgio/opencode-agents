from sqlalchemy import text

GET_ITEMS = text("""
SELECT id, name, description, created_at
FROM items
ORDER BY created_at DESC
""")

GET_ITEM = text("""
SELECT id, name, description, created_at
FROM items
WHERE id = :id
""")

NEW_ITEM = text("""
INSERT INTO items (name, description)
VALUES (:name, :description)
RETURNING id, name, description, created_at
""")

UPDATE_ITEM = text("""
UPDATE items
SET name = :name,
    description = :description
WHERE id = :id
RETURNING id, name, description, created_at
""")

DELETE_ITEM = text("""
DELETE FROM items
WHERE id = :id
""")
