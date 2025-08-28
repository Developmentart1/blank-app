# Sistema Analítico Dinámico (Plan vs Real)

Stack: Postgres, FastAPI, React (Vite), Docker Compose.

## Uso rápido

1. Crear `.env` (ya incluido con defaults).
2. Levantar servicios:

```bash
docker compose --env-file .env up -d --build
```

- API: http://localhost:${API_PORT}/api/health
- Frontend: http://localhost:${FRONTEND_PORT}

## Estructura
- `db/migrations`: Esquema inicial montado a Postgres.
- `api`: FastAPI con endpoints stub.
- `frontend`: React + Vite con pantalla mínima.
- `etl`: espacio para scripts pandas.

## Siguientes pasos
- Implementar capa de acceso a datos y endpoints reales.
- Agregar ETL (pandas) y loaders.
- Crear jobs `recompute_metrics` y `recompute_alerts`.
