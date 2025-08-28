CREATE TABLE IF NOT EXISTS dim_time (
  date DATE PRIMARY KEY,
  year INT,
  quarter INT,
  month INT,
  week INT,
  day INT
);

CREATE TABLE IF NOT EXISTS dim_unidad (
  unidad_id TEXT PRIMARY KEY,
  torre TEXT,
  nivel TEXT,
  tipologia TEXT,
  m2 NUMERIC,
  precio_lista NUMERIC,
  estatus TEXT
);

CREATE TABLE IF NOT EXISTS fact_plan_ingresos (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL REFERENCES dim_time(date),
  unidad_id TEXT REFERENCES dim_unidad(unidad_id),
  concepto TEXT,
  monto_plan NUMERIC NOT NULL,
  escenario TEXT,
  version_id TEXT NOT NULL,
  valid_from TIMESTAMPTZ DEFAULT NOW(),
  valid_to TIMESTAMPTZ,
  is_current BOOLEAN DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS fact_plan_ingresos_unidad_date_idx ON fact_plan_ingresos (unidad_id, date) WHERE is_current;

CREATE TABLE IF NOT EXISTS fact_plan_egresos (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL REFERENCES dim_time(date),
  categoria TEXT NOT NULL,
  subcategoria TEXT,
  concepto TEXT,
  monto_plan NUMERIC NOT NULL,
  escenario TEXT,
  version_id TEXT NOT NULL,
  valid_from TIMESTAMPTZ DEFAULT NOW(),
  valid_to TIMESTAMPTZ,
  is_current BOOLEAN DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS fact_plan_egresos_cat_date_idx ON fact_plan_egresos (categoria, date) WHERE is_current;

CREATE TABLE IF NOT EXISTS fact_real_ingresos (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL REFERENCES dim_time(date),
  unidad_id TEXT REFERENCES dim_unidad(unidad_id),
  recibo_id TEXT NOT NULL UNIQUE,
  monto_real NUMERIC NOT NULL,
  medio_pago TEXT
);
CREATE INDEX IF NOT EXISTS fact_real_ingresos_unidad_date_idx ON fact_real_ingresos (unidad_id, date);

CREATE TABLE IF NOT EXISTS fact_real_egresos (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL REFERENCES dim_time(date),
  proveedor_id TEXT,
  factura_id TEXT NOT NULL UNIQUE,
  categoria TEXT,
  subcategoria TEXT,
  monto_real NUMERIC NOT NULL
);
CREATE INDEX IF NOT EXISTS fact_real_egresos_cat_date_idx ON fact_real_egresos (categoria, date);

CREATE TABLE IF NOT EXISTS diccionario_categorias (
  id BIGSERIAL PRIMARY KEY,
  categoria_real TEXT,
  subcategoria_real TEXT,
  categoria_plan TEXT,
  subcategoria_plan TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
  id BIGSERIAL PRIMARY KEY,
  generated_at TIMESTAMPTZ DEFAULT NOW(),
  scope TEXT NOT NULL,
  key TEXT NOT NULL,
  metric TEXT NOT NULL,
  variance_pct NUMERIC NOT NULL,
  threshold_pct NUMERIC NOT NULL,
  status TEXT NOT NULL
);
