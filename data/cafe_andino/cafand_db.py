# Define the product catalog for Café Andino
products = {
    # Coffee Drinks (High performers - 80/20 rule)
    'CAF001': {'name': 'AMERICANO REGULAR', 'cost': 800, 'price': 1800, 'category': 'coffee', 'popularity': 0.25},
    'CAF002': {'name': 'CAPPUCCINO GRANDE', 'cost': 900, 'price': 2200, 'category': 'coffee', 'popularity': 0.20},
    'CAF003': {'name': 'LATTE REGULAR', 'cost': 850, 'price': 2000, 'category': 'coffee', 'popularity': 0.18},
    'CAF004': {'name': 'ESPRESSO DOBLE', 'cost': 600, 'price': 1500, 'category': 'coffee', 'popularity': 0.15},
    'CAF005': {'name': 'MOCHA CHOCOLATE', 'cost': 1000, 'price': 2500, 'category': 'coffee', 'popularity': 0.08},
    
    # Cold Drinks
    'BEB001': {'name': 'FRAPPUCCINO VAINILLA', 'cost': 1200, 'price': 2800, 'category': 'cold', 'popularity': 0.06},
    'BEB002': {'name': 'SMOOTHIE FRUTILLA', 'cost': 1100, 'price': 2600, 'category': 'cold', 'popularity': 0.04},
    'BEB003': {'name': 'TE HELADO LIMON', 'cost': 700, 'price': 1600, 'category': 'cold', 'popularity': 0.03},
    
    # Hot Teas
    'TE001': {'name': 'TE VERDE JASMIN', 'cost': 500, 'price': 1400, 'category': 'tea', 'popularity': 0.02},
    'TE002': {'name': 'TE NEGRO EARL GREY', 'cost': 550, 'price': 1500, 'category': 'tea', 'popularity': 0.015},
    'TE003': {'name': 'INFUSION MANZANILLA', 'cost': 400, 'price': 1200, 'category': 'tea', 'popularity': 0.01},
    
    # Pastries (Medium performers)
    'PAN001': {'name': 'CROISSANT MANTEQUILLA', 'cost': 600, 'price': 1500, 'category': 'pastry', 'popularity': 0.05},
    'PAN002': {'name': 'MUFFIN ARANDANOS', 'cost': 700, 'price': 1800, 'category': 'pastry', 'popularity': 0.04},
    'PAN003': {'name': 'MEDIALUNAS DULCES', 'cost': 500, 'price': 1200, 'category': 'pastry', 'popularity': 0.03},
    'PAN004': {'name': 'BROWNIE CHOCOLATE', 'cost': 800, 'price': 2000, 'category': 'pastry', 'popularity': 0.025},
    
    # Sandwiches
    'SAN001': {'name': 'SANDWICH PALTA PAVO', 'cost': 1500, 'price': 3500, 'category': 'sandwich', 'popularity': 0.03},
    'SAN002': {'name': 'SANDWICH ITALIANO', 'cost': 1400, 'price': 3200, 'category': 'sandwich', 'popularity': 0.025},
    'SAN003': {'name': 'TOSTADO JAMON QUESO', 'cost': 1200, 'price': 2800, 'category': 'sandwich', 'popularity': 0.02},
    
    # Salads
    'SAL001': {'name': 'ENSALADA CESAR POLLO', 'cost': 1800, 'price': 4200, 'category': 'salad', 'popularity': 0.015},
    'SAL002': {'name': 'ENSALADA QUINOA', 'cost': 1600, 'price': 3800, 'category': 'salad', 'popularity': 0.01},
    
    # Specialty/Seasonal (Low performers - potential dead inventory)
    'ESP001': {'name': 'CAFE TURCO ESPECIAL', 'cost': 1000, 'price': 2800, 'category': 'specialty', 'popularity': 0.005},
    'ESP002': {'name': 'CHAI LATTE ESPECIAS', 'cost': 900, 'price': 2400, 'category': 'specialty', 'popularity': 0.003},
    'ESP003': {'name': 'MATCHA LATTE PREMIUM', 'cost': 1300, 'price': 3200, 'category': 'specialty', 'popularity': 0.002},
    'EST001': {'name': 'CHOCOLATE CALIENTE NAVIDAD', 'cost': 800, 'price': 2200, 'category': 'seasonal', 'popularity': 0.001},
    'EST002': {'name': 'LIMONADA ROSA VERANO', 'cost': 600, 'price': 1800, 'category': 'seasonal', 'popularity': 0.0005},
}

# Locations
locations = ['ANDINO_PROVIDENCIA', 'ANDINO_LAS_CONDES', 'ANDINO_VITACURA']
