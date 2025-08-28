from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, Date, Boolean, Text

class Base(DeclarativeBase):
    pass

class DimTime(Base):
    __tablename__ = 'dim_time'
    date: Mapped[Date] = mapped_column(Date, primary_key=True)
    year: Mapped[int | None] = mapped_column(Integer)
    quarter: Mapped[int | None] = mapped_column(Integer)
    month: Mapped[int | None] = mapped_column(Integer)
    week: Mapped[int | None] = mapped_column(Integer)
    day: Mapped[int | None] = mapped_column(Integer)

class DimUnidad(Base):
    __tablename__ = 'dim_unidad'
    unidad_id: Mapped[str] = mapped_column(String, primary_key=True)
    torre: Mapped[str | None] = mapped_column(String)
    nivel: Mapped[str | None] = mapped_column(String)
    tipologia: Mapped[str | None] = mapped_column(String)
    m2: Mapped[float | None] = mapped_column(Numeric)
    precio_lista: Mapped[float | None] = mapped_column(Numeric)
    estatus: Mapped[str | None] = mapped_column(String)

class FactPlanIngresos(Base):
    __tablename__ = 'fact_plan_ingresos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date)
    unidad_id: Mapped[str | None] = mapped_column(String)
    concepto: Mapped[str | None] = mapped_column(Text)
    monto_plan: Mapped[float] = mapped_column(Numeric)
    escenario: Mapped[str | None] = mapped_column(String)
    version_id: Mapped[str] = mapped_column(String)
    valid_from: Mapped[str | None]
    valid_to: Mapped[str | None]
    is_current: Mapped[bool | None] = mapped_column(Boolean, default=True)

class FactPlanEgresos(Base):
    __tablename__ = 'fact_plan_egresos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date)
    categoria: Mapped[str] = mapped_column(String)
    subcategoria: Mapped[str | None] = mapped_column(String)
    concepto: Mapped[str | None] = mapped_column(Text)
    monto_plan: Mapped[float] = mapped_column(Numeric)
    escenario: Mapped[str | None] = mapped_column(String)
    version_id: Mapped[str] = mapped_column(String)
    valid_from: Mapped[str | None]
    valid_to: Mapped[str | None]
    is_current: Mapped[bool | None] = mapped_column(Boolean, default=True)

class FactRealIngresos(Base):
    __tablename__ = 'fact_real_ingresos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date)
    unidad_id: Mapped[str | None] = mapped_column(String)
    recibo_id: Mapped[str] = mapped_column(String)
    monto_real: Mapped[float] = mapped_column(Numeric)
    medio_pago: Mapped[str | None] = mapped_column(String)

class FactRealEgresos(Base):
    __tablename__ = 'fact_real_egresos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[Date] = mapped_column(Date)
    proveedor_id: Mapped[str | None] = mapped_column(String)
    factura_id: Mapped[str] = mapped_column(String)
    categoria: Mapped[str | None] = mapped_column(String)
    subcategoria: Mapped[str | None] = mapped_column(String)
    monto_real: Mapped[float] = mapped_column(Numeric)

class DiccionarioCategorias(Base):
    __tablename__ = 'diccionario_categorias'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    categoria_real: Mapped[str | None] = mapped_column(String)
    subcategoria_real: Mapped[str | None] = mapped_column(String)
    categoria_plan: Mapped[str | None] = mapped_column(String)
    subcategoria_plan: Mapped[str | None] = mapped_column(String)

class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    generated_at: Mapped[str | None]
    scope: Mapped[str] = mapped_column(String)
    key: Mapped[str] = mapped_column(String)
    metric: Mapped[str] = mapped_column(String)
    variance_pct: Mapped[float] = mapped_column(Numeric)
    threshold_pct: Mapped[float] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(String)
