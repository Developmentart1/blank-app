from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Modelo Vivo API", version="1.0.0", openapi_url="/api/openapi.json")

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Stubs mínimos según OpenAPI
@app.get("/api/plan/ingresos")
def get_plan_ingresos():
    return []

@app.post("/api/plan/ingresos")
def post_plan_ingresos(payload: dict):
    return JSONResponse(status_code=202, content={"received": True})

@app.get("/api/plan/egresos")
def get_plan_egresos():
    return []

@app.post("/api/plan/egresos")
def post_plan_egresos(payload: dict):
    return JSONResponse(status_code=202, content={"received": True})

@app.get("/api/real/ingresos")
def get_real_ingresos():
    return []

@app.post("/api/real/ingresos")
def post_real_ingresos(payload: dict):
    return JSONResponse(status_code=202, content={"received": True})

@app.get("/api/real/egresos")
def get_real_egresos():
    return []

@app.post("/api/real/egresos")
def post_real_egresos(payload: dict):
    return JSONResponse(status_code=202, content={"received": True})

@app.get("/api/metrics/kpis")
def get_metrics_kpis(period: str | None = None, group_by: str | None = None):
    return {"period": period, "group_by": group_by, "data": []}

@app.get("/api/variance")
def get_variance(dim: str | None = None):
    return {"dim": dim, "data": []}

@app.get("/api/alerts")
def get_alerts():
    return []

@app.post("/api/alerts")
def post_alerts(payload: dict):
    return JSONResponse(status_code=202, content={"received": True})
