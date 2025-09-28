# Define the product catalog for AutoPartes Chile
products = {
    # HIGH-VOLUME CONSUMABLES (Top revenue drivers - 80/20 rule)
    'OIL001': {'name': 'ACEITE MOTOR 5W30 SINTETICO 4L', 'cost': 12000, 'price': 18000, 'category': 'oil', 'popularity': 0.15},
    'OIL002': {'name': 'ACEITE MOTOR 15W40 MINERAL 4L', 'cost': 8000, 'price': 12000, 'category': 'oil', 'popularity': 0.12},
    'FILT001': {'name': 'FILTRO ACEITE UNIVERSAL', 'cost': 3500, 'price': 6000, 'category': 'filter', 'popularity': 0.10},
    'FILT002': {'name': 'FILTRO AIRE MOTOR UNIVERSAL', 'cost': 4500, 'price': 8000, 'category': 'filter', 'popularity': 0.08},
    'FILT003': {'name': 'FILTRO COMBUSTIBLE DIESEL', 'cost': 5500, 'price': 9500, 'category': 'filter', 'popularity': 0.07},
    'BRAKE001': {'name': 'PASTILLAS FRENO DELANTERAS', 'cost': 15000, 'price': 25000, 'category': 'brake', 'popularity': 0.06},
    'BRAKE002': {'name': 'PASTILLAS FRENO TRASERAS', 'cost': 12000, 'price': 20000, 'category': 'brake', 'popularity': 0.05},
    
    # TIRE SALES (Seasonal - high revenue)
    'TIRE001': {'name': 'NEUMATICO 195/65 R15 VERANO', 'cost': 45000, 'price': 75000, 'category': 'tire', 'popularity': 0.04},
    'TIRE002': {'name': 'NEUMATICO 205/55 R16 VERANO', 'cost': 55000, 'price': 90000, 'category': 'tire', 'popularity': 0.035},
    'TIRE003': {'name': 'NEUMATICO 185/60 R14 INVIERNO', 'cost': 50000, 'price': 85000, 'category': 'tire', 'popularity': 0.03},
    'TIRE004': {'name': 'NEUMATICO 215/60 R17 TODO TERRENO', 'cost': 85000, 'price': 140000, 'category': 'tire', 'popularity': 0.02},
    
    # BATTERIES (Medium volume, good margin)
    'BATT001': {'name': 'BATERIA 12V 60AH AUTO', 'cost': 55000, 'price': 95000, 'category': 'battery', 'popularity': 0.025},
    'BATT002': {'name': 'BATERIA 12V 75AH CAMIONETA', 'cost': 75000, 'price': 125000, 'category': 'battery', 'popularity': 0.02},
    'BATT003': {'name': 'BATERIA 12V 100AH CAMION', 'cost': 120000, 'price': 200000, 'category': 'battery', 'popularity': 0.015},
    
    # ENGINE PARTS (Medium frequency)
    'ENG001': {'name': 'BUJIAS PLATINO SET 4 UNIDADES', 'cost': 25000, 'price': 42000, 'category': 'engine', 'popularity': 0.03},
    'ENG002': {'name': 'CORREA DISTRIBUCION MOTOR', 'cost': 35000, 'price': 60000, 'category': 'engine', 'popularity': 0.02},
    'ENG003': {'name': 'BOMBA AGUA REFRIGERACION', 'cost': 65000, 'price': 110000, 'category': 'engine', 'popularity': 0.015},
    'ENG004': {'name': 'TERMOSTATO MOTOR', 'cost': 15000, 'price': 28000, 'category': 'engine', 'popularity': 0.02},
    
    # SUSPENSION & STEERING
    'SUSP001': {'name': 'AMORTIGUADOR DELANTERO PAR', 'cost': 85000, 'price': 145000, 'category': 'suspension', 'popularity': 0.01},
    'SUSP002': {'name': 'AMORTIGUADOR TRASERO PAR', 'cost': 75000, 'price': 125000, 'category': 'suspension', 'popularity': 0.008},
    'STEER001': {'name': 'ROTULA DIRECCION', 'cost': 25000, 'price': 45000, 'category': 'steering', 'popularity': 0.015},
    'STEER002': {'name': 'CREMALLERA DIRECCION', 'cost': 180000, 'price': 320000, 'category': 'steering', 'popularity': 0.003},
    
    # ELECTRICAL PARTS
    'ELEC001': {'name': 'ALTERNADOR 90A REMANUFACTURADO', 'cost': 85000, 'price': 150000, 'category': 'electrical', 'popularity': 0.008},
    'ELEC002': {'name': 'MOTOR ARRANQUE REMANUFACTURADO', 'cost': 95000, 'price': 165000, 'category': 'electrical', 'popularity': 0.006},
    'ELEC003': {'name': 'FOCO HALOGENO H4 PAR', 'cost': 8000, 'price': 15000, 'category': 'electrical', 'popularity': 0.025},
    'ELEC004': {'name': 'FOCO LED H7 ALTA POTENCIA', 'cost': 35000, 'price': 65000, 'category': 'electrical', 'popularity': 0.01},
    
    # ACCESSORIES & TOOLS
    'ACC001': {'name': 'LLAVE TUERCAS CRUZ 4 PUNTAS', 'cost': 8500, 'price': 15000, 'category': 'tool', 'popularity': 0.012},
    'ACC002': {'name': 'GATO HIDRAULICO 2 TONELADAS', 'cost': 35000, 'price': 65000, 'category': 'tool', 'popularity': 0.005},
    'ACC003': {'name': 'LIQUIDO FRENOS DOT 4 500ML', 'cost': 4500, 'price': 8500, 'category': 'fluid', 'popularity': 0.02},
    'ACC004': {'name': 'REFRIGERANTE MOTOR 5L', 'cost': 8000, 'price': 15000, 'category': 'fluid', 'popularity': 0.015},
    
    # DEAD INVENTORY CANDIDATES (Obsolete/Specialty parts)
    'OLD001': {'name': 'CARBURADOR CLASICO WEBER 32/36', 'cost': 95000, 'price': 180000, 'category': 'obsolete', 'popularity': 0.001},
    'OLD002': {'name': 'REPUESTO RADIO CASSETTE VINTAGE', 'cost': 25000, 'price': 45000, 'category': 'obsolete', 'popularity': 0.0008},
    'RARE001': {'name': 'PIEZA MOTOR ALFA ROMEO CLASICO', 'cost': 150000, 'price': 280000, 'category': 'rare', 'popularity': 0.0005},
    'RARE002': {'name': 'EMBLEMA CROMADO PEUGEOT 504', 'cost': 35000, 'price': 65000, 'category': 'rare', 'popularity': 0.0003},
    'DISC001': {'name': 'FILTRO AIRE MODELO DISCONTINUADO', 'cost': 12000, 'price': 22000, 'category': 'discontinued', 'popularity': 0.002},
    'SPEC001': {'name': 'TURBO COMPRESOR DEPORTIVO', 'cost': 450000, 'price': 750000, 'category': 'specialty', 'popularity': 0.0008},
    'SPEC002': {'name': 'KIT SUSPENSION RACING', 'cost': 320000, 'price': 580000, 'category': 'specialty', 'popularity': 0.0006}
}

# B2B Customers (Repair shops, dealerships, etc.)
customers = [
    'TALLER_MECANICO_SAN_MIGUEL', 'LUBRICENTRO_PROVIDENCIA', 'TALLER_DIESEL_MAIPU',
    'CONCESIONARIO_HONDA', 'MECANICA_RAPIDA_LAS_CONDES', 'TALLER_HERMANOS_LOPEZ',
    'SERVICE_AUTOMOTRIZ_CENTRAL', 'LUBRICADORA_EXPRESS'
]
