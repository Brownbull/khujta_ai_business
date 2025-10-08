# Define the product catalog for TechnoMax Electronics
products = {
    # HIGH-VALUE, LOW-VOLUME (Top revenue generators - 80/20 rule)
    'SMART001': {'name': 'IPHONE 15 PRO MAX 256GB', 'cost': 800000, 'price': 1200000, 'category': 'smartphone', 'popularity': 0.12},
    'SMART002': {'name': 'SAMSUNG GALAXY S24 ULTRA', 'cost': 750000, 'price': 1100000, 'category': 'smartphone', 'popularity': 0.10},
    'SMART003': {'name': 'IPHONE 15 REGULAR 128GB', 'cost': 650000, 'price': 950000, 'category': 'smartphone', 'popularity': 0.08},
    'LAP001': {'name': 'MACBOOK AIR M3 13 PULGADAS', 'cost': 900000, 'price': 1350000, 'category': 'laptop', 'popularity': 0.06},
    'LAP002': {'name': 'LENOVO THINKPAD X1 CARBON', 'cost': 850000, 'price': 1250000, 'category': 'laptop', 'popularity': 0.05},
    'LAP003': {'name': 'ASUS ROG GAMING LAPTOP', 'cost': 1100000, 'price': 1600000, 'category': 'laptop', 'popularity': 0.04},
    'TV001': {'name': 'SAMSUNG QLED 55 PULGADAS 4K', 'cost': 600000, 'price': 900000, 'category': 'tv', 'popularity': 0.03},
    'TV002': {'name': 'LG OLED 65 PULGADAS HDR', 'cost': 1000000, 'price': 1450000, 'category': 'tv', 'popularity': 0.02},
    
    # MEDIUM-VALUE PRODUCTS (Good sellers)
    'TAB001': {'name': 'IPAD AIR 10.9 WIFI 64GB', 'cost': 350000, 'price': 520000, 'category': 'tablet', 'popularity': 0.05},
    'TAB002': {'name': 'SAMSUNG GALAXY TAB A8', 'cost': 180000, 'price': 280000, 'category': 'tablet', 'popularity': 0.04},
    'GAME001': {'name': 'PLAYSTATION 5 CONSOLA', 'cost': 400000, 'price': 600000, 'category': 'gaming', 'popularity': 0.03},
    'GAME002': {'name': 'NINTENDO SWITCH OLED', 'cost': 250000, 'price': 380000, 'category': 'gaming', 'popularity': 0.025},
    'AUDIO001': {'name': 'AIRPODS PRO 2DA GEN', 'cost': 180000, 'price': 280000, 'category': 'audio', 'popularity': 0.04},
    'AUDIO002': {'name': 'SONY WH-1000XM5 HEADPHONES', 'cost': 220000, 'price': 350000, 'category': 'audio', 'popularity': 0.03},
    
    # HIGH-VOLUME, LOW-VALUE (Accessories - high frequency)
    'ACC001': {'name': 'CABLE USB-C LIGHTNING 1M', 'cost': 8000, 'price': 15000, 'category': 'accessory', 'popularity': 0.08},
    'ACC002': {'name': 'CARGADOR INALAMBRICO RAPIDO', 'cost': 15000, 'price': 28000, 'category': 'accessory', 'popularity': 0.06},
    'ACC003': {'name': 'FUNDA SILICONA IPHONE 15', 'cost': 5000, 'price': 12000, 'category': 'accessory', 'popularity': 0.05},
    'ACC004': {'name': 'PROTECTOR PANTALLA TEMPERED', 'cost': 3000, 'price': 8000, 'category': 'accessory', 'popularity': 0.07},
    'ACC005': {'name': 'CABLE HDMI 4K 2 METROS', 'cost': 12000, 'price': 22000, 'category': 'accessory', 'popularity': 0.04},
    'ACC006': {'name': 'MOUSE GAMING RGB LOGITECH', 'cost': 35000, 'price': 65000, 'category': 'accessory', 'popularity': 0.03},
    'ACC007': {'name': 'TECLADO MECANICO CORSAIR', 'cost': 80000, 'price': 145000, 'category': 'accessory', 'popularity': 0.02},
    
    # STORAGE & COMPONENTS
    'STOR001': {'name': 'SSD SAMSUNG 1TB EXTERNO', 'cost': 80000, 'price': 140000, 'category': 'storage', 'popularity': 0.025},
    'STOR002': {'name': 'MICRO SD 128GB SANDISK', 'cost': 25000, 'price': 45000, 'category': 'storage', 'popularity': 0.03},
    'COMP001': {'name': 'RAM DDR4 16GB CORSAIR', 'cost': 60000, 'price': 110000, 'category': 'component', 'popularity': 0.015},
    
    # DEAD INVENTORY CANDIDATES (Specialty/Outdated items)
    'OLD001': {'name': 'IPHONE 12 MINI 64GB REACONDICIONADO', 'cost': 300000, 'price': 450000, 'category': 'smartphone', 'popularity': 0.005},
    'OLD002': {'name': 'LAPTOP HP CELERON 4GB REFURB', 'cost': 200000, 'price': 320000, 'category': 'laptop', 'popularity': 0.003},
    'SPEC001': {'name': 'CAMARA ACCION GOPRO HERO 8', 'cost': 180000, 'price': 280000, 'category': 'camera', 'popularity': 0.002},
    'SPEC002': {'name': 'DRONE DJI MINI SE', 'cost': 250000, 'price': 380000, 'category': 'drone', 'popularity': 0.001},
    'SPEC003': {'name': 'VR HEADSET META QUEST 2', 'cost': 300000, 'price': 450000, 'category': 'vr', 'popularity': 0.0008},
    'LEGACY001': {'name': 'DVD PLAYER SAMSUNG BASICO', 'cost': 25000, 'price': 45000, 'category': 'legacy', 'popularity': 0.0005},
    'LEGACY002': {'name': 'RADIO AM/FM PORTABLE SONY', 'cost': 15000, 'price': 30000, 'category': 'legacy', 'popularity': 0.0003}
}

# Stores
stores = ['TECHNOMAX_MALL_COSTANERA', 'TECHNOMAX_PROVIDENCIA', 'TECHNOMAX_ONLINE']
