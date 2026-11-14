-- Bootstrap PostgreSQL for CKPA (development)
-- Chạy tự động khi container db khởi động lần đầu.
CREATE EXTENSION IF NOT EXISTS vector;         -- pgvector 0.8+
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";   -- uuid_generate_v4()
