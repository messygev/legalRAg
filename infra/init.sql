CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS source_registry (
  source_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source_type TEXT,
  base_url TEXT NOT NULL,
  authority_rank INT NOT NULL,
  is_authoritative BOOLEAN DEFAULT FALSE,
  update_frequency TEXT,
  enabled BOOLEAN DEFAULT TRUE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO source_registry (source_id, name, source_type, base_url, authority_rank, is_authoritative, update_frequency, enabled, notes)
VALUES
('ris_api_preview', 'RIS API / Rechtsinformationen des Bundes', 'official', 'https://testphase.rechtsinformationen.bund.de/', 1, TRUE, 'daily', TRUE, 'Preview API; Aktivierung nur nach Quality Gate'),
('gii_official', 'Gesetze im Internet', 'official', 'https://www.gesetze-im-internet.de/', 2, TRUE, 'daily', TRUE, 'Fallback und Pflichtvergleich')
ON CONFLICT (source_id) DO NOTHING;
