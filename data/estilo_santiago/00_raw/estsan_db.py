# Define the product catalog for Estilo Santiago Fashion Boutique
products = {
    # CURRENT SEASON (Autumn/Winter 2024) - TOP PERFORMERS
    'WOM001': {'name': 'BLUSA SEDA MANGA LARGA NEGRA', 'cost': 18000, 'price': 35000, 'category': 'blouse', 'season': 'AW2024', 'popularity': 0.08},
    'WOM002': {'name': 'PANTALON TELA RECTO GRIS', 'cost': 22000, 'price': 42000, 'category': 'pants', 'season': 'AW2024', 'popularity': 0.07},
    'WOM003': {'name': 'VESTIDO MIDI LANA AZUL MARINO', 'cost': 35000, 'price': 65000, 'category': 'dress', 'season': 'AW2024', 'popularity': 0.06},
    'WOM004': {'name': 'CHAQUETA BLAZER CLASICA BEIGE', 'cost': 45000, 'price': 85000, 'category': 'jacket', 'season': 'AW2024', 'popularity': 0.05},
    'WOM005': {'name': 'SWEATER CASHMERE CUELLO V CREMA', 'cost': 55000, 'price': 95000, 'category': 'sweater', 'season': 'AW2024', 'popularity': 0.04},
    
    'MEN001': {'name': 'CAMISA ALGODON MANGA LARGA BLANCA', 'cost': 16000, 'price': 32000, 'category': 'shirt', 'season': 'AW2024', 'popularity': 0.06},
    'MEN002': {'name': 'PANTALON CHINO AZUL MARINO', 'cost': 25000, 'price': 48000, 'category': 'pants', 'season': 'AW2024', 'popularity': 0.05},
    'MEN003': {'name': 'SUETER LANA MERINO GRIS', 'cost': 40000, 'price': 75000, 'category': 'sweater', 'season': 'AW2024', 'popularity': 0.04},
    'MEN004': {'name': 'CHAQUETA CUERO MARRON', 'cost': 85000, 'price': 155000, 'category': 'jacket', 'season': 'AW2024', 'popularity': 0.025},
    
    # ACCESSORIES (Steady sellers)
    'ACC001': {'name': 'BUFANDA LANA ESTAMPADA', 'cost': 8000, 'price': 18000, 'category': 'accessory', 'season': 'AW2024', 'popularity': 0.03},
    'ACC002': {'name': 'CARTERA CUERO NEGRO', 'cost': 35000, 'price': 65000, 'category': 'accessory', 'season': 'AW2024', 'popularity': 0.025},
    'ACC003': {'name': 'COLLAR PERLAS CLASICO', 'cost': 15000, 'price': 32000, 'category': 'accessory', 'season': 'AW2024', 'popularity': 0.02},
    'ACC004': {'name': 'CINTURON CUERO CAFE', 'cost': 12000, 'price': 25000, 'category': 'accessory', 'season': 'AW2024', 'popularity': 0.025},
    
    # SHOES (Medium performers)
    'SHOE001': {'name': 'ZAPATO TACON MEDIO NEGRO', 'cost': 45000, 'price': 85000, 'category': 'shoes', 'season': 'AW2024', 'popularity': 0.02},
    'SHOE002': {'name': 'BOTA CUERO HASTA RODILLA', 'cost': 65000, 'price': 125000, 'category': 'shoes', 'season': 'AW2024', 'popularity': 0.015},
    'SHOE003': {'name': 'ZAPATO OXFORD HOMBRE CAFE', 'cost': 55000, 'price': 105000, 'category': 'shoes', 'season': 'AW2024', 'popularity': 0.01},
    
    # PREVIOUS SEASON ITEMS (Spring/Summer 2024) - CLEARANCE/DEAD INVENTORY
    'OLD001': {'name': 'VESTIDO FLORAL MANGA CORTA', 'cost': 25000, 'price': 15000, 'category': 'dress', 'season': 'SS2024', 'popularity': 0.008},
    'OLD002': {'name': 'SHORT LINO BLANCO MUJER', 'cost': 18000, 'price': 12000, 'category': 'shorts', 'season': 'SS2024', 'popularity': 0.006},
    'OLD003': {'name': 'CAMISA HAWAIANA HOMBRE', 'cost': 20000, 'price': 14000, 'category': 'shirt', 'season': 'SS2024', 'popularity': 0.004},
    'OLD004': {'name': 'SANDALIAS PLATAFORMA DORADAS', 'cost': 35000, 'price': 22000, 'category': 'shoes', 'season': 'SS2024', 'popularity': 0.003},
    'OLD005': {'name': 'BIKINI DOS PIEZAS ESTAMPADO', 'cost': 15000, 'price': 8000, 'category': 'swimwear', 'season': 'SS2024', 'popularity': 0.002},
    
    # VERY OLD INVENTORY (Autumn/Winter 2023) - DEEP DISCOUNT DEAD INVENTORY
    'DEAD001': {'name': 'ABRIGO LANA OVERSIZED 2023', 'cost': 75000, 'price': 25000, 'category': 'coat', 'season': 'AW2023', 'popularity': 0.001},
    'DEAD002': {'name': 'BOTAS LLUVIA ESTILO RETRO', 'cost': 40000, 'price': 18000, 'category': 'shoes', 'season': 'AW2023', 'popularity': 0.0008},
    'DEAD003': {'name': 'SUETER PATRON GEOMETRICO VINTAGE', 'cost': 30000, 'price': 12000, 'category': 'sweater', 'season': 'AW2023', 'popularity': 0.0006},
    'DEAD004': {'name': 'PANTALON PATA ELEFANTE RETRO', 'cost': 28000, 'price': 10000, 'category': 'pants', 'season': 'AW2023', 'popularity': 0.0004},
    
    # LUXURY/SPECIALTY ITEMS (Low volume, high margin)
    'LUX001': {'name': 'VESTIDO SEDA DISEÑADOR LIMITADO', 'cost': 120000, 'price': 220000, 'category': 'dress', 'season': 'AW2024', 'popularity': 0.002},
    'LUX002': {'name': 'ABRIGO CACHEMIRA ITALIANA', 'cost': 200000, 'price': 380000, 'category': 'coat', 'season': 'AW2024', 'popularity': 0.001},
    'LUX003': {'name': 'ZAPATOS CUERO HECHOS A MANO', 'cost': 150000, 'price': 280000, 'category': 'shoes', 'season': 'AW2024', 'popularity': 0.0008},
    
    # FAILED EXPERIMENTS (Items that didn't sell)
    'FAIL001': {'name': 'CAMISETA MENSAJE FILOSOFICO', 'cost': 8000, 'price': 5000, 'category': 'tshirt', 'season': 'AW2024', 'popularity': 0.0003},
    'FAIL002': {'name': 'SOMBRERO FEDORA NEON', 'cost': 15000, 'price': 8000, 'category': 'accessory', 'season': 'SS2024', 'popularity': 0.0002},
    'FAIL003': {'name': 'PONCHO ALPACA MULTICOLOR', 'cost': 45000, 'price': 20000, 'category': 'outerwear', 'season': 'AW2024', 'popularity': 0.0001}
}

# Fashion boutique locations
locations = ['ESTILO_PROVIDENCIA', 'ESTILO_LAS_CONDES', 'ESTILO_ONLINE']
