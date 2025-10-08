# Define the product catalog for Libros & Más
products = {
    # CURRENT TEXTBOOKS (High demand, high price, semester-driven)
    'TEXT001': {'name': 'CALCULO DIFERENCIAL STEWART ED.2024', 'cost': 45000, 'price': 78000, 'category': 'textbook_current', 'subject': 'mathematics', 'popularity': 0.08},
    'TEXT002': {'name': 'FISICA UNIVERSITARIA SEARS ED.2024', 'cost': 52000, 'price': 89000, 'category': 'textbook_current', 'subject': 'physics', 'popularity': 0.07},
    'TEXT003': {'name': 'QUIMICA GENERAL CHANG ED.2024', 'cost': 48000, 'price': 82000, 'category': 'textbook_current', 'subject': 'chemistry', 'popularity': 0.06},
    'TEXT004': {'name': 'CONTABILIDAD FINANCIERA HORNGREN ED.2024', 'cost': 42000, 'price': 72000, 'category': 'textbook_current', 'subject': 'business', 'popularity': 0.055},
    'TEXT005': {'name': 'PSICOLOGIA COGNITIVA STERNBERG ED.2024', 'cost': 38000, 'price': 65000, 'category': 'textbook_current', 'subject': 'psychology', 'popularity': 0.05},
    'TEXT006': {'name': 'DERECHO CIVIL ALESSANDRI ED.2024', 'cost': 55000, 'price': 95000, 'category': 'textbook_current', 'subject': 'law', 'popularity': 0.04},
    
    # POPULAR FICTION & NON-FICTION (General public, steady sellers)
    'BOOK001': {'name': 'BESTSELLER NOVELA CONTEMPORANEA', 'cost': 8000, 'price': 16000, 'category': 'fiction', 'subject': 'literature', 'popularity': 0.06},
    'BOOK002': {'name': 'BIOGRAFIA PERSONAJE HISTORICO', 'cost': 12000, 'price': 22000, 'category': 'biography', 'subject': 'history', 'popularity': 0.04},
    'BOOK003': {'name': 'LIBRO AUTOAYUDA MOTIVACIONAL', 'cost': 7500, 'price': 15000, 'category': 'selfhelp', 'subject': 'psychology', 'popularity': 0.045},
    'BOOK004': {'name': 'NOVELA FANTASIA JUVENIL', 'cost': 9000, 'price': 18000, 'category': 'fiction', 'subject': 'literature', 'popularity': 0.035},
    'BOOK005': {'name': 'ENSAYO FILOSOFIA MODERNA', 'cost': 14000, 'price': 26000, 'category': 'philosophy', 'subject': 'philosophy', 'popularity': 0.02},
    
    # STATIONERY & SUPPLIES (High volume, low margin, consistent demand)
    'STAT001': {'name': 'CUADERNO UNIVERSITARIO 100 HOJAS', 'cost': 1200, 'price': 2500, 'category': 'stationery', 'subject': 'supplies', 'popularity': 0.12},
    'STAT002': {'name': 'LAPICES GRAFITO CAJA 12 UNIDADES', 'cost': 800, 'price': 1800, 'category': 'stationery', 'subject': 'supplies', 'popularity': 0.08},
    'STAT003': {'name': 'CARPETA ARCHIVADOR TAMAÑO CARTA', 'cost': 2500, 'price': 4500, 'category': 'stationery', 'subject': 'supplies', 'popularity': 0.06},
    'STAT004': {'name': 'CALCULADORA CIENTIFICA CASIO', 'cost': 18000, 'price': 32000, 'category': 'calculator', 'subject': 'supplies', 'popularity': 0.025},
    'STAT005': {'name': 'RESALTADORES COLORES SET 6', 'cost': 1500, 'price': 3200, 'category': 'stationery', 'subject': 'supplies', 'popularity': 0.05},
    'STAT006': {'name': 'MOCHILA UNIVERSITARIA RESISTENTE', 'cost': 15000, 'price': 28000, 'category': 'backpack', 'subject': 'supplies', 'popularity': 0.015},
    
    # REFERENCE BOOKS (Steady demand, professional market)
    'REF001': {'name': 'DICCIONARIO RAE ESPAÑOL COMPLETO', 'cost': 25000, 'price': 45000, 'category': 'reference', 'subject': 'language', 'popularity': 0.015},
    'REF002': {'name': 'ATLAS GEOGRAFICO MUNDIAL', 'cost': 20000, 'price': 38000, 'category': 'reference', 'subject': 'geography', 'popularity': 0.01},
    'REF003': {'name': 'CODIGO CIVIL ACTUALIZADO 2024', 'cost': 18000, 'price': 32000, 'category': 'reference', 'subject': 'law', 'popularity': 0.012},
    
    # GIFT BOOKS & COFFEE TABLE (Seasonal, gift-driven)
    'GIFT001': {'name': 'LIBRO FOTOGRAFIA CHILE PAISAJES', 'cost': 22000, 'price': 42000, 'category': 'coffee_table', 'subject': 'photography', 'popularity': 0.008},
    'GIFT002': {'name': 'RECETARIO COCINA CHILENA TRADICIONAL', 'cost': 16000, 'price': 30000, 'category': 'cookbook', 'subject': 'cooking', 'popularity': 0.012},
    'GIFT003': {'name': 'AGENDA EJECUTIVA TAPA DURA 2024', 'cost': 8000, 'price': 18000, 'category': 'agenda', 'subject': 'supplies', 'popularity': 0.02},
    
    # OLD TEXTBOOK EDITIONS (Dead inventory - previous editions)
    'OLD001': {'name': 'CALCULO DIFERENCIAL STEWART ED.2022', 'cost': 45000, 'price': 25000, 'category': 'textbook_old', 'subject': 'mathematics', 'popularity': 0.005},
    'OLD002': {'name': 'FISICA UNIVERSITARIA SEARS ED.2021', 'cost': 52000, 'price': 20000, 'category': 'textbook_old', 'subject': 'physics', 'popularity': 0.003},
    'OLD003': {'name': 'CONTABILIDAD FINANCIERA ED.2020', 'cost': 42000, 'price': 18000, 'category': 'textbook_old', 'subject': 'business', 'popularity': 0.002},
    'OLD004': {'name': 'DERECHO CIVIL EDICION DESCONTINUADA', 'cost': 55000, 'price': 15000, 'category': 'textbook_old', 'subject': 'law', 'popularity': 0.001},
    
    # SPECIALTY/NICHE BOOKS (Low volume, specialized)
    'SPEC001': {'name': 'TRATADO FILOSOFIA MEDIEVAL LATINA', 'cost': 35000, 'price': 65000, 'category': 'specialty', 'subject': 'philosophy', 'popularity': 0.002},
    'SPEC002': {'name': 'MANUAL BOTANICA FLORA CHILENA', 'cost': 28000, 'price': 52000, 'category': 'specialty', 'subject': 'biology', 'popularity': 0.0015},
    'SPEC003': {'name': 'ARQUEOLOGIA PRECOLOMBINA ANDES', 'cost': 32000, 'price': 58000, 'category': 'specialty', 'subject': 'archaeology', 'popularity': 0.001},
    
    # FAILED TITLES (Books that didn't sell, clearance)
    'FAIL001': {'name': 'NOVELA AUTOPAUBLICADA DESCONOCIDA', 'cost': 8000, 'price': 4000, 'category': 'fiction_failed', 'subject': 'literature', 'popularity': 0.0008},
    'FAIL002': {'name': 'MANUAL TECNOLOGIA OBSOLETA', 'cost': 25000, 'price': 8000, 'category': 'technical_failed', 'subject': 'technology', 'popularity': 0.0005},
    'FAIL003': {'name': 'LIBRO DIETA MODA PASAJERA', 'cost': 12000, 'price': 5000, 'category': 'health_failed', 'subject': 'health', 'popularity': 0.0003}
}

# Store locations
locations = ['LIBROS_UNIVERSIDAD', 'LIBROS_CENTRO', 'LIBROS_ONLINE']

# Customer types
customer_types = ['ESTUDIANTE', 'PROFESIONAL', 'GENERAL', 'PROFESOR']