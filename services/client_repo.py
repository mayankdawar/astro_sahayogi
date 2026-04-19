"""ClientRepository: SQLite-based client database with search."""
from __future__ import annotations
import sqlite3
import os
from datetime import datetime
from typing import Optional

from astro_sahayogi.models.client import Client


class ClientRepository:
    def __init__(self, db_path: str = "astro_sahayogi_clients.db"):
        self._db_path = db_path
        self._ensure_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _ensure_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    tob TEXT NOT NULL,
                    city TEXT DEFAULT '',
                    latitude TEXT DEFAULT '',
                    longitude TEXT DEFAULT '',
                    horary TEXT DEFAULT '1',
                    timezone TEXT DEFAULT 'Asia/Kolkata',
                    created_at TEXT DEFAULT ''
                )
            """)
            conn.commit()

    def save(self, client: Client) -> int:
        """Insert a client. Returns the new row id. Raises ValueError on duplicate."""
        existing = self.find_duplicate(client.name, client.dob, client.tob)
        if existing:
            raise ValueError(f"Chart for '{client.name}' already exists.")

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO clients (name, dob, tob, city, latitude, longitude, horary, timezone, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                client.to_tuple(),
            )
            conn.commit()
            return cursor.lastrowid

    def find_duplicate(self, name: str, dob: str, tob: str) -> Optional[Client]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM clients WHERE LOWER(name)=? AND dob=? AND tob=?",
                (name.lower(), dob, tob),
            ).fetchone()
            if row:
                return self._row_to_client(row)
        return None

    def get_all(self) -> list[Client]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM clients ORDER BY id DESC"
            ).fetchall()
            return [self._row_to_client(r) for r in rows]

    def search(self, term: str) -> list[Client]:
        with self._connect() as conn:
            pattern = f"%{term}%"
            rows = conn.execute(
                "SELECT * FROM clients WHERE name LIKE ? OR city LIKE ? OR dob LIKE ? ORDER BY id DESC",
                (pattern, pattern, pattern),
            ).fetchall()
            return [self._row_to_client(r) for r in rows]

    def get_by_id(self, client_id: int) -> Optional[Client]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
            if row:
                return self._row_to_client(row)
        return None

    def delete(self, client_id: int):
        with self._connect() as conn:
            conn.execute("DELETE FROM clients WHERE id=?", (client_id,))
            conn.commit()

    def import_from_csv(self, csv_path: str) -> int:
        """Import clients from the old CSV format. Returns count imported."""
        import csv
        if not os.path.exists(csv_path):
            return 0
        count = 0
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                c = Client(
                    name=row.get("Name", ""),
                    dob=row.get("DOB", ""),
                    tob=row.get("Time", ""),
                    city=row.get("City", ""),
                    latitude=row.get("Latitude", ""),
                    longitude=row.get("Longitude", ""),
                    horary=row.get("Horary", "1"),
                    timezone=row.get("Timezone", "Asia/Kolkata"),
                    created_at=row.get("Saved On", ""),
                )
                try:
                    self.save(c)
                    count += 1
                except ValueError:
                    pass
        return count

    @staticmethod
    def _row_to_client(row: tuple) -> Client:
        return Client(
            id=row[0], name=row[1], dob=row[2], tob=row[3],
            city=row[4], latitude=row[5], longitude=row[6],
            horary=row[7], timezone=row[8],
            created_at=row[9] if len(row) > 9 else None,
        )
