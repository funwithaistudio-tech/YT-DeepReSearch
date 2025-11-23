-- Database Schema for YT-DeepReSearch
-- This file documents the required database schema for the topics table

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    style VARCHAR(50) DEFAULT 'educational',
    language VARCHAR(10) DEFAULT 'en',
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    last_run_at TIMESTAMP,
    last_error TEXT,
    youtube_video_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX idx_topics_status ON topics(status);
CREATE INDEX idx_topics_priority ON topics(priority DESC);
CREATE INDEX idx_topics_status_priority ON topics(status, priority DESC, id ASC);

-- Sample data for testing
INSERT INTO topics (topic, style, language, priority) VALUES
    ('Quantum Computing: The Future of Technology', 'educational', 'en', 10),
    ('The Science Behind Black Holes', 'documentary', 'en', 9),
    ('Artificial Intelligence and Machine Learning', 'educational', 'en', 8),
    ('Climate Change: Understanding the Science', 'educational', 'en', 7),
    ('The History of Space Exploration', 'documentary', 'en', 6);

-- Notes:
-- - status values: 'pending', 'in_progress', 'completed', 'failed'
-- - style values: 'educational', 'documentary', 'entertaining'
-- - language: ISO 639-1 language codes (en, hi, ta, te, kn, ml, etc.)
-- - priority: higher number = higher priority
