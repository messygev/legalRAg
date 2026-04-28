CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS source_registry (
  source_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source_type TEXT CHECK (source_type IN ('official','api','mirror','metadata','dev')),
  base_url TEXT NOT NULL,
  authority_rank INT NOT NULL,
  is_authoritative BOOLEAN DEFAULT FALSE,
  update_frequency TEXT,
  enabled BOOLEAN DEFAULT TRUE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS laws (
  law_id TEXT PRIMARY KEY,
  short_title TEXT NOT NULL,
  full_title TEXT,
  alternative_title TEXT,
  eli_uri TEXT UNIQUE,
  celex_id TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS law_versions (
  version_id TEXT PRIMARY KEY,
  law_id TEXT REFERENCES laws(law_id),
  source_id TEXT REFERENCES source_registry(source_id),
  valid_from DATE NOT NULL,
  valid_to DATE,
  document_hash TEXT NOT NULL,
  status TEXT CHECK (status IN ('draft','active','superseded','quarantined')) DEFAULT 'draft',
  imported_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS norms (
  norm_id TEXT PRIMARY KEY,
  version_id TEXT REFERENCES law_versions(version_id),
  law_abbr TEXT,
  norm_label TEXT NOT NULL,
  title TEXT,
  source_eid TEXT,
  UNIQUE(version_id, norm_label, source_eid)
);

CREATE TABLE IF NOT EXISTS norm_chunks (
  chunk_id TEXT PRIMARY KEY,
  norm_id TEXT REFERENCES norms(norm_id),
  version_id TEXT REFERENCES law_versions(version_id),
  law_abbr TEXT,
  norm_label TEXT,
  paragraph_path TEXT,
  text TEXT NOT NULL,
  context_text TEXT NOT NULL,
  token_count INT CHECK (token_count BETWEEN 20 AND 900),
  chunk_hash TEXT UNIQUE NOT NULL,
  eli_uri TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  tsv tsvector GENERATED ALWAYS AS (
    to_tsvector('german', coalesce(text,'') || ' ' || coalesce(context_text,''))
  ) STORED,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_norm_chunks_tsv ON norm_chunks USING GIN(tsv);
CREATE INDEX IF NOT EXISTS idx_norm_chunks_norm_label ON norm_chunks(norm_label);
CREATE INDEX IF NOT EXISTS idx_norm_chunks_law_abbr ON norm_chunks(law_abbr);
CREATE INDEX IF NOT EXISTS idx_law_versions_law_validity ON law_versions(law_id, valid_from, valid_to);

CREATE TABLE IF NOT EXISTS retrieval_logs (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query TEXT NOT NULL,
  effective_date DATE,
  extracted_norm_refs JSONB,
  top_chunk_ids TEXT[],
  retrieval_trace JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS answer_audits (
  audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  retrieval_log_id UUID REFERENCES retrieval_logs(log_id),
  query TEXT NOT NULL,
  answer TEXT,
  cited_chunk_ids TEXT[] NOT NULL,
  validation_status TEXT CHECK (validation_status IN ('passed','failed','abstained','blocked')),
  failure_reason TEXT,
  model_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS notices (
  notice_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id_hash TEXT,
  document_hash TEXT NOT NULL,
  document_type TEXT,
  authority TEXT,
  file_number TEXT,
  notice_date DATE,
  received_date DATE,
  status TEXT CHECK (status IN ('uploaded','extracted','analyzed','failed','deleted')) DEFAULT 'uploaded',
  pii_detected BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO source_registry
(source_id, name, source_type, base_url, authority_rank, is_authoritative, update_frequency, enabled, notes)
VALUES
('ris_api_preview', 'RIS API / Rechtsinformationen des Bundes', 'official', 'https://testphase.rechtsinformationen.bund.de/', 1, TRUE, 'daily', TRUE, 'Preview API; Aktivierung nur nach Quality Gate'),
('gii_official', 'Gesetze im Internet', 'official', 'https://www.gesetze-im-internet.de/', 2, TRUE, 'daily', TRUE, 'Fallback und Pflichtvergleich')
ON CONFLICT (source_id) DO NOTHING;
