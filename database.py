"""
Database Layer for Crop Yield Prediction Application
Handles SQLite database persistence, historical logs, analytics aggregation, and CSV exports.
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crop_yield.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed sample farmer records if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT,
        state TEXT,
        farm_size_ha REAL DEFAULT 1.0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        user_id INTEGER,
        farmer_name TEXT,
        state TEXT NOT NULL,
        crop TEXT NOT NULL,
        season TEXT NOT NULL,
        soil_type TEXT NOT NULL,
        area_ha REAL NOT NULL,
        rainfall_mm REAL NOT NULL,
        temp_c REAL NOT NULL,
        fertilizer_kg REAL NOT NULL,
        pesticide_kg REAL NOT NULL,
        predicted_yield_t_ha REAL NOT NULL,
        total_production_tonnes REAL NOT NULL,
        yield_status TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # Check if user_id column exists in predictions (migration for existing db)
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [col[1] for col in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE predictions ADD COLUMN user_id INTEGER")
    conn.commit()

    # Seed sample records if table is brand new
    cursor.execute("SELECT COUNT(*) FROM predictions")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_records = [
            (
                "2026-09-15 10:30:00",
                "Ramesh Kumar",
                "Punjab",
                "Wheat",
                "Rabi",
                "Alluvial",
                2.5,
                480.0,
                19.5,
                130.0,
                1.4,
                3.85,
                9.63,
                "Optimal / High Yield",
                "Ludhiana district farm - balanced basal NPK application"
            ),
            (
                "2026-09-16 14:15:00",
                "Gurpreet Singh",
                "West Bengal",
                "Rice",
                "Kharif",
                "Clayey",
                3.0,
                1450.0,
                29.0,
                145.0,
                2.1,
                3.95,
                11.85,
                "Optimal / High Yield",
                "Burdwan fertile basin - canal irrigated"
            ),
            (
                "2026-09-17 09:45:00",
                "Suresh Patil",
                "Maharashtra",
                "Cotton",
                "Kharif",
                "Black",
                4.0,
                720.0,
                28.5,
                140.0,
                2.8,
                1.82,
                7.28,
                "Good / Normal Yield",
                "Vidarbha black regur soil with drip irrigation"
            ),
            (
                "2026-09-18 11:20:00",
                "Venkatesh Rao",
                "Karnataka",
                "Maize",
                "Kharif",
                "Red",
                1.8,
                780.0,
                26.0,
                120.0,
                1.7,
                3.42,
                6.16,
                "Good / Normal Yield",
                "Davanagere district - ridge & furrow sowing"
            ),
            (
                "2026-09-18 16:05:00",
                "Mahesh Verma",
                "Uttar Pradesh",
                "Sugarcane",
                "Whole Year",
                "Alluvial",
                5.0,
                1350.0,
                27.5,
                230.0,
                3.2,
                74.5,
                372.5,
                "Optimal / High Yield",
                "Muzaffarnagar tract - high biomass variety"
            )
        ]

        cursor.executemany("""
        INSERT INTO predictions (
            created_at, farmer_name, state, crop, season, soil_type,
            area_ha, rainfall_mm, temp_c, fertilizer_kg, pesticide_kg,
            predicted_yield_t_ha, total_production_tonnes, yield_status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_records)
        conn.commit()

    conn.close()


def create_user(name, email, password_hash, phone=None, state=None, farm_size_ha=1.0):
    """Register a new user into SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO users (created_at, name, email, password_hash, phone, state, farm_size_ha)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        now_str,
        name.strip(),
        email.strip().lower(),
        password_hash,
        phone.strip() if phone else None,
        state.strip() if state else None,
        float(farm_size_ha or 1.0)
    ))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email):
    """Retrieve user dictionary by email."""
    if not email:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Retrieve user dictionary by user_id."""
    if not user_id:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def save_prediction(data, user_id=None):
    """Insert a new prediction record into SQLite with optional user_id."""
    conn = get_connection()
    cursor = conn.cursor()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO predictions (
        created_at, user_id, farmer_name, state, crop, season, soil_type,
        area_ha, rainfall_mm, temp_c, fertilizer_kg, pesticide_kg,
        predicted_yield_t_ha, total_production_tonnes, yield_status, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_str,
        user_id,
        data.get("farmer_name") or "Anonymous Farmer",
        data["state"],
        data["crop"],
        data["season"],
        data["soil_type"],
        float(data["area_ha"]),
        float(data["rainfall_mm"]),
        float(data["temp_c"]),
        float(data["fertilizer_kg"]),
        float(data["pesticide_kg"]),
        float(data["predicted_yield_t_ha"]),
        float(data["total_production_tonnes"]),
        data["yield_status"],
        data.get("notes") or ""
    ))

    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inserted_id


def get_history(limit=50, crop_filter=None, search_query=None, user_id=None):
    """Fetch prediction logs with optional crop filtering, search, and user filtering."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM predictions WHERE 1=1"
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    if crop_filter and crop_filter != "all":
        query += " AND crop = ?"
        params.append(crop_filter)

    if search_query:
        query += " AND (farmer_name LIKE ? OR state LIKE ? OR notes LIKE ?)"
        like_str = f"%{search_query}%"
        params.extend([like_str, like_str, like_str])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def delete_prediction(pred_id):
    """Delete a prediction by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    conn.commit()
    conn.close()


def get_stats():
    """Aggregate statistics for Chart.js dashboards."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total counts and averages
    cursor.execute("SELECT COUNT(*), AVG(predicted_yield_t_ha), MAX(predicted_yield_t_ha) FROM predictions")
    total_count, avg_yield, max_yield = cursor.fetchone()

    total_count = total_count or 0
    avg_yield = round(avg_yield, 2) if avg_yield else 0.0
    max_yield = round(max_yield, 2) if max_yield else 0.0

    # Crop frequency & average yield per crop
    cursor.execute("""
    SELECT crop, COUNT(*) as cnt, AVG(predicted_yield_t_ha) as avg_y
    FROM predictions
    GROUP BY crop
    ORDER BY cnt DESC
    """)
    crop_stats = [{"crop": row[0], "count": row[1], "avg_yield": round(row[2], 2)} for row in cursor.fetchall()]

    # Soil distribution
    cursor.execute("""
    SELECT soil_type, COUNT(*) as cnt
    FROM predictions
    GROUP BY soil_type
    ORDER BY cnt DESC
    """)
    soil_stats = [{"soil": row[0], "count": row[1]} for row in cursor.fetchall()]

    # Rainfall vs Yield scatter points (recent 40 entries)
    cursor.execute("""
    SELECT rainfall_mm, predicted_yield_t_ha, crop
    FROM predictions
    ORDER BY id DESC
    LIMIT 40
    """)
    scatter_data = [{"x": round(row[0], 1), "y": round(row[1], 2), "crop": row[2]} for row in cursor.fetchall()]

    # Top crop
    top_crop = crop_stats[0]["crop"] if crop_stats else "N/A"

    conn.close()

    return {
        "total_predictions": total_count,
        "avg_yield": avg_yield,
        "max_yield": max_yield,
        "top_crop": top_crop,
        "crop_stats": crop_stats,
        "soil_stats": soil_stats,
        "scatter_data": scatter_data
    }


def get_all_for_csv():
    """Retrieve all records for CSV download."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return columns, rows
