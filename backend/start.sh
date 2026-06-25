#!/bin/bash
set -e

echo "[BeanBrew] Running migrations and seeding..."
python -c "
from src.repositories.database import test_connection
from src.migrations.create_tables import Migration
from src.migrations.seeder import Seeder
test_connection()
Migration().create_tables()
Seeder().seed_data()
print('Setup complete!')
"

echo "[BeanBrew] Starting server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
