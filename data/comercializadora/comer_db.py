# Define the product catalog for Comercializadora Al Sur
products = {
    # SUSHI SUPPLIES & ASIAN INGREDIENTS (High margin, steady demand)
    'SUSH001': {'name': 'PANKO ODN BLANCO 1KG', 'cost': 6500, 'price': 8500, 'category': 'sushi_supplies', 'velocity': 'medium', 'popularity': 0.06},
    'SUSH002': {'name': 'PANKO ODN RUBIO 1KG', 'cost': 6500, 'price': 8500, 'category': 'sushi_supplies', 'velocity': 'medium', 'popularity': 0.05},
    'SUSH003': {'name': 'ALGAS NORI PREMIUM 50 HOJAS', 'cost': 8000, 'price': 12000, 'category': 'sushi_supplies', 'velocity': 'medium', 'popularity': 0.04},
    'SUSH004': {'name': 'ARROZ SUSHI KOSHIHIKARI 5KG', 'cost': 12000, 'price': 18000, 'category': 'sushi_supplies', 'velocity': 'high', 'popularity': 0.07},
    'SUSH005': {'name': 'VINAGRE ARROZ MIZKAN 500ML', 'cost': 3500, 'price': 5200, 'category': 'sushi_supplies', 'velocity': 'medium', 'popularity': 0.03},
    'SUSH006': {'name': 'WASABI POLVO PREMIUM 1KG', 'cost': 25000, 'price': 38000, 'category': 'sushi_supplies', 'velocity': 'low', 'popularity': 0.015},
    'SUSH007': {'name': 'JENGIBRE ENCURTIDO 1KG', 'cost': 4500, 'price': 7200, 'category': 'sushi_supplies', 'velocity': 'medium', 'popularity': 0.025},
    'SUSH008': {'name': 'SALSA SOYA KIKKOMAN 1L', 'cost': 3200, 'price': 4800, 'category': 'sushi_supplies', 'velocity': 'high', 'popularity': 0.05},
    'SUSH009': {'name': 'ESTERILLA BAMBU MAKISU', 'cost': 1500, 'price': 2800, 'category': 'sushi_supplies', 'velocity': 'low', 'popularity': 0.01},
    'SUSH010': {'name': 'MISO PASTA SHIROMISO 500G', 'cost': 4800, 'price': 7500, 'category': 'sushi_supplies', 'velocity': 'low', 'popularity': 0.012},
    
    # FRESH SEAFOOD (High velocity, low margin, seasonal peaks)
    'FRESH001': {'name': 'SALMON FRESCO ATLANTICO KG', 'cost': 8500, 'price': 12000, 'category': 'fresh_seafood', 'velocity': 'very_high', 'popularity': 0.12},
    'FRESH002': {'name': 'CONGRIO FRESCO KG', 'cost': 6500, 'price': 9500, 'category': 'fresh_seafood', 'velocity': 'very_high', 'popularity': 0.08},
    'FRESH003': {'name': 'REINETA FRESCA KG', 'cost': 4500, 'price': 7200, 'category': 'fresh_seafood', 'velocity': 'very_high', 'popularity': 0.06},
    'FRESH004': {'name': 'CENTOLLA FRESCA KG', 'cost': 15000, 'price': 22000, 'category': 'fresh_seafood', 'velocity': 'high', 'popularity': 0.02},
    'FRESH005': {'name': 'OSTIONES FRESCOS KG', 'cost': 12000, 'price': 18000, 'category': 'fresh_seafood', 'velocity': 'high', 'popularity': 0.03},
    'FRESH006': {'name': 'MEJILLONES FRESCOS KG', 'cost': 3500, 'price': 5800, 'category': 'fresh_seafood', 'velocity': 'very_high', 'popularity': 0.04},
    'FRESH007': {'name': 'PULPO FRESCO KG', 'cost': 9500, 'price': 14500, 'category': 'fresh_seafood', 'velocity': 'high', 'popularity': 0.025},
    'FRESH008': {'name': 'CAMARONES FRESCOS KG', 'cost': 11000, 'price': 16500, 'category': 'fresh_seafood', 'velocity': 'high', 'popularity': 0.04},
    
    # FROZEN PRODUCTS (Volume drivers, moderate margin)
    'FROZ001': {'name': 'NUGGETS POLLO EMPANADOS 1KG', 'cost': 3200, 'price': 4500, 'category': 'frozen', 'velocity': 'high', 'popularity': 0.08},
    'FROZ002': {'name': 'FINGERS POLLO EMPANADOS 1KG', 'cost': 3500, 'price': 4800, 'category': 'frozen', 'velocity': 'high', 'popularity': 0.06},
    'FROZ003': {'name': 'BARRITAS MERLUZA EMPANADAS 1KG', 'cost': 4200, 'price': 6200, 'category': 'frozen', 'velocity': 'high', 'popularity': 0.07},
    'FROZ004': {'name': 'CALAMARES ANILLAS EMPANADOS 1KG', 'cost': 5500, 'price': 8200, 'category': 'frozen', 'velocity': 'medium', 'popularity': 0.03},
    'FROZ005': {'name': 'SALMON PORCIONES CONGELADO 1KG', 'cost': 7500, 'price': 11200, 'category': 'frozen', 'velocity': 'high', 'popularity': 0.05},
    'FROZ006': {'name': 'LANGOSTINOS PELADOS CONGELADOS 1KG', 'cost': 8800, 'price': 13500, 'category': 'frozen', 'velocity': 'medium', 'popularity': 0.025},
    'FROZ007': {'name': 'PAPAS FRITAS CORTE BASTÓN 2.5KG', 'cost': 2200, 'price': 3200, 'category': 'frozen', 'velocity': 'very_high', 'popularity': 0.09},
    'FROZ008': {'name': 'VERDURAS SALTEADO ORIENTAL 1KG', 'cost': 2800, 'price': 4200, 'category': 'frozen', 'velocity': 'medium', 'popularity': 0.02},
    'FROZ009': {'name': 'GYOZA POLLO CONGELADAS 1KG', 'cost': 4500, 'price': 6800, 'category': 'frozen', 'velocity': 'medium', 'popularity': 0.015},
    'FROZ010': {'name': 'ROLLITOS PRIMAVERA 20 UNIDADES', 'cost': 3200, 'price': 4800, 'category': 'frozen', 'velocity': 'medium', 'popularity': 0.02},
    
    # DRY GOODS & GROCERIES (Steady movers, good margin)
    'DRY001': {'name': 'ACEITE GIRASOL CHEF 5L', 'cost': 4500, 'price': 6500, 'category': 'dry_goods', 'velocity': 'high', 'popularity': 0.05},
    'DRY002': {'name': 'SAL MARINA GRUESA 1KG', 'cost': 800, 'price': 1500, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.03},
    'DRY003': {'name': 'PIMIENTA NEGRA MOLIDA 500G', 'cost': 3500, 'price': 5200, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.02},
    'DRY004': {'name': 'AJO MOLIDO DESHIDRATADO 1KG', 'cost': 6500, 'price': 9500, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.015},
    'DRY005': {'name': 'MAYONESA INDUSTRIAL 3.7KG', 'cost': 3200, 'price': 4800, 'category': 'dry_goods', 'velocity': 'high', 'popularity': 0.04},
    'DRY006': {'name': 'KETCHUP INDUSTRIAL 4KG', 'cost': 2800, 'price': 4200, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.025},
    'DRY007': {'name': 'HARINA TEMPURA ESPECIAL 1KG', 'cost': 2200, 'price': 3500, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.02},
    'DRY008': {'name': 'FÉCULA PAPA INDUSTRIAL 1KG', 'cost': 1800, 'price': 2800, 'category': 'dry_goods', 'velocity': 'low', 'popularity': 0.01},
    'DRY009': {'name': 'CONCENTRADO CALDO POLLO 1KG', 'cost': 4200, 'price': 6200, 'category': 'dry_goods', 'velocity': 'medium', 'popularity': 0.018},
    'DRY010': {'name': 'VINAGRE BLANCO CHEF 1L', 'cost': 1200, 'price': 2000, 'category': 'dry_goods', 'velocity': 'low', 'popularity': 0.012},
    
    # SPECIALTY/SLOW MOVERS (Low velocity, potential dead inventory)
    'SPEC001': {'name': 'SAKE COCINA PREMIUM 750ML', 'cost': 8500, 'price': 14500, 'category': 'specialty', 'velocity': 'very_low', 'popularity': 0.003},
    'SPEC002': {'name': 'ACEITE SESAMO TOSTADO 500ML', 'cost': 6500, 'price': 10200, 'category': 'specialty', 'velocity': 'very_low', 'popularity': 0.004},
    'SPEC003': {'name': 'PASTA MISO ROJO AKAMISO 500G', 'cost': 5500, 'price': 8800, 'category': 'specialty', 'velocity': 'very_low', 'popularity': 0.002},
    'SPEC004': {'name': 'ALGAS WAKAME SECAS 100G', 'cost': 4200, 'price': 7200, 'category': 'specialty', 'velocity': 'very_low', 'popularity': 0.001},
    'SPEC005': {'name': 'SHIITAKE DESHIDRATADOS 500G', 'cost': 12000, 'price': 18500, 'category': 'specialty', 'velocity': 'very_low', 'popularity': 0.0008},
    
    # FAILED/DISCONTINUED ITEMS (Dead inventory candidates)
    'DEAD001': {'name': 'SALSA TERIYAKI MARCA DESCONTINUADA 1L', 'cost': 4500, 'price': 2200, 'category': 'dead_inventory', 'velocity': 'dead', 'popularity': 0.0003},
    'DEAD002': {'name': 'TEMPEH EXPERIMENTAL 500G', 'cost': 3200, 'price': 1500, 'category': 'dead_inventory', 'velocity': 'dead', 'popularity': 0.0002},
    'DEAD003': {'name': 'RAMEN INSTANT PREMIUM VENCIDO', 'cost': 2800, 'price': 800, 'category': 'dead_inventory', 'velocity': 'dead', 'popularity': 0.0001},
    'DEAD004': {'name': 'CONDIMENTO ASIÁTICO CLIENTE CERRADO', 'cost': 5500, 'price': 1800, 'category': 'dead_inventory', 'velocity': 'dead', 'popularity': 0.0001}
}

# Customer segments and locations
customers = {
    # TOP-TIER RESTAURANTS (15 customers, 65% of revenue)
    'R001': {'name': 'SUSHI BAR SAKURA PUCON', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R002': {'name': 'RESTAURANTE ASIAN FUSION VILLARRICA', 'type': 'restaurant_top', 'location': 'Villarrica', 'seasonal': False},
    'R003': {'name': 'HOTEL GRAN PUCON COCINA', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R004': {'name': 'MARISQUERIA EL MUELLE', 'type': 'restaurant_top', 'location': 'Villarrica', 'seasonal': False},
    'R005': {'name': 'SUSHI TOKYO TEMUCO', 'type': 'restaurant_top', 'location': 'Temuco', 'seasonal': False},
    'R006': {'name': 'RESTAURANTE PESCADOS Y MARISCOS', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R007': {'name': 'HOTEL TERMAS RESORT COCINA', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R008': {'name': 'CASINO DREAMS RESTAURANT', 'type': 'restaurant_top', 'location': 'Temuco', 'seasonal': False},
    'R009': {'name': 'SUSHI NIKKEI LICAN RAY', 'type': 'restaurant_top', 'location': 'Lican Ray', 'seasonal': True},
    'R010': {'name': 'PARRILLA DEL LAGO PREMIUM', 'type': 'restaurant_top', 'location': 'Villarrica', 'seasonal': False},
    'R011': {'name': 'RESTAURANTE JAPONÉS KOBE', 'type': 'restaurant_top', 'location': 'Temuco', 'seasonal': False},
    'R012': {'name': 'HOTEL BOUTIQUE COCINA GOURMET', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R013': {'name': 'MARISCOS LA FRONTERA', 'type': 'restaurant_top', 'location': 'Temuco', 'seasonal': False},
    'R014': {'name': 'FUSION RESTAURANT VOLCAN', 'type': 'restaurant_top', 'location': 'Pucón', 'seasonal': True},
    'R015': {'name': 'SUSHI EXPRESS ARAUCANIA', 'type': 'restaurant_top', 'location': 'Temuco', 'seasonal': False},
    
    # MID-TIER BUSINESSES (25 customers shown, total 50, 25% of revenue)
    'B001': {'name': 'CAFE CENTRAL VILLARRICA', 'type': 'business_mid', 'location': 'Villarrica', 'seasonal': False},
    'B002': {'name': 'PIZZERIA ITALIANA PUCON', 'type': 'business_mid', 'location': 'Pucón', 'seasonal': True},
    'B003': {'name': 'FAST FOOD CHICKEN BOX', 'type': 'business_mid', 'location': 'Temuco', 'seasonal': False},
    'B004': {'name': 'CATERING EVENTOS ESPECIALIDAD', 'type': 'business_mid', 'location': 'Villarrica', 'seasonal': False},
    'B005': {'name': 'HOSTAL BACKPACKER COCINA', 'type': 'business_mid', 'location': 'Pucón', 'seasonal': True},
    # ... (additional mid-tier customers would continue B006-B050)
    
    # SMALL CUSTOMERS (10 shown, total 135, 10% of revenue)
    'S001': {'name': 'MINIMARKET DON CARLOS', 'type': 'small', 'location': 'Villarrica', 'seasonal': False},
    'S002': {'name': 'ALMACEN FAMILIAR LAGOS', 'type': 'small', 'location': 'Pucón', 'seasonal': False},
    'S003': {'name': 'CONSUMIDOR INDIVIDUAL RODRIGUEZ', 'type': 'individual', 'location': 'Temuco', 'seasonal': False},
    # ... (additional small customers would continue S004-S135)
}

# Generate additional mid-tier and small customers programmatically
mid_tier_names = [
    'RESTAURANT FAMILIAR', 'CAFE EXPRESS', 'COMIDA RAPIDA', 'CATERING', 'HOSTAL', 'PENSION',
    'BAR RESTAURANT', 'PIZZERIA', 'EMPANADAS', 'SANDWICH', 'COCINA CASERA', 'ALMUERZO'
]

small_names = [
    'MINIMARKET', 'ALMACEN', 'KIOSCO', 'DESPENSA', 'CONSUMIDOR', 'CLIENTE', 'COMPRADOR'
]
