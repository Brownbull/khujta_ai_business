# GabeDA Features: Regulatory Categorization by Development Stage

This document maps each analytical capability to the appropriate development stage based on Chilean regulatory constraints, specifying safe language and restrictions for each.

---

## STAGE 1: Single-Tenant SaaS Tool (Months 0-12)
### Regulatory Status: UNREGULATED
### Data Scope: Each client's own data only, completely segregated

---

### ✅ FULLY APPROVED FEATURES - No Language Restrictions

These features work exclusively with each client's own data and carry zero regulatory risk:

#### **A1. Análisis Pareto (Regla 80/20)**
- **Marketing Language:** ✅ "Identifica qué productos/clientes generan el 80% de TUS ventas"
- **Avoid:** ❌ "Compara con otras empresas" or "Benchmarks de industria"
- **Regulatory Note:** Safe - analyzes only client's own data

#### **A2. Alertas de Inventario**
- **Marketing Language:** ✅ "Te avisa cuando TUS productos se están agotando o acumulando"
- **Avoid:** ❌ "Estándares de la industria" or "Niveles óptimos comparativos"
- **Regulatory Note:** Safe - monitors only client's inventory

#### **A3. Salud de Inventario**
- **Marketing Language:** ✅ "Analiza la rotación de TU inventario"
- **Avoid:** ❌ "Compara tu rotación con otras empresas"
- **Regulatory Note:** Safe - client's own inventory metrics

#### **A4. Segmentación de Clientes**
- **Marketing Language:** ✅ "Agrupa TUS clientes por su comportamiento de compra"
- **Avoid:** ❌ "Evaluación de riesgo de clientes" or "Scoring de clientes"
- **Regulatory Note:** Safe - segments client's own customer base

#### **A5. Velocidad de Productos**
- **Marketing Language:** ✅ "Mide qué tan rápido se vende cada uno de TUS productos"
- **Avoid:** ❌ "Compara con velocidad promedio del sector"
- **Regulatory Note:** Safe - tracks client's own sales velocity

#### **A6. Pronóstico de Ventas Básico**
- **Marketing Language:** ✅ "Proyecta TUS ventas futuras basado en TU histórico"
- **Avoid:** ❌ "Predicciones de mercado" or "Tendencias de industria"
- **Regulatory Note:** Safe - forecasts based on client's own data

#### **A7. Análisis de Tendencias Temporales**
- **Marketing Language:** ✅ "Compara TU desempeño mes vs mes, año vs año"
- **Avoid:** ❌ "Rendimiento vs competencia"
- **Regulatory Note:** Safe - compares client to their own history

#### **B1. Análisis de Rentabilidad por Producto**
- **Marketing Language:** ✅ "Calcula la ganancia real de cada uno de TUS productos"
- **Avoid:** ❌ "Márgenes recomendados de la industria"
- **Regulatory Note:** Safe - analyzes client's own profitability

#### **B2. Análisis de Estacionalidad**
- **Marketing Language:** ✅ "Identifica patrones de venta en TU negocio por temporada"
- **Avoid:** ❌ "Patrones estacionales del sector"
- **Regulatory Note:** Safe - identifies client's own seasonal patterns

#### **B3. Análisis de Canastas (Market Basket)**
- **Marketing Language:** ✅ "Descubre qué productos TUS clientes compran juntos"
- **Avoid:** ❌ "Combinaciones populares en la industria"
- **Regulatory Note:** Safe - analyzes client's own transaction patterns

#### **B4. Detección de Clientes en Riesgo de Abandonar**
- **Marketing Language:** ✅ "Identifica TUS clientes que antes compraban seguido y ahora no"
- **Avoid:** ❌ "Evaluación de riesgo crediticio" or "Scoring de abandono"
- **Legal Note:** CRITICAL - Position as "behavioral patterns in YOUR customer base" NOT as "customer credit risk assessment"
- **Regulatory Note:** Safe if positioned as operational insight, NOT financial evaluation

#### **B5. Análisis de Punto de Reorden Inteligente**
- **Marketing Language:** ✅ "Calcula el momento exacto para pedir más inventario en TU negocio"
- **Avoid:** ❌ "Basado en mejores prácticas del sector"
- **Regulatory Note:** Safe - optimizes client's own inventory

#### **B6. Dashboard de Indicadores Clave (KPIs)**
- **Marketing Language:** ✅ "Vista rápida de la salud de TU negocio en una sola pantalla"
- **Avoid:** ❌ "Compara tus KPIs con el promedio de la industria"
- **Regulatory Note:** Safe - displays client's own metrics

#### **B7. Comparación con Meses/Años Anteriores (Benchmarking Personal)**
- **Marketing Language:** ✅ "Compara TU negocio con TU propio histórico"
- **Avoid:** ❌ "Benchmarking" alone (could imply industry comparison), use "Benchmarking Personal" or "Comparación Histórica"
- **Regulatory Note:** Safe - compares client to themselves, not to others

#### **C5. Procesamiento Inteligente de Documentos (Foto → Datos)**
- **Marketing Language:** ✅ "Digitaliza TUS boletas/facturas automáticamente con IA"
- **Avoid:** ❌ Any language suggesting cross-business data sharing
- **Regulatory Note:** Safe - processes client's own documents

#### **C7. Detección de Anomalías Automática**
- **Marketing Language:** ✅ "La IA detecta patrones inusuales en TU negocio automáticamente"
- **Avoid:** ❌ "Compara con patrones normales de la industria"
- **Regulatory Note:** Safe - detects anomalies in client's own data

#### **C8. Pronósticos Inteligentes Multi-Factor**
- **Marketing Language:** ✅ "Predicciones que consideran múltiples factores de TU negocio"
- **Avoid:** ❌ "Incorpora datos de mercado" or "Predicciones de industria"
- **Regulatory Note:** Safe if based on client's data + public events (holidays, seasons)

---

### ⚠️ APPROVED WITH LANGUAGE RESTRICTIONS

These features require careful positioning to avoid regulatory triggers:

#### **C1. Asistente de Voz/Chat para Consultas ("Habla con Tus Datos")**
- **Marketing Language:** ✅ "Pregunta sobre TU negocio en lenguaje natural"
- **Example Safe Query:** ✅ "¿Cuáles fueron mis 5 productos más vendidos?"
- **Avoid Queries Like:** ❌ "¿Debo invertir en este producto?" or "¿Es buen momento para expandir?"
- **Legal Note:** Train AI to respond with "insights" not "recommendations" or "advice"
- **Safe Response Format:** "Basado en tus datos, observo que..." NOT "Te recomiendo que..."
- **Regulatory Note:** Safe if positioned as data query tool, NOT business advisor

#### **C2. Explicaciones Inteligentes ("¿Por Qué Pasó Esto?")**
- **Marketing Language:** ✅ "La IA explica QUÉ pasó y POR QUÉ en TU negocio"
- **Safe Explanation Format:** ✅ "Tus ventas bajaron 15%. Detecté que: [observations]. Opciones a considerar: [options]"
- **Avoid:** ❌ "Recomendación:" use instead "Opciones:" or "Podrías considerar:"
- **Avoid:** ❌ "Debes hacer..." use instead "Podrías evaluar..." or "Una opción sería..."
- **Legal Note:** CRITICAL distinction:
  - ✅ "Observaciones" (observations)
  - ✅ "Opciones" (options)
  - ✅ "Posibilidades" (possibilities)
  - ❌ "Recomendaciones financieras" (financial recommendations)
  - ❌ "Consejos de inversión" (investment advice)
- **Regulatory Note:** Safe if framed as descriptive insights, NOT prescriptive advice

#### **C3. Alertas Predictivas ("Te Aviso ANTES de que Pase")**
- **Marketing Language:** ✅ "La IA predice situaciones en TU negocio y te avisa automáticamente"
- **Safe Alert Format:** 
  - ✅ "⚠️ Tu inventario llegará a 0 en 8 días según tendencia actual"
  - ✅ "💡 Se acerca diciembre, tus ventas históricas suben 60%"
- **Avoid Alert Format:**
  - ❌ "Debes comprar más inventario urgente" (imperative)
  - ✅ "Considera revisar inventario" (suggestion)
- **Regulatory Note:** Safe as predictive notifications, not directives

#### **C4. Recomendaciones Automáticas de Acciones**
- **⚠️ HIGH RISK FEATURE** - Requires most careful language
- **Marketing Language:** ✅ "La IA sugiere opciones basadas en TU situación específica"
- **NEVER SAY:** ❌ "Recomendaciones Automáticas" - change to "Opciones Sugeridas" or "Ideas para Considerar"
- **Safe Response Format:**
  - ✅ "Producto Z lleva 90 días sin moverse. **Opciones a evaluar:** 1) Descuento 30% 2) Bundle con productos A y B"
  - ✅ "**Posibilidades para inventario lento:** 1) Promoción 2x1 2) Consignación 3) Liquidación"
- **Avoid Response Format:**
  - ❌ "**Recomendación:** Debes hacer descuento" (sounds like advice)
  - ❌ "**Deberías:** renegociar con proveedor" (prescriptive)
- **Legal Note:** NEVER use:
  - ❌ "Recomendación financiera"
  - ❌ "Asesoría"
  - ❌ "Consejo de negocio"
  - ❌ "Debes/Deberías" (imperative/should)
- **Always use:**
  - ✅ "Opciones" (options)
  - ✅ "Podrías considerar" (you could consider)
  - ✅ "Una posibilidad sería" (one possibility would be)
  - ✅ "Basado en tus datos, observo" (based on your data, I observe)
- **Required Disclaimer:** Always include: "Esta información es solo para análisis operativo. Para decisiones financieras importantes, consulta con un contador o asesor financiero."
- **Regulatory Note:** Can be offered in Stage 1 ONLY with proper language disclaimers

#### **C6. Coach de Negocios Personalizado con IA**
- **⚠️ HIGHEST RISK FEATURE** - Most likely to trigger "financial advice" classification
- **Marketing Language:** ✅ "Asistente IA que analiza TU negocio y presenta opciones"
- **NEVER SAY:** ❌ "Coach de Negocios" or "Asesor" - use instead "Asistente de Análisis"
- **NEVER SAY:** ❌ "Te guía en decisiones" - use "Presenta opciones basadas en tus datos"
- **Safe Conversation Format:**
  ```
  Usuario: "¿Cómo puedo aumentar mis ventas?"
  
  ✅ IA: "Basado en el análisis de tus datos, identifico 3 patrones:
  1) Tienes 8 clientes que antes compraban $500k/mes y ahora no
  2) Producto A tiene alta demanda pero quiebres frecuentes
  3) Tus clientes frecuentes compran 40% más los viernes
  
  Opciones que podrías evaluar:
  - Contactar clientes inactivos con promoción
  - Ajustar inventario de Producto A
  - Considerar promoción especial jueves
  
  Para decisiones de inversión o financiamiento, te sugiero consultar con tu contador."
  ```
- **Avoid Conversation Format:**
  ```
  ❌ IA: "Te recomiendo que inviertas en más inventario de Producto A.
  Deberías contactar a esos clientes y ofrecerles 15% descuento.
  Esto aumentará tus ventas en $2M este mes."
  ```
- **Required Elements:**
  - Always present multiple options (never single directive)
  - Always frame as "basado en tus datos" (data-driven insights)
  - Always include disclaimer about financial/investment decisions
  - Never use imperative language (debe, tiene que, debería)
- **Prohibited Topics:**
  - ❌ Investment decisions ("invierte en X")
  - ❌ Financing recommendations ("solicita préstamo de X")
  - ❌ Tax optimization advice ("puedes reducir impuestos con X")
  - ❌ Legal structure recommendations ("deberías cambiar a SRL")
  - ❌ Credit evaluation ("tu crédito mejorará si...")
- **Safe Topics:**
  - ✅ Operational insights from client's data
  - ✅ Pattern identification in sales/inventory
  - ✅ Historical comparisons
  - ✅ Multiple strategic options for consideration
- **Regulatory Note:** Can be offered in Stage 1 ONLY if:
  1. Renamed to "Asistente de Análisis Inteligente"
  2. Strict language controls implemented
  3. Financial advice disclaimer always present
  4. Responses limited to data observations + multiple options
  5. Never prescriptive or directive

---

## STAGE 2: Internal Benchmarking Platform (Months 12-24)
### Regulatory Status: BORDERLINE - Must maintain "operational insights" positioning
### Data Scope: Client's own data + anonymous aggregate industry data

---

### 🔄 NEW FEATURES UNLOCKED IN STAGE 2

No new features from the menu are unlocked in Stage 2, but existing features gain enhanced capabilities:

#### **ALL STAGE 1 FEATURES + Anonymous Comparative Context**

**Example Enhancement for A6 (Sales Forecasting):**
- **Stage 1 Language:** "Proyecta tus ventas basado en tu histórico"
- **Stage 2 Language:** ✅ "Proyecta tus ventas basado en tu histórico + contexto anónimo del sector"
- **Example:** "Tu pronóstico: $4.5M próximo mes. Contexto: Empresas similares (anonimizadas) proyectan crecimiento 8-12% en este período"

**Example Enhancement for B7 (Historical Benchmarking):**
- **Stage 1 Language:** "Compara tu negocio con tu propio histórico"
- **Stage 2 Language:** ✅ "Compara tu desempeño histórico + contexto de empresas anónimas similares"
- **Example:** "Creciste 15% este año. Empresas similares en tu sector (datos anónimos) crecieron 8-18%"

**CRITICAL REQUIREMENTS for Stage 2:**

1. **Anonymization Must Be Irreversible:**
   - Cannot identify specific businesses or owners
   - Must aggregate minimum 5-10 businesses per comparison
   - No specific location data (use "región" not "Villarrica")

2. **Required Disclaimers:**
   - "Benchmarks basados en datos anónimos agregados"
   - "Solo para análisis operacional, no para evaluación crediticia"
   - "Los datos comparativos no identifican empresas específicas"

3. **Prohibited Language:**
   - ❌ "Compara tu perfil con otras empresas" (sounds like credit evaluation)
   - ❌ "Ranking de empresas" (implies identification)
   - ❌ "Tu posición vs competencia directa" (too specific)
   - ✅ "Contexto anónimo del sector" (safe)
   - ✅ "Rango típico para empresas similares" (safe)

4. **Marketing Positioning:**
   - ✅ "Benchmarking operacional con datos anónimos"
   - ✅ "Contexto de industria para mejores decisiones operativas"
   - ❌ "Inteligencia comercial" (triggers commercial data regulation)
   - ❌ "Evaluación comparativa para financiamiento" (triggers credit regulation)

---

## STAGE 3: Business Intelligence Platform (Months 24+)
### Regulatory Status: DEPENDS on chosen path

---

### Path A: UNREGULATED (Operational Intelligence)

Stay focused on operational insights without entering credit/financial evaluation space.

**All Stage 1 & 2 features remain available with same language constraints.**

**No new features from current menu require Stage 3** - all can be offered in Stages 1-2 with proper positioning.

---

### Path B: REGULATED (Commercial Intelligence)

If you decide to offer commercial intelligence for third-party evaluation (banks, suppliers, partners), you must:

1. **Implement Law 20.575 Compliance:**
   - Maintain detailed access logs
   - Provide data subjects with free log access every 4 months
   - Designate Chilean representative
   - Implement all 9 data protection principles

2. **New Permissible Language:**
   - ✅ "Perfiles comerciales para evaluación de socios"
   - ✅ "Inteligencia comercial para transacciones B2B"
   - ✅ "Información de salud financiera empresarial"

3. **Still PROHIBITED Without CMF License:**
   - ❌ "Calificación de riesgo crediticio" (credit rating)
   - ❌ "Asesoría de inversión" (investment advice)
   - ❌ "Recomendaciones financieras" (financial recommendations)

---

## SUMMARY TABLE: Feature Availability by Stage

| Feature                       | Stage 1 | Stage 2   | Stage 3 | Risk Level  |
| ----------------------------- | ------- | --------- | ------- | ----------- |
| A1-A7 (Traditional Analytics) | ✅       | ✅         | ✅       | 🟢 Low       |
| B1-B6 (Advanced Analytics)    | ✅       | ✅         | ✅       | 🟢 Low       |
| B7 (Historical Benchmarking)  | ✅ (own) | ✅ (+anon) | ✅       | 🟢 Low       |
| C1 (Voice/Chat Assistant)     | ✅*      | ✅*        | ✅*      | 🟡 Medium    |
| C2 (Intelligent Explanations) | ✅*      | ✅*        | ✅*      | 🟡 Medium    |
| C3 (Predictive Alerts)        | ✅*      | ✅*        | ✅*      | 🟡 Medium    |
| C4 (Action Recommendations)   | ✅**     | ✅**       | ✅**     | 🔴 High      |
| C5 (Document Processing)      | ✅       | ✅         | ✅       | 🟢 Low       |
| C6 (Business Coach)           | ✅***    | ✅***      | ✅***    | 🔴 Very High |
| C7 (Anomaly Detection)        | ✅       | ✅         | ✅       | 🟢 Low       |
| C8 (Multi-Factor Forecasting) | ✅       | ✅         | ✅       | 🟢 Low       |

**Legend:**
- ✅ = Available with standard language
- ✅* = Available with language restrictions
- ✅** = Available with strict disclaimers required
- ✅*** = Available only if renamed and heavily restricted language
- 🟢 Low Risk = No regulatory concerns
- 🟡 Medium Risk = Requires careful language
- 🔴 High Risk = Requires strict controls and disclaimers
- 🔴 Very High Risk = Consider removing or heavily modifying

---

## MANDATORY DISCLAIMERS BY FEATURE

### For C4 (Action Recommendations):
**Spanish:** "Esta información presenta opciones basadas en el análisis de tus datos operacionales. No constituye asesoría financiera, contable, legal o de inversión. Para decisiones financieras importantes, consulta con profesionales especializados."

**Required Location:** Below every "recommendation" screen, in small but readable text

---

### For C6 (Business Coach/Assistant):
**Spanish:** "Este asistente analiza tus datos operacionales y presenta opciones para tu consideración. No proporciona asesoría financiera, de inversión, contable, legal o tributaria. Las decisiones financieras importantes deben ser consultadas con contadores, asesores financieros u otros profesionales especializados."

**Required Location:** 
1. Permanently visible at bottom of chat interface
2. First message when user initiates conversation
3. After any query about financial/investment topics

---

### For Stage 2 Benchmarking Features:
**Spanish:** "Los datos comparativos provienen de información anónima agregada y no identifican empresas específicas. Esta información es solo para análisis operacional y mejora de procesos, no para evaluación crediticia o decisiones de financiamiento."

**Required Location:** Wherever comparative/benchmark data is displayed

---

## IMPLEMENTATION RECOMMENDATIONS

### Priority 1: Launch with Low-Risk Features
Start with all 🟢 Low Risk features in Stage 1:
- A1-A7 (Traditional Analytics)
- B1-B6 (Advanced Analytics - except B7 comparative part)
- C5 (Document Processing)
- C7 (Anomaly Detection)
- C8 (Forecasting)

### Priority 2: Add Medium-Risk Features with Controls
Add 🟡 Medium Risk features once proper language controls implemented:
- C1 (Voice/Chat)
- C2 (Intelligent Explanations)
- C3 (Predictive Alerts)

### Priority 3: Consider Carefully
For 🔴 High Risk features, evaluate if business value justifies complexity:
- C4: Either remove "Recommendations" language entirely or implement strict disclaimer system
- C6: Strongly consider removing or renaming to "Data Analysis Assistant" with heavy restrictions

### Legal Review Required Before Launch
Have Chilean data protection lawyer review:
1. All AI-generated response templates for C1, C2, C4, C6
2. Disclaimer language and placement
3. Terms of Service clearly stating service limitations
4. Privacy Policy addressing data usage

---

## RECOMMENDED FEATURE NAMING FOR MARKET

To avoid regulatory triggers, rename features in customer-facing materials:

| Current Name                | Recommended Name                                                | Reason                                     |
| --------------------------- | --------------------------------------------------------------- | ------------------------------------------ |
| Coach de Negocios           | Asistente de Análisis de Datos                                  | Avoid "coach/asesor"                       |
| Recomendaciones Automáticas | Opciones Sugeridas                                              | Avoid "recomendaciones"                    |
| Benchmarking                | Comparación Histórica (Stage 1)<br>Contexto de Sector (Stage 2) | "Benchmarking" implies industry comparison |

---

**Document Version:** 1.0  
**Last Updated:** Based on Chilean regulatory analysis October 2025  
**Legal Review Required:** Yes, before implementing Medium/High risk features  
**Next Review:** Before Stage 2 transition (Month 12)