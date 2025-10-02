"""
Translation module for multi-language support
Supports: ENG (English), ESP (Spanish)
"""

TRANSLATIONS = {
    'ENG': {
        # Common
        'customers': 'customers',
        'customer': 'customer',
        'products': 'products',
        'product': 'product',
        'day': 'day',
        'days': 'days',
        'purchase': 'purchase',
        'purchases': 'purchases',
        'transactions': 'transactions',
        'ago': 'ago',

        # KPIs
        'periods_for_growth': 'Periods considered for growth:',
        'previous': 'Previous',
        'current': 'Current',
        'growth': 'Growth',
        'revenue': 'Revenue',
        'total_revenue': 'Total Revenue',
        'avg_transaction': 'Avg Transaction',

        # Alerts
        'critical_actions': 'CRITICAL ACTIONS REQUIRED:',
        'warnings': 'WARNINGS:',
        'success_indicators': 'SUCCESS INDICATORS:',
        'impact': 'Impact',
        'action': 'Action',
        'next_step': 'Next Step',

        # Pareto
        'top_insight': 'TOP INSIGHT',
        'concentration_risk': 'Concentration Risk Level',
        'top_revenue_generators': 'Top Revenue Generators',
        'top_products': 'Your top {count} products ({pct}% of catalog) generate {revenue_pct}% of revenue!',
        'pareto_rule': '80/20 Rule: Top 20% = {pct}% of revenue',

        # Inventory
        'inventory_health_score': 'Inventory Health Score',
        'dead_stock_alert': 'Dead Stock Alert',

        # Peak Times
        'peak_performance': 'Peak Performance Windows:',
        'best_day': 'Best Day',
        'peak_hour': 'Peak Hour',
        'slowest_day': 'Slowest Day',
        'optimize_staffing': 'Optimize staffing for {day} around {hour}',

        # Customer Segmentation
        'champions': 'Champions',
        'loyal_customers': 'Loyal Customers',
        'recent_customers': 'Recent Customers',
        'at_risk': 'At Risk',
        'need_attention': 'Need Attention',
        'customer_segmentation': 'Customer/Transaction Segmentation Analysis',
        'customer_segments': 'Customer Segments:',
        'total_customers': 'Total Customers',
        'avg_recency': 'Avg Recency',
        'avg_frequency': 'Avg Frequency',
        'avg_monetary': 'Avg Monetary',
        'last_purchase': 'Last Purchase',
        'rfm_score': 'RFM Score',
        'why_segment': 'Why {segment}?',

        # Detailed Segmentation Report
        'detailed_segmentation_report': 'DETAILED CUSTOMER SEGMENTATION REPORT',
        'rfm_explanation_title': 'Understanding RFM Scores:',
        'rfm_r_label': 'R (Recency)',
        'rfm_r_desc': 'How recently the customer made a purchase (days ago → segment)',
        'rfm_f_label': 'F (Frequency)',
        'rfm_f_desc': 'How often the customer makes purchases (count → segment)',
        'rfm_m_label': 'M (Monetary)',
        'rfm_m_desc': 'How much money the customer spends (total → segment)',
        'rfm_quartile_note': 'Segments rank customers: S1 (lowest) to S4 (highest performance)',

        # Segment Explanations
        'exp_purchased_recently': 'Purchased very recently (top tier recency)',
        'exp_high_frequency': 'High purchase frequency (top tier loyalty)',
        'exp_high_spending': 'High total spending (top tier revenue)',
        'exp_strong_revenue': 'Strong revenue contribution',
        'exp_regular_customer': 'Regular customer with consistent orders',
        'exp_building_history': 'Building purchase history',
        'exp_potential_engagement': 'Potential for increased engagement',
        'exp_not_purchased': "Haven't purchased recently (needs attention)",
        'exp_churn_risk': 'Risk of customer churn',
        'exp_reengagement': 'Recommended: Re-engagement campaign',
        'exp_moderate_engagement': 'Moderate engagement levels',
        'exp_opportunity': 'Opportunity for improvement',
        'exp_targeted_promo': 'Recommended: Targeted promotions',

        # Forecast
        'revenue_forecast': 'Revenue Forecast for next {days} days:',
        'daily': 'Daily:',
        'average': 'Average',
        'std_dev': 'Std Dev',
        'confidence_interval': 'Confidence Interval',
        'total': 'Total:',
        'forecast': 'Forecast',
        'trend': 'Trend',
        'increasing': 'Increasing',
        'decreasing': 'Decreasing',
        'stable': 'Stable',

        # Cross-sell
        'cross_sell_opportunities': 'Cross-Sell Opportunities:',
        'no_cross_sell': 'No significant cross-sell opportunities found.',

        # Anomalies
        'anomalies_detected': 'Anomalies Detected:',
        'no_anomalies': 'No anomalies detected.',

        # Recommendations
        'top_recommendations': 'TOP RECOMMENDATIONS:',
        'no_recommendations': 'No actionable recommendations found.',
        'timeline': 'Timeline',
        'expected_impact': 'Impact',

        # Weekly Report
        'weekly_comparison': 'WEEKLY COMPARISON REPORT',
        'last_week': 'Last Week',
        'previous_week': 'Previous Week',
        'change': 'Change',
        'products_sold': 'Products Sold',

        # Transaction Segmentation
        'transaction_segments': 'Transaction Size Segments:',
        'avg_transaction_size': 'Avg Transaction Size',
        'avg_items_per_transaction': 'Avg Items per Transaction',

        # Dashboard
        'dashboard_summary': 'DASHBOARD SUMMARY',
        'key_metrics': 'KEY METRICS:',
        'growth_rate': 'Growth Rate',
        'critical_actions_short': 'CRITICAL ACTIONS:',
        'key_insights': 'KEY INSIGHTS:',
        'inventory_health': 'Inventory Health',
        'dead_stock': 'Dead Stock',

        # Chart/Dashboard Visualizations
        'dashboard_title': 'Executive Business Intelligence Dashboard',
        'kpi_total_revenue': 'Total Revenue',
        'kpi_transactions': 'Transactions',
        'kpi_avg_transaction': 'Avg Transaction',
        'kpi_active_products': 'Active Products',
        'top_revenue_generators_title': 'Top {n} Revenue Generators',
        'revenue_axis': 'Revenue',
        'inventory_health_title': 'Inventory Health Status',
        'healthy_label': 'Healthy',
        'status_hot': 'Hot',
        'status_active': 'Active',
        'status_slowing': 'Slowing',
        'status_cold': 'Cold',
        'status_dead': 'Dead',
        'status_zombie': 'Zombie',
        'alerts_actions_title': 'Alerts & Actions',
        'revenue_by_hour': 'Revenue by Hour',
        'peak_label': 'Peak',
        'hour_of_day': 'Hour of Day',
        'generated_label': 'Generated',
        'pareto_subtitle': '{pct}% of products = {revenue_pct}% of revenue',

        # Trend Analysis
        'trend_analysis_title': 'Business Trend Analysis',
        'revenue_trend': 'Revenue Trend',
        'date_label': 'Date',
        'revenue_label': 'Revenue',
        'moving_average_7d': '7-day MA',
        'daily_transactions_title': 'Daily Transactions',
        'num_transactions': 'Number of Transactions',
        'top_products_weekly': 'Top 5 Products Weekly Performance',
        'week_label': 'Week',
        'avg_revenue_by_dow': 'Average Revenue by Day of Week',
        'day_of_week_label': 'Day of Week',

        # Velocity Matrix
        'velocity_matrix_title': 'Product Velocity Matrix',
        'size_revenue': 'Size = Revenue',
        'units_sold': 'Units Sold',
        'total_revenue_label': 'Total Revenue',
        'quadrant_stars': 'Stars',
        'quadrant_stars_desc': 'High Revenue, High Volume',
        'quadrant_premium': 'Premium',
        'quadrant_premium_desc': 'High Revenue, Low Volume',
        'quadrant_volume': 'Volume',
        'quadrant_volume_desc': 'Low Revenue, High Volume',
        'quadrant_question': 'Question',
        'quadrant_question_desc': 'Low Revenue, Low Volume',
        'product_rank_label': 'Product Rank',

        # Day names
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',

        # Alert Messages
        'alert_dead_inventory_msg': "{count} products haven't sold in {days}+ days",
        'alert_dead_inventory_impact': 'Cash tied up in non-moving inventory',
        'alert_dead_inventory_action': 'Consider liquidation or promotional campaigns',
        'alert_high_concentration_msg': 'Top 20% of products generate {pct}% of revenue',
        'alert_high_concentration_impact': 'High dependency on few products',
        'alert_high_concentration_action': 'Diversify product portfolio',
        'alert_balanced_portfolio_msg': 'Revenue well distributed across products',
        'alert_balanced_portfolio_impact': 'Lower concentration risk',
        'alert_balanced_portfolio_action': 'Maintain current portfolio balance',
        'alert_strong_growth_msg': 'Revenue growing at {pct}%',
        'alert_strong_growth_impact': 'Positive business momentum',
        'alert_strong_growth_action': 'Scale successful initiatives',
        'alert_revenue_decline_msg': 'Revenue declining by {pct}%',
        'alert_revenue_decline_impact': 'Negative business trend',
        'alert_revenue_decline_action': 'Urgent review of sales strategy needed',

        # Recommendation Messages
        'rec_address_decline_title': 'Address Declining Revenue Trend',
        'rec_address_decline_desc': 'Revenue showing downward trend in recent period',
        'rec_address_decline_action': 'Review pricing strategy and launch customer retention campaign',
        'rec_address_decline_impact': 'Stabilize revenue decline',
        'rec_promote_top_title': 'Promote Top Revenue Generators',
        'rec_promote_top_desc': 'Focus marketing on highest performing products',
        'rec_promote_top_action': 'Increase inventory and promotional budget for top products',
        'rec_promote_top_impact': 'Maximize revenue from proven winners',
        'rec_clear_dead_stock_title': 'Clear Dead Stock',
        'rec_clear_dead_stock_desc': '{count} products with no recent sales',
        'rec_clear_dead_stock_action': 'Run clearance promotion or discontinue products',
        'rec_clear_dead_stock_impact': 'Free up capital and warehouse space',
        'priority_high': 'HIGH',
        'priority_medium': 'MEDIUM',
        'priority_low': 'LOW',
        'timeline_immediate': 'Immediate',
        'timeline_1_2_weeks': '1-2 weeks',
        'timeline_monthly': 'Monthly',
    },

    'ESP': {
        # Common
        'customers': 'clientes',
        'customer': 'cliente',
        'products': 'productos',
        'product': 'producto',
        'day': 'día',
        'days': 'días',
        'purchase': 'compra',
        'purchases': 'compras',
        'transactions': 'transacciones',
        'ago': 'atrás',

        # KPIs
        'periods_for_growth': 'Períodos considerados para crecimiento:',
        'previous': 'Anterior',
        'current': 'Actual',
        'growth': 'Crecimiento',
        'revenue': 'Ingresos',
        'total_revenue': 'Ingresos Totales',
        'avg_transaction': 'Transacción Promedio',

        # Alerts
        'critical_actions': 'ACCIONES CRÍTICAS REQUERIDAS:',
        'warnings': 'ADVERTENCIAS:',
        'success_indicators': 'INDICADORES DE ÉXITO:',
        'impact': 'Impacto',
        'action': 'Acción',
        'next_step': 'Siguiente Paso',

        # Pareto
        'top_insight': 'INSIGHT PRINCIPAL',
        'concentration_risk': 'Nivel de Riesgo de Concentración',
        'top_revenue_generators': 'Principales Generadores de Ingresos',
        'top_products': '¡Tus {count} productos principales ({pct}% del catálogo) generan {revenue_pct}% de los ingresos!',
        'pareto_rule': 'Regla 80/20: El Top 20% = {pct}% de ingresos',

        # Inventory
        'inventory_health_score': 'Puntuación de Salud de Inventario',
        'dead_stock_alert': 'Alerta de Producto Sin Movimiento',

        # Peak Times
        'peak_performance': 'Ventanas de Máximo Rendimiento:',
        'best_day': 'Mejor Día',
        'peak_hour': 'Hora Pico',
        'slowest_day': 'Día Más Lento',
        'optimize_staffing': 'Optimizar personal para {day} alrededor de las {hour}',

        # Customer Segmentation
        'champions': 'Campeones',
        'loyal_customers': 'Clientes Leales',
        'recent_customers': 'Clientes Recientes',
        'at_risk': 'En Riesgo',
        'need_attention': 'Necesitan Atención',
        'customer_segmentation': 'Análisis de Segmentación de Clientes/Transacciones',
        'customer_segments': 'Segmentos de Clientes:',
        'total_customers': 'Total de Clientes',
        'avg_recency': 'Recencia Promedio',
        'avg_frequency': 'Frecuencia Promedio',
        'avg_monetary': 'Monetario Promedio',
        'last_purchase': 'Última Compra',
        'rfm_score': 'Puntuación RFM',
        'why_segment': '¿Por qué {segment}?',

        # Detailed Segmentation Report
        'detailed_segmentation_report': 'REPORTE DETALLADO DE SEGMENTACIÓN DE CLIENTES',
        'rfm_explanation_title': 'Entendiendo las Puntuaciones RFM:',
        'rfm_r_label': 'R (Recencia)',
        'rfm_r_desc': 'Qué tan recientemente el cliente compró (días atrás → segmento)',
        'rfm_f_label': 'F (Frecuencia)',
        'rfm_f_desc': 'Con qué frecuencia el cliente compra (cantidad → segmento)',
        'rfm_m_label': 'M (Monetario)',
        'rfm_m_desc': 'Cuánto dinero gasta el cliente (total → segmento)',
        'rfm_quartile_note': 'Los segmentos clasifican clientes: S1 (menor) a S4 (mejor desempeño)',

        # Segment Explanations
        'exp_purchased_recently': 'Compró muy recientemente (nivel superior de recencia)',
        'exp_high_frequency': 'Alta frecuencia de compra (nivel superior de lealtad)',
        'exp_high_spending': 'Alto gasto total (nivel superior de ingresos)',
        'exp_strong_revenue': 'Fuerte contribución de ingresos',
        'exp_regular_customer': 'Cliente regular con pedidos consistentes',
        'exp_building_history': 'Construyendo historial de compras',
        'exp_potential_engagement': 'Potencial para mayor compromiso',
        'exp_not_purchased': 'No ha comprado recientemente (necesita atención)',
        'exp_churn_risk': 'Riesgo de pérdida de cliente',
        'exp_reengagement': 'Recomendado: Campaña de re-compromiso',
        'exp_moderate_engagement': 'Niveles moderados de compromiso',
        'exp_opportunity': 'Oportunidad de mejora',
        'exp_targeted_promo': 'Recomendado: Promociones dirigidas',

        # Forecast
        'revenue_forecast': 'Pronóstico de Ingresos para los próximos {days} días:',
        'daily': 'Diario:',
        'average': 'Promedio',
        'std_dev': 'Desv. Est.',
        'confidence_interval': 'Intervalo de Confianza',
        'total': 'Total:',
        'forecast': 'Pronóstico',
        'trend': 'Tendencia',
        'increasing': 'Creciente',
        'decreasing': 'Decreciente',
        'stable': 'Estable',

        # Cross-sell
        'cross_sell_opportunities': 'Oportunidades de Venta Cruzada:',
        'no_cross_sell': 'No se encontraron oportunidades significativas de venta cruzada.',

        # Anomalies
        'anomalies_detected': 'Anomalías Detectadas:',
        'no_anomalies': 'No se detectaron anomalías.',

        # Recommendations
        'top_recommendations': 'PRINCIPALES RECOMENDACIONES:',
        'no_recommendations': 'No se encontraron recomendaciones accionables.',
        'timeline': 'Cronograma',
        'expected_impact': 'Impacto',

        # Weekly Report
        'weekly_comparison': 'REPORTE DE COMPARACIÓN SEMANAL',
        'last_week': 'Última Semana',
        'previous_week': 'Semana Anterior',
        'change': 'Cambio',
        'products_sold': 'Productos Vendidos',

        # Transaction Segmentation
        'transaction_segments': 'Segmentos de Tamaño de Transacción:',
        'avg_transaction_size': 'Tamaño Promedio de Transacción',
        'avg_items_per_transaction': 'Artículos Promedio por Transacción',

        # Dashboard
        'dashboard_summary': 'RESUMEN DEL DASHBOARD',
        'key_metrics': 'MÉTRICAS CLAVE:',
        'growth_rate': 'Tasa de Crecimiento',
        'critical_actions_short': 'ACCIONES CRÍTICAS:',
        'key_insights': 'INSIGHTS CLAVE:',
        'inventory_health': 'Salud de Inventario',
        'dead_stock': 'Producto Sin Movimiento',

        # Chart/Dashboard Visualizations
        'dashboard_title': 'Dashboard Ejecutivo de Inteligencia de Negocios',
        'kpi_total_revenue': 'Ingresos Totales',
        'kpi_transactions': 'Transacciones',
        'kpi_avg_transaction': 'Transacción Promedio',
        'kpi_active_products': 'Productos Activos',
        'top_revenue_generators_title': 'Top {n} Generadores de Ingresos',
        'revenue_axis': 'Ingresos',
        'inventory_health_title': 'Estado de Salud del Inventario',
        'healthy_label': 'Saludable',
        'status_hot': 'Caliente',
        'status_active': 'Activo',
        'status_slowing': 'Desacelerando',
        'status_cold': 'Frío',
        'status_dead': 'Muerto',
        'status_zombie': 'Zombi',
        'alerts_actions_title': 'Alertas y Acciones',
        'revenue_by_hour': 'Ingresos por Hora',
        'peak_label': 'Pico',
        'hour_of_day': 'Hora del Día',
        'generated_label': 'Generado',
        'pareto_subtitle': '{pct}% de productos = {revenue_pct}% de ingresos',

        # Trend Analysis
        'trend_analysis_title': 'Análisis de Tendencias del Negocio',
        'revenue_trend': 'Tendencia de Ingresos',
        'date_label': 'Fecha',
        'revenue_label': 'Ingresos',
        'moving_average_7d': 'MA 7 días',
        'daily_transactions_title': 'Transacciones Diarias',
        'num_transactions': 'Número de Transacciones',
        'top_products_weekly': 'Desempeño Semanal Top 5 Productos',
        'week_label': 'Semana',
        'avg_revenue_by_dow': 'Ingreso Promedio por Día de la Semana',
        'day_of_week_label': 'Día de la Semana',

        # Velocity Matrix
        'velocity_matrix_title': 'Matriz de Velocidad de Productos',
        'size_revenue': 'Tamaño = Ingresos',
        'units_sold': 'Unidades Vendidas',
        'total_revenue_label': 'Ingresos Totales',
        'quadrant_stars': 'Estrellas',
        'quadrant_stars_desc': 'Altos Ingresos, Alto Volumen',
        'quadrant_premium': 'Premium',
        'quadrant_premium_desc': 'Altos Ingresos, Bajo Volumen',
        'quadrant_volume': 'Volumen',
        'quadrant_volume_desc': 'Bajos Ingresos, Alto Volumen',
        'quadrant_question': 'Interrogante',
        'quadrant_question_desc': 'Bajos Ingresos, Bajo Volumen',
        'product_rank_label': 'Ranking de Productos',

        # Day names
        'monday': 'Lunes',
        'tuesday': 'Martes',
        'wednesday': 'Miércoles',
        'thursday': 'Jueves',
        'friday': 'Viernes',
        'saturday': 'Sábado',
        'sunday': 'Domingo',

        # Alert Messages
        'alert_dead_inventory_msg': "{count} productos no se han vendido en {days}+ días",
        'alert_dead_inventory_impact': 'Capital inmovilizado en inventario sin movimiento',
        'alert_dead_inventory_action': 'Considerar liquidación o campañas promocionales',
        'alert_high_concentration_msg': 'El top 20% de productos genera {pct}% de los ingresos',
        'alert_high_concentration_impact': 'Alta dependencia en pocos productos',
        'alert_high_concentration_action': 'Diversificar portafolio de productos',
        'alert_balanced_portfolio_msg': 'Ingresos bien distribuidos entre productos',
        'alert_balanced_portfolio_impact': 'Menor riesgo de concentración',
        'alert_balanced_portfolio_action': 'Mantener balance actual del portafolio',
        'alert_strong_growth_msg': 'Ingresos creciendo a {pct}%',
        'alert_strong_growth_impact': 'Momentum positivo del negocio',
        'alert_strong_growth_action': 'Escalar iniciativas exitosas',
        'alert_revenue_decline_msg': 'Ingresos decreciendo en {pct}%',
        'alert_revenue_decline_impact': 'Tendencia negativa del negocio',
        'alert_revenue_decline_action': 'Revisión urgente de estrategia de ventas necesaria',

        # Recommendation Messages
        'rec_address_decline_title': 'Atender Tendencia Decreciente de Ingresos',
        'rec_address_decline_desc': 'Ingresos mostrando tendencia a la baja en período reciente',
        'rec_address_decline_action': 'Revisar estrategia de precios y lanzar campaña de retención de clientes',
        'rec_address_decline_impact': 'Estabilizar caída de ingresos',
        'rec_promote_top_title': 'Promover Principales Generadores de Ingresos',
        'rec_promote_top_desc': 'Enfocar marketing en productos de mayor rendimiento',
        'rec_promote_top_action': 'Aumentar inventario y presupuesto promocional para productos top',
        'rec_promote_top_impact': 'Maximizar ingresos de ganadores probados',
        'rec_clear_dead_stock_title': 'Liquidar Inventario Sin Movimiento',
        'rec_clear_dead_stock_desc': '{count} productos sin ventas recientes',
        'rec_clear_dead_stock_action': 'Ejecutar promoción de liquidación o descontinuar productos',
        'rec_clear_dead_stock_impact': 'Liberar capital y espacio en bodega',
        'priority_high': 'ALTA',
        'priority_medium': 'MEDIA',
        'priority_low': 'BAJA',
        'timeline_immediate': 'Inmediato',
        'timeline_1_2_weeks': '1-2 semanas',
        'timeline_monthly': 'Mensual',
    }
}


def get_text(key: str, lang: str = 'ENG', **kwargs) -> str:
    """
    Get translated text for the given key and language

    Args:
        key: Translation key
        lang: Language code ('ENG' or 'ESP')
        **kwargs: Format parameters for string interpolation

    Returns:
        Translated and formatted string
    """
    # Default to English if language not supported
    if lang not in TRANSLATIONS:
        lang = 'ENG'

    # Get translation, fallback to English if key not found
    text = TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['ENG'].get(key, key))

    # Apply formatting if kwargs provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass  # Return unformatted if format fails

    return text


def translate_segment_name(segment: str, lang: str = 'ENG') -> str:
    """Translate segment names"""
    segment_keys = {
        'Champions': 'champions',
        'Loyal Customers': 'loyal_customers',
        'Recent Customers': 'recent_customers',
        'At Risk': 'at_risk',
        'Need Attention': 'need_attention'
    }

    key = segment_keys.get(segment)
    if key:
        return get_text(key, lang)
    return segment


def translate_day_name(day: str, lang: str = 'ENG') -> str:
    """Translate day names"""
    day_keys = {
        'Monday': 'monday',
        'Tuesday': 'tuesday',
        'Wednesday': 'wednesday',
        'Thursday': 'thursday',
        'Friday': 'friday',
        'Saturday': 'saturday',
        'Sunday': 'sunday'
    }

    key = day_keys.get(day)
    if key:
        return get_text(key, lang)
    return day


def translate_status_name(status: str, lang: str = 'ENG') -> str:
    """Translate inventory status names"""
    status_keys = {
        'Hot': 'status_hot',
        'Active': 'status_active',
        'Slowing': 'status_slowing',
        'Cold': 'status_cold',
        'Dead': 'status_dead',
        'Zombie': 'status_zombie'
    }

    key = status_keys.get(status)
    if key:
        return get_text(key, lang)
    return status


# File name suffix translations
FILE_NAME_TRANSLATIONS = {
    'ENG': {
        'quick_summary': 'quick_summary',
        'kpi': 'kpi',
        'alerts': 'alerts',
        'pareto': 'pareto',
        'inventory': 'inventory',
        'peak_times': 'peak_times',
        'executive': 'executive',
        'trend': 'trend',
        'velocity': 'velocity',
        'forecast': 'forecast',
        'cross_selling': 'cross_selling',
        'anomalies': 'anomalies',
        'recommendations': 'recommendations',
        'weekly_compare': 'weekly_compare',
        'customer_segmentation': 'customer_segmentation',
        'detailed_customer_segments': 'detailed_customer_segments',
        'executive_summary': 'executive_summary',
    },
    'ESP': {
        'quick_summary': 'resumen_rapido',
        'kpi': 'kpi',
        'alerts': 'alertas',
        'pareto': 'pareto',
        'inventory': 'inventario',
        'peak_times': 'horas_pico',
        'executive': 'ejecutivo',
        'trend': 'tendencia',
        'velocity': 'velocidad',
        'forecast': 'pronostico',
        'cross_selling': 'venta_cruzada',
        'anomalies': 'anomalias',
        'recommendations': 'recomendaciones',
        'weekly_compare': 'comparacion_semanal',
        'customer_segmentation': 'segmentacion_clientes',
        'detailed_customer_segments': 'segmentos_detallados_clientes',
        'executive_summary': 'resumen_ejecutivo',
    }
}


def get_filename(prefix: str, suffix_key: str, lang: str = 'ENG', extension: str = 'txt') -> str:
    """
    Generate translated filename

    Args:
        prefix: File prefix (BA, AV, DASH, REPORT)
        suffix_key: Key for the file name suffix
        lang: Language code ('ENG' or 'ESP')
        extension: File extension (default 'txt')

    Returns:
        Translated filename like "BA_kpi.txt" or "BA_kpi.txt"

    Example:
        get_filename('BA', 'kpi', 'ESP') -> 'BA_kpi.txt'
        get_filename('AV', 'forecast', 'ESP') -> 'AV_pronostico.txt'
    """
    if lang not in FILE_NAME_TRANSLATIONS:
        lang = 'ENG'

    suffix = FILE_NAME_TRANSLATIONS[lang].get(suffix_key, suffix_key)
    return f"{prefix}_{suffix}.{extension}"
