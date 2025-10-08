# Define the product catalog for Cerveza Artesanal Los Andes
products = {
    # CORE BEER LINEUP (Top revenue drivers - consistent sellers)
    'BEER001': {'name': 'IPA LUPULO AMERICANO 330ML', 'cost': 1800, 'price': 3500, 'category': 'beer_core', 'abv': 6.2, 'popularity': 0.18},
    'BEER002': {'name': 'LAGER PREMIUM CRISTALINA 330ML', 'cost': 1200, 'price': 2800, 'category': 'beer_core', 'abv': 4.8, 'popularity': 0.15},
    'BEER003': {'name': 'PORTER CHOCOLATE NEGRO 330ML', 'cost': 2000, 'price': 3800, 'category': 'beer_core', 'abv': 5.5, 'popularity': 0.12},
    'BEER004': {'name': 'WHEAT BEER TRIGO SUAVE 330ML', 'cost': 1500, 'price': 3200, 'category': 'beer_core', 'abv': 5.0, 'popularity': 0.10},
    'BEER005': {'name': 'PALE ALE CITRICA 330ML', 'cost': 1600, 'price': 3300, 'category': 'beer_core', 'abv': 5.8, 'popularity': 0.08},
    
    # SEASONAL BEERS (Limited time, higher margin)
    'SEAS001': {'name': 'CERVEZA CALABAZA OTOÑO 330ML', 'cost': 2200, 'price': 4200, 'category': 'beer_seasonal', 'abv': 6.0, 'popularity': 0.05},
    'SEAS002': {'name': 'STOUT INVIERNO ESPECIADO 330ML', 'cost': 2500, 'price': 4500, 'category': 'beer_seasonal', 'abv': 7.2, 'popularity': 0.04},
    'SEAS003': {'name': 'CERVEZA MIEL PRIMAVERA 330ML', 'cost': 2300, 'price': 4300, 'category': 'beer_seasonal', 'abv': 5.5, 'popularity': 0.03},
    'SEAS004': {'name': 'CERVEZA FRUTAS VERANO 330ML', 'cost': 2400, 'price': 4400, 'category': 'beer_seasonal', 'abv': 4.5, 'popularity': 0.025},
    
    # DRAFT/TAP ONLY (Taproom exclusive)
    'TAP001': {'name': 'IPA FRESCA BARRIL 500ML', 'cost': 2200, 'price': 4500, 'category': 'beer_tap', 'abv': 6.2, 'popularity': 0.06},
    'TAP002': {'name': 'LAGER BARRIL PREMIUM 500ML', 'cost': 1800, 'price': 3800, 'category': 'beer_tap', 'abv': 4.8, 'popularity': 0.05},
    'TAP003': {'name': 'CERVEZA EXPERIMENTAL BARRIL 500ML', 'cost': 2800, 'price': 5500, 'category': 'beer_tap', 'abv': 8.0, 'popularity': 0.02},
    
    # FOOD MENU (Taproom pairing)
    'FOOD001': {'name': 'TABLA QUESOS ARTESANALES', 'cost': 8500, 'price': 16000, 'category': 'food', 'abv': 0, 'popularity': 0.04},
    'FOOD002': {'name': 'SANDWICH PULLED PORK BBQ', 'cost': 6500, 'price': 12500, 'category': 'food', 'abv': 0, 'popularity': 0.035},
    'FOOD003': {'name': 'NACHOS BREWERY ESPECIALES', 'cost': 4500, 'price': 9500, 'category': 'food', 'abv': 0, 'popularity': 0.03},
    'FOOD004': {'name': 'PRETZELS CASEROS CON DIP', 'cost': 3000, 'price': 6500, 'category': 'food', 'abv': 0, 'popularity': 0.025},
    'FOOD005': {'name': 'ALITAS BUFFALO PICANTES', 'cost': 7500, 'price': 14000, 'category': 'food', 'abv': 0, 'popularity': 0.02},
    
    # MERCHANDISE (Brand building)
    'MERCH001': {'name': 'CAMISETA LOGO BREWERY NEGRA', 'cost': 8000, 'price': 18000, 'category': 'merchandise', 'abv': 0, 'popularity': 0.015},
    'MERCH002': {'name': 'GORRO TRUCKER LOGO BORDADO', 'cost': 6000, 'price': 14000, 'category': 'merchandise', 'abv': 0, 'popularity': 0.01},
    'MERCH003': {'name': 'VASO CERVEZA VIDRIO GRABADO', 'cost': 4500, 'price': 12000, 'category': 'merchandise', 'abv': 0, 'popularity': 0.012},
    'MERCH004': {'name': 'ABREBOTELLAS METALICO LOGO', 'cost': 2500, 'price': 7500, 'category': 'merchandise', 'abv': 0, 'popularity': 0.008},
    
    # MIXED PACKS (Gift/sampler sets)
    'PACK001': {'name': 'PACK DEGUSTACION 6 CERVEZAS', 'cost': 9000, 'price': 18000, 'category': 'beer_pack', 'abv': 5.5, 'popularity': 0.02},
    'PACK002': {'name': 'PACK REGALO CERVEZA + VASO', 'cost': 6000, 'price': 14500, 'category': 'beer_pack', 'abv': 6.0, 'popularity': 0.015},
    
    # FAILED EXPERIMENTS (Dead inventory candidates)
    'FAIL001': {'name': 'CERVEZA CHILE HABANERO 330ML', 'cost': 2500, 'price': 2000, 'category': 'beer_experimental', 'abv': 6.5, 'popularity': 0.003},
    'FAIL002': {'name': 'SOUR BEER PICKLE EXTREMO 330ML', 'cost': 3000, 'price': 2200, 'category': 'beer_experimental', 'abv': 4.2, 'popularity': 0.002},
    'FAIL003': {'name': 'CERVEZA CAFE AMARGO 330ML', 'cost': 2800, 'price': 2500, 'category': 'beer_experimental', 'abv': 7.0, 'popularity': 0.001},
    
    # OLD SEASONAL (Past season inventory)
    'OLD001': {'name': 'CERVEZA NAVIDAD 2023 330ML', 'cost': 2200, 'price': 1800, 'category': 'beer_old', 'abv': 6.8, 'popularity': 0.002},
    'OLD002': {'name': 'OKTOBERFEST ESPECIAL 2023 330ML', 'cost': 2000, 'price': 1500, 'category': 'beer_old', 'abv': 5.9, 'popularity': 0.001},
    
    # SPECIALTY HIGH-END (Limited production)
    'SPEC001': {'name': 'IMPERIAL STOUT BARRICA WHISKY 330ML', 'cost': 4500, 'price': 9500, 'category': 'beer_specialty', 'abv': 11.0, 'popularity': 0.004},
    'SPEC002': {'name': 'SOUR WILD FERMENTATION 330ML', 'cost': 4000, 'price': 8500, 'category': 'beer_specialty', 'abv': 6.8, 'popularity': 0.003}
}

# Sales channels
channels = ['TAPROOM_DIRECT', 'DISTRIBUTOR_B2B', 'ONLINE_DELIVERY']

# B2B customers (bars, restaurants)
b2b_customers = [
    'BAR_PROVIDENCIA', 'RESTAURANT_VITACURA', 'PUB_LAS_CONDES', 'BEER_SHOP_SANTIAGO',
    'RESTAURANT_BELLAVISTA', 'BAR_ÑUÑOA', 'CERVECERIA_INDEPENDENT'
]
