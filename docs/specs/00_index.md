# GabeDA - Clasificación de Features por Workflow de Datos

## Estructura del Workflow

```
INPUT → PREPROCESS → FILTERS → ATTRIBUTES → SCORE
```

**INPUT:** CSV transaccional (trans_id, fecha, producto, glosa, costo, total, cantidad, inith, initm, customer_id, customer_name, customer_location)

**PREPROCESS:** Limpieza, formato de fechas, eliminación de NAs, validación de tipos de datos

**FILTERS:** Cálculos fila por fila (nuevas columnas derivadas)

**ATTRIBUTES:** Agregaciones (por cliente, producto, fecha, etc.)

**SCORE:** Cálculo de scores/métricas finales usando attributes

---

## SECCIÓN A: Analítica Tradicional (Capacidades Actuales)

### A1. Análisis Pareto (Regla 80/20)

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ ATTRIBUTES: 
  - Agregación de ventas por producto: `SUM(total) GROUP BY producto`
  - Agregación de ventas por cliente: `SUM(total) GROUP BY customer_id`
  - Ordenamiento descendente por total
- ✅ SCORE:
  - Cálculo de % acumulado
  - Identificación del punto 80/20
  - Ranking de contribución

**Outputs clave:**
- Lista de productos Top 20% que generan 80% ingresos
- Lista de clientes Top 20% que generan 80% ingresos

---

### A2. Alertas de Inventario

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos, validación de stock
- ✅ FILTERS:
  - Cálculo de días desde última venta: `fecha - MAX(fecha) per producto`
- ✅ ATTRIBUTES:
  - Stock actual por producto (si se tiene campo stock, o inferido de inith/initm)
  - Promedio ventas diarias por producto: `AVG(cantidad) per día per producto`
  - Días sin movimiento: `current_date - MAX(fecha) per producto`
- ✅ SCORE:
  - Días de stock restante = `stock_actual / promedio_ventas_diarias`
  - Flags de alerta: stock_bajo (< 7 días), sin_movimiento (> 90 días)

**Outputs clave:**
- Productos con < 7 días de stock
- Productos sin venta en 90+ días

---

### A3. Salud de Inventario

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Margen por transacción: `total - costo`
  - Valor inventario por producto: `stock_actual * costo_unitario`
- ✅ ATTRIBUTES:
  - Rotación de inventario = `total_ventas_periodo / promedio_inventario`
  - Días de inventario = `365 / rotación`
  - Valor total inventario estancado (> 60 días sin venta)
  - % inventario lento vs total
- ✅ SCORE:
  - Índice de salud (0-100) basado en rotación y días
  - Categorización: saludable / atención / crítico

**Outputs clave:**
- Monto en inventario estancado
- Rotación por producto
- Score de salud de inventario

---

### A4. Segmentación de Clientes

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos, estandarización customer_id
- ✅ ATTRIBUTES:
  - Recency: días desde última compra por cliente
  - Frequency: número de transacciones por cliente
  - Monetary: total gastado por cliente
  - Primera compra: `MIN(fecha) per customer_id`
- ✅ SCORE:
  - Segmentos RFM:
    - Frecuentes: frequency > X, recency < Y
    - Ocasionales: frequency mediano, recency mediana
    - Dormidos: recency > 90 días, frequency > 0 histórico
    - Nuevos: primera compra < 60 días

**Outputs clave:**
- Conteo de clientes por segmento
- Lista de clientes por categoría

---

### A5. Velocidad de Productos

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Extracción de día juliano: `DATE_TO_DAY(fecha)`
- ✅ ATTRIBUTES:
  - Días entre transacciones por producto
  - Promedio días entre ventas: `AVG(días_entre_ventas) per producto`
  - Frecuencia de venta: `COUNT(trans_id) / días_operación per producto`
- ✅ SCORE:
  - Velocidad categorizada:
    - Rápida: < 7 días entre ventas
    - Media: 7-30 días
    - Lenta: > 30 días

**Outputs clave:**
- Días promedio para vender cada producto
- Categorización velocidad

---

### A6. Pronóstico de Ventas Básico

**Workflow:**
- ✅ PREPROCESS: Limpieza, ordenamiento temporal
- ✅ FILTERS:
  - Extracción de mes, año: `MONTH(fecha), YEAR(fecha)`
- ✅ ATTRIBUTES:
  - Ventas mensuales históricas: `SUM(total) GROUP BY año, mes`
  - Promedio móvil (3 meses, 6 meses)
  - Tendencia lineal
- ✅ SCORE:
  - Proyección mes siguiente usando:
    - Promedio móvil
    - Tendencia lineal
    - Estacionalidad (si detectada)

**Outputs clave:**
- Ventas proyectadas próximo mes
- Intervalo de confianza

---

### A7. Análisis de Tendencias Temporales

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Extracción temporal: año, mes, semana
- ✅ ATTRIBUTES:
  - Ventas por período (mes, año)
  - Comparaciones período anterior
  - Comparaciones mismo período año anterior
- ✅ SCORE:
  - % cambio mes vs mes anterior: `(mes_actual - mes_anterior) / mes_anterior`
  - % cambio año sobre año: `(mes_actual_año - mes_mismo_año_anterior) / mes_mismo_año_anterior`
  - Dirección de tendencia: creciente/estable/decreciente

**Outputs clave:**
- % crecimiento mes vs mes
- % crecimiento año sobre año
- Gráfica de tendencia

---

## SECCIÓN B: Nuevas Capacidades Analíticas (Sin IA)

### B1. Análisis de Rentabilidad por Producto

**Workflow:**
- ✅ PREPROCESS: Limpieza, validación costo y total
- ✅ FILTERS:
  - Margen unitario: `total - costo`
  - % margen: `(total - costo) / total * 100`
- ✅ ATTRIBUTES:
  - Margen total por producto: `SUM(margen) GROUP BY producto`
  - % margen promedio por producto: `AVG(% margen) per producto`
  - Volumen de ventas por producto
- ✅ SCORE:
  - Rentabilidad = margen_total * volumen_ventas
  - Ranking por rentabilidad
  - Categorización: alta/media/baja rentabilidad

**Outputs clave:**
- Productos con mayor margen absoluto
- Productos con mayor % margen
- Matriz volumen vs margen

---

### B2. Análisis de Estacionalidad

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Componentes temporales: mes, trimestre, día_semana
  - Flags: es_fin_semana, es_feriado
- ✅ ATTRIBUTES:
  - Ventas por mes (agregadas multi-año)
  - Ventas por día de semana
  - Ventas por trimestre
  - Índice estacional = `ventas_período / promedio_general`
- ✅ SCORE:
  - Coeficiente de variación estacional
  - Períodos peak vs valle
  - Factores de estacionalidad por período

**Outputs clave:**
- Meses con mayor/menor venta
- Días de semana más activos
- Factores de ajuste estacional

---

### B3. Análisis de Canastas (Market Basket)

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Agrupación de transacciones: `GROUP BY trans_id, customer_id, fecha`
  - Creación de "cestas" (productos comprados juntos en misma transacción/día)
- ✅ ATTRIBUTES:
  - Frecuencia de pares de productos: `COUNT(producto_A AND producto_B en misma transacción)`
  - Frecuencia individual de cada producto
- ✅ SCORE:
  - Support: `freq(A,B) / total_transacciones`
  - Confidence: `freq(A,B) / freq(A)`
  - Lift: `confidence(A→B) / support(B)`
  - Reglas de asociación con lift > 1

**Outputs clave:**
- Pares de productos frecuentemente comprados juntos
- Reglas: "Si compra A, probablemente compre B"
- Lift scores

---

### B4. Detección de Clientes en Riesgo de Abandonar

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ ATTRIBUTES:
  - Recencia actual por cliente: `days_since_last_purchase`
  - Frecuencia histórica esperada: `AVG(días_entre_compras) per customer`
  - Desviación de patrón: `recencia_actual - frecuencia_esperada`
  - Valor histórico del cliente: `SUM(total) per customer`
- ✅ SCORE:
  - Riesgo de churn = `recencia_actual / frecuencia_esperada`
  - Categorías:
    - Alto riesgo: recencia > 2x frecuencia esperada
    - Riesgo medio: recencia > 1.5x frecuencia
    - Activo: dentro del patrón normal
  - Prioridad = riesgo * valor_histórico

**Outputs clave:**
- Lista de clientes en riesgo alto
- Clientes priorizados por valor
- Días desde esperada compra

---

### B5. Análisis de Punto de Reorden Inteligente

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ ATTRIBUTES:
  - Velocidad de venta diaria: `AVG(cantidad) per día per producto`
  - Desviación estándar de ventas: `STDDEV(cantidad) per producto`
  - Lead time proveedor (si disponible o asumido)
  - Stock actual
  - Stock de seguridad = `Z_score * STDDEV(ventas_diarias) * SQRT(lead_time)`
- ✅ SCORE:
  - Punto de reorden = `(velocidad_venta * lead_time) + stock_seguridad`
  - Cantidad óptima de pedido (EOQ) si se tienen costos
  - Días hasta stockout: `stock_actual / velocidad_venta`

**Outputs clave:**
- Punto de reorden por producto
- Cuándo pedir (alerta cuando stock < punto_reorden)
- Cantidad sugerida de pedido

---

### B6. Dashboard de Indicadores Clave (KPIs)

**Nota:** No es un proceso de datos per se, sino una visualización de outputs de otros análisis.

**Inputs desde otros workflows:**
- Ventas del mes (A7)
- Margen promedio (B1)
- Inventario crítico (A2)
- Clientes activos (A4)
- Productos top (A1)
- Tendencia de crecimiento (A7)

**Presentación:**
- Formato de dashboard visual
- Métricas en tiempo real
- Comparaciones período anterior
- Indicadores visuales (colores, gráficos)

---

### B7. Comparación con Meses/Años Anteriores (Benchmarking Personal)

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS:
  - Componentes de fecha: año, mes, semana
- ✅ ATTRIBUTES:
  - KPIs por período:
    - Ventas totales
    - Margen promedio
    - Cantidad de transacciones
    - Ticket promedio: `AVG(total) per transacción`
    - Productos vendidos
    - Clientes únicos
- ✅ SCORE:
  - Variaciones período sobre período:
    - `(KPI_actual - KPI_anterior) / KPI_anterior`
  - Variaciones año sobre año:
    - `(KPI_mes_actual - KPI_mismo_mes_año_anterior) / KPI_mismo_mes_año_anterior`
  - Índices de desempeño relativo

**Outputs clave:**
- Tabla comparativa multi-período
- % cambios en cada métrica
- Indicadores de mejora/deterioro

---

## SECCIÓN C: Capacidades con Inteligencia Artificial

### C1. Asistente de Voz/Chat para Consultas

**Workflow:**
- **No es parte del pipeline de datos, sino una capa de interfaz**
- Consume outputs de ATTRIBUTES y SCORES de otros análisis

**Arquitectura:**
- INPUT: Query en lenguaje natural (español)
- NLP Processing: Interpretación de intención del usuario
- Query Translation: Convierte pregunta a consulta de datos
- Data Retrieval: Obtiene datos de attributes/scores existentes
- Response Generation: Genera respuesta en lenguaje natural

**Requisitos de datos:**
- Acceso a todos los attributes y scores generados
- Metadata de qué análisis están disponibles
- Contexto del negocio del cliente

**Ejemplo:**
- Usuario: "¿Cuáles fueron mis 5 productos más vendidos en julio?"
- Sistema: 
  - Identifica: query de ranking de productos
  - Filtra: mes = julio
  - Obtiene: output de A1 (Pareto) filtrado
  - Responde: "Los más vendidos en julio fueron..."

---

### C2. Explicaciones Inteligentes ("¿Por Qué Pasó Esto?")

**Workflow:**
- Capa de análisis **post-SCORE** que genera narrativa

**Arquitectura:**
```
Detecta cambio → Identifica causas posibles → Genera explicación
```

**Proceso:**
1. Detecta anomalía/cambio (ej: ventas -15%)
2. Analiza factores contribuyentes:
   - ✅ ATTRIBUTES correlacionados:
     - Quiebres de stock (de A2)
     - Días operacionales (calendarios, feriados)
     - Cambios en mix de productos
   - Factores externos (si disponible):
     - Competencia
     - Estacionalidad (de B2)
3. ✅ SCORE: Peso de cada factor
4. AI: Genera narrativa explicativa con recomendaciones

**Inputs requeridos:**
- Todos los attributes de análisis previos
- Calendario de eventos (feriados, campañas)
- Datos de contexto (competencia, clima, etc.) si disponible

---

### C3. Alertas Predictivas

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS: Cálculos temporales
- ✅ ATTRIBUTES:
  - Series temporales por producto/cliente
  - Tendencias recientes (últimas 2-4 semanas)
  - Desviaciones de patrón normal
- ✅ SCORE: 
  - Modelos predictivos simples:
    - Proyección lineal
    - Promedio móvil exponencial
    - Detección de tendencias
  - Umbrales de alerta configurables
- 🤖 AI: 
  - Algoritmos de forecasting (ARIMA, Prophet)
  - Clasificación de urgencia de alerta
  - Generación de mensaje contextual

**Tipos de alertas:**
1. **Alerta de Stockout:**
   - Predicción: días hasta stock = 0
   - Trigger: < 7 días predichos
   
2. **Alerta de Demanda:**
   - Detección: tendencia acelerada > 30%
   - Trigger: Z-score > 2
   
3. **Alerta de Churn:**
   - Score de riesgo de B4
   - Trigger: cliente de alto valor en riesgo alto

---

### C4. Recomendaciones Automáticas de Acciones

**Workflow:**
- **Post-SCORE:** Motor de recomendaciones basado en reglas + AI

**Arquitectura:**
```
Situación detectada → Reglas de negocio → Opciones generadas → Ranking → Recomendación
```

**Proceso:**
1. Identifica problema (ej: inventario lento)
2. ✅ Recupera ATTRIBUTES relevantes:
   - Valor en inventario lento (de A3)
   - Productos afectados
   - Margen histórico (de B1)
   - Productos complementarios (de B3)
3. Aplica reglas de negocio:
   - Si margen > 40% → puede descontar 30%
   - Si tiene complemento popular → bundle
4. 🤖 AI: 
   - Genera múltiples estrategias
   - Evalúa impacto esperado
   - Rankea por probabilidad de éxito
5. Output: Lista priorizada de acciones

**Ejemplo lógica:**
```python
if producto.dias_sin_venta > 90:
    opciones = []
    if producto.margen > 40%:
        opciones.append("Descuento 30%")
    if tiene_complemento_popular(producto):
        opciones.append(f"Bundle con {complemento}")
    if producto.costo < valor_promedio_inventario * 0.1:
        opciones.append("Liquidación")
    return AI_rank_opciones(opciones, contexto_negocio)
```

---

### C5. Procesamiento Inteligente de Documentos (OCR + AI)

**Workflow:**
- **Enhancement del INPUT stage**

**Arquitectura:**
```
Foto/Scan → OCR → Extracción de campos → Validación → Estructuración → INPUT
```

**Proceso:**
1. **INPUT**: Imagen de boleta/factura
2. **OCR Processing:**
   - Detección de texto
   - Reconocimiento de caracteres
3. **🤖 AI - Field Extraction:**
   - Identifica tipo de documento (boleta, factura, inventario)
   - Extrae campos:
     - Fecha
     - Monto total
     - Items/productos
     - Proveedor/cliente
     - RUT si aplica
4. **Validation:**
   - Formato de fecha
   - Validación de RUT
   - Coherencia de montos
5. **Estructuración:**
   - Convierte a formato CSV estándar
   - Mapea a schema: (trans_id, fecha, producto, glosa, costo, total, cantidad, customer_id, etc.)
6. **OUTPUT**: Row(s) para añadir al INPUT CSV

**Tecnologías requeridas:**
- OCR engine (Tesseract, Google Vision API, AWS Textract)
- AI model para clasificación de documentos
- NER (Named Entity Recognition) para extracción de campos
- Reglas de validación Chile-específicas (formato RUT, formato boleta)

---

### C6. Coach de Negocios Personalizado con IA

**Workflow:**
- **Capa conversacional que consume todos los ATTRIBUTES y SCORES**

**Arquitectura:**
```
Pregunta → Entendimiento de intención → Análisis multi-source → Síntesis → Recomendación
```

**Componentes:**
1. **Conversational AI:**
   - Procesa pregunta del usuario
   - Mantiene contexto de conversación
   
2. **Knowledge Retrieval:**
   - Accede a TODOS los attributes generados
   - Identifica qué análisis son relevantes
   
3. **Business Logic:**
   - Reglas de negocio del rubro
   - Best practices de retail/comercio
   
4. **🤖 AI Reasoning:**
   - Analiza múltiples attributes simultáneamente
   - Identifica patrones y oportunidades
   - Prioriza recomendaciones
   
5. **Response Generation:**
   - Genera explicación comprensible
   - Incluye datos específicos del negocio
   - Sugiere acciones concretas

**Ejemplo flujo:**
```
Usuario: "¿Cómo puedo aumentar mis ventas?"

Coach AI:
1. Analiza ventas actuales (A7)
2. Identifica clientes dormidos (B4) → 8 clientes, $500k/mes histórico
3. Detecta quiebres de stock (A2) → Producto A con alta demanda
4. Analiza días de venta (B2) → Viernes +40% vs otros días
5. Sintetiza: 3 oportunidades priorizadas
6. Genera respuesta personalizada con números del negocio
```

---

### C7. Detección de Anomalías Automática

**Workflow:**
- ✅ PREPROCESS: Limpieza de datos
- ✅ FILTERS: Cálculos temporales, ventanas móviles
- ✅ ATTRIBUTES:
  - Series temporales de métricas clave:
    - Ventas diarias por producto
    - Gastos operacionales
    - Ticket promedio
    - Tráfico de clientes
  - Estadísticas de normalidad:
    - Media móvil (7 días, 30 días)
    - Desviación estándar
    - Percentiles (P5, P95)
- ✅ SCORE:
  - Z-score para cada métrica: `(valor_actual - media) / std_dev`
  - Detección de outliers: |Z-score| > 2
  - Tipo de anomalía: spike positivo/negativo, cambio de tendencia
- 🤖 AI:
  - Algoritmos de detección:
    - Isolation Forest
    - Autoencoders para patrones complejos
    - LSTM para series temporales
  - Clasificación de severidad
  - Contextualización (es anomalía real o evento esperado)

**Tipos de anomalías detectables:**
1. **Anomalía de volumen:** Producto vende 0 vs 5-8 diario normal
2. **Anomalía de gasto:** Gastos +40% sin razón aparente
3. **Anomalía de patrón:** Cambio de día peak de viernes a sábado
4. **Anomalía de distribución:** Mix de productos muy diferente

**Output:**
- Alerta con:
  - Qué métrica
  - Valor esperado vs observado
  - Severidad (crítico/moderado/información)
  - Sugerencia de investigación

---

### C8. Pronósticos Inteligentes Multi-Factor

**Workflow:**
- ✅ PREPROCESS: Limpieza, imputación de valores faltantes
- ✅ FILTERS:
  - Features temporales: mes, día_semana, semana_año, es_feriado
  - Features de lag: ventas_7d_atras, ventas_30d_atras
  - Features de tendencia: crecimiento_reciente
- ✅ ATTRIBUTES:
  - Agregaciones temporales multinivel
  - Factores estacionales (de B2)
  - Eventos calendarios (feriados, campañas)
  - Variables exógenas si disponible (clima, competencia)
- ✅ SCORE - ML Models:
  - **Modelo 1 - Simple:** Promedio móvil ponderado + estacionalidad
  - **Modelo 2 - Estadístico:** ARIMA o Prophet
  - **Modelo 3 - ML:** 
    - XGBoost o LightGBM con features multi-factor
    - Features: lag values, día semana, mes, tendencia, estacionalidad, eventos
  - **Ensemble:** Combina predicciones de múltiples modelos
  
**Feature Engineering para ML:**
```python
features = {
    'temporal': ['mes', 'dia_semana', 'semana_año', 'trimestre'],
    'lags': ['ventas_lag_7', 'ventas_lag_14', 'ventas_lag_30'],
    'rolling': ['ventas_rolling_7d', 'ventas_rolling_30d'],
    'trends': ['tendencia_7d', 'tendencia_30d'],
    'seasonality': ['factor_estacional_mes', 'factor_dia_semana'],
    'events': ['es_feriado', 'dias_hasta_feriado', 'es_mes_campaña'],
    'external': ['competencia_nueva', 'clima_categoria'] # si disponible
}
```

**Output avanzado:**
- Pronóstico puntual (valor esperado)
- Intervalos de confianza (P10, P90)
- Descomposición: tendencia + estacionalidad + residual
- Factores de influencia (feature importance)
- Recomendaciones operativas basadas en forecast

**Ejemplo output:**
```
Pronóstico Noviembre 2025:
- Ventas esperadas: $4.2M (rango: $3.9M - $4.5M)
- Basado en:
  * Histórico nov 2023-2024: +$50k cada año
  * Tendencia actual: +12% últimos 3 meses
  * Black Friday semana 4: +30% impacto esperado
  * Factor estacional noviembre: 1.15x
- Drivers principales:
  1. Estacionalidad (40% de predicción)
  2. Tendencia de crecimiento (30%)
  3. Evento Black Friday (20%)
  4. Día de semana (10%)
- Recomendaciones:
  * Productos A,B,C: aumentar stock 40%
  * Producto D: mantener normal
  * Staff: considerar +2 personas semana 4
- Riesgos:
  * Competencia nueva (monitorear primeras 2 semanas)
  * Incertidumbre: ±$300k (7%)
```

---

## RESUMEN: Arquitectura de Datos Completa

### Pipeline Core (Todos los Features)
```
CSV Input
    ↓
[PREPROCESS] → Datos limpios y validados
    ↓
[FILTERS] → Datos + columnas derivadas (margins, dates, etc.)
    ↓
[ATTRIBUTES] → Agregaciones por entidad (cliente, producto, período)
    ↓
[SCORES] → Métricas finales, rankings, clasificaciones
    ↓
[OUTPUTS] → Reportes, dashboards, alertas
```

### Capas AI (Enhancements)

**Input Enhancement:**
- C5: OCR/Document Processing → mejora INPUT

**Analysis Enhancement:**
- C3: Predictive Alerts → mejora SCORE con ML forecasting
- C7: Anomaly Detection → mejora SCORE con ML detection
- C8: Multi-factor Forecasting → mejora SCORE con ML avanzado

**Interpretation Enhancement:**
- C2: Intelligent Explanations → post-SCORE narrativa
- C4: Automated Recommendations → post-SCORE acción

**Interface Enhancement:**
- C1: Conversational Interface → consume ATTRIBUTES/SCORES
- C6: Business Coach → consume todo, razonamiento avanzado

---

## Priorización de Implementación

### Fase 1: Foundation (Sin AI)
**Implementar:** A1-A7, B1, B7
- Pipeline básico: Input → Preprocess → Filters → Attributes → Score
- Analytics fundamentales

### Fase 2: Advanced Analytics (Sin AI)
**Implementar:** B2-B6
- Requires más feature engineering
- Análisis más sofisticados

### Fase 3: AI Layer - Quick Wins
**Implementar:** C2 (Explanations), C5 (OCR)
- C2 usa LLM sobre datos existentes (rápido)
- C5 resuelve pain point crítico de input

### Fase 4: AI Layer - Predictive
**Implementar:** C3 (Alerts), C7 (Anomalies)
- Modelos ML simples primero
- Mejora operativa significativa

### Fase 5: AI Layer - Advanced
**Implementar:** C8 (Advanced Forecasting), C4 (Recommendations)
- ML más complejo
- Requiere datos históricos suficientes (6+ meses)

### Fase 6: AI Interface
**Implementar:** C1 (Chat), C6 (Coach)
- Capa conversacional sobre todo lo anterior
- Mayor impacto UX

---

## Dependencias de Datos

### Campos CSV actuales:
- ✅ trans_id, fecha, producto, glosa, costo, total, cantidad
- ✅ customer_id, customer_name, customer_location
- ✅ inith, initm (horarios?)

### Campos adicionales útiles:
- 🔴 **stock_actual**: para A2, A3, B5 (crítico)
- 🟡 **categoria_producto**: mejora B3, análisis categorial
- 🟡 **proveedor**: para análisis de proveedores
- 🟡 **costo_fijo_producto**: para B1 mejorado
- 🟡 **lead_time_proveedor**: para B5 más preciso
- 🟡 **es_feriado, eventos**: para C8 forecasting

### Fuentes externas opcionales:
- 📅 Calendario de feriados Chile
- 🌦️ Datos de clima (si aplica al negocio)
- 💰 Indicadores económicos (IPC, tipo cambio)
- 🏢 Datos de competencia (si disponible)

---

**Este documento debe actualizarse a medida que:**
1. Se implementen nuevos features
2. Se descubran nuevas dependencies
3. Se refine el data pipeline
4. Se agreguen nuevos campos al CSV