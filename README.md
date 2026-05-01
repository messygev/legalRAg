# legalRAg

MVP+ Skeleton für **Legal RAG Bescheid-Kompass**.

## Deployment mit Docker

```bash
docker compose up --build
```

Danach:
- API/UI: `http://localhost:8000`
- Health: `http://localhost:8000/health`
- Qdrant: `http://localhost:6333`

## Endpunkte
- `GET /health`
- `POST /v1/search`
- `POST /v1/notices/analyze-text`
