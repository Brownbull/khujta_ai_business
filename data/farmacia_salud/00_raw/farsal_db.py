products = {
    # HIGH-VOLUME ESSENTIALS (Top revenue drivers - everyday necessities)
    'MED001': {'name': 'PARACETAMOL 500MG 20 TABLETAS', 'cost': 800, 'price': 1500, 'category': 'analgesic', 'popularity': 0.15},
    'MED002': {'name': 'IBUPROFENO 400MG 30 CAPS', 'cost': 1200, 'price': 2200, 'category': 'analgesic', 'popularity': 0.12},
    'MED003': {'name': 'ASPIRINA 100MG 28 TABLETAS', 'cost': 900, 'price': 1700, 'category': 'analgesic', 'popularity': 0.10},
    'MED004': {'name': 'OMEPRAZOL 20MG 14 CAPS', 'cost': 2500, 'price': 4500, 'category': 'gastric', 'popularity': 0.08},
    'MED005': {'name': 'LORATADINA 10MG 10 TABLETAS', 'cost': 1500, 'price': 2800, 'category': 'allergy', 'popularity': 0.07},
    'VIT001': {'name': 'VITAMINA C 1000MG 30 CAPS', 'cost': 3500, 'price': 6500, 'category': 'vitamin', 'popularity': 0.09},
    'VIT002': {'name': 'MULTIVITAMINICO ADULTO 60 CAPS', 'cost': 5000, 'price': 9000, 'category': 'vitamin', 'popularity': 0.06},
    
    # PRESCRIPTION MEDICATIONS (Medium volume, higher margin)
    'RX001': {'name': 'ATORVASTATINA 20MG 30 TAB', 'cost': 8000, 'price': 15000, 'category': 'prescription', 'popularity': 0.04},
    'RX002': {'name': 'METFORMINA 850MG 60 TAB', 'cost': 6500, 'price': 12000, 'category': 'prescription', 'popularity': 0.035},
    'RX003': {'name': 'LOSARTAN 50MG 28 TAB', 'cost': 7200, 'price': 13500, 'category': 'prescription', 'popularity': 0.03},
    'RX004': {'name': 'LEVOTIROXINA 100MCG 30 TAB', 'cost': 4500, 'price': 8500, 'category': 'prescription', 'popularity': 0.025},
    'RX005': {'name': 'AMLODIPINO 5MG 30 TAB', 'cost': 5500, 'price': 10500, 'category': 'prescription', 'popularity': 0.02},
    
    # SEASONAL PRODUCTS (Flu/Cold season)
    'COLD001': {'name': 'JARABE TOS ADULTO 120ML', 'cost': 2800, 'price': 5200, 'category': 'cold', 'popularity': 0.05},
    'COLD002': {'name': 'ANTIGRIPAL TABLETAS 12 UN', 'cost': 1800, 'price': 3400, 'category': 'cold', 'popularity': 0.04},
    'COLD003': {'name': 'DESCONGESTIONANTE SPRAY NASAL', 'cost': 2200, 'price': 4200, 'category': 'cold', 'popularity': 0.03},
    
    # HEALTH & BEAUTY (Medium popularity)
    'BEAUTY001': {'name': 'PROTECTOR SOLAR FPS 50 120ML', 'cost': 8500, 'price': 15500, 'category': 'beauty', 'popularity': 0.025},
    'BEAUTY002': {'name': 'CREMA HIDRATANTE FACIAL 50ML', 'cost': 6000, 'price': 11000, 'category': 'beauty', 'popularity': 0.02},
    'BEAUTY003': {'name': 'SHAMPOO ANTICASPA 400ML', 'cost': 4500, 'price': 8500, 'category': 'beauty', 'popularity': 0.015},
    'DERM001': {'name': 'CREMA CICATRIZANTE 30G', 'cost': 3500, 'price': 6800, 'category': 'dermatology', 'popularity': 0.01},
    
    # BABY CARE (Niche but steady)
    'BABY001': {'name': 'PAÑALES TALLA M 30 UNIDADES', 'cost': 6500, 'price': 12000, 'category': 'baby', 'popularity': 0.02},
    'BABY002': {'name': 'FORMULA INFANTIL 900G', 'cost': 12000, 'price': 22000, 'category': 'baby', 'popularity': 0.015},
    'BABY003': {'name': 'TOALLITAS HUMEDAS 80 UN', 'cost': 1800, 'price': 3500, 'category': 'baby', 'popularity': 0.025},
    
    # MEDICAL DEVICES & SUPPLIES
    'DEV001': {'name': 'TERMOMETRO DIGITAL', 'cost': 8000, 'price': 15000, 'category': 'device', 'popularity': 0.008},
    'DEV002': {'name': 'TENSIOMETRO AUTOMATICO', 'cost': 25000, 'price': 45000, 'category': 'device', 'popularity': 0.003},
    'SUP001': {'name': 'MASCARILLAS QUIRURGICAS 50 UN', 'cost': 3500, 'price': 6500, 'category': 'supply', 'popularity': 0.02},
    'SUP002': {'name': 'ALCOHOL GEL 500ML', 'cost': 1500, 'price': 2800, 'category': 'supply', 'popularity': 0.03},
    
    # SPECIALTY SUPPLEMENTS (Lower volume)
    'SUPL001': {'name': 'OMEGA 3 1000MG 60 CAPS', 'cost': 8500, 'price': 16000, 'category': 'supplement', 'popularity': 0.01},
    'SUPL002': {'name': 'PROBIOTICOS 30 CAPS', 'cost': 12000, 'price': 22000, 'category': 'supplement', 'popularity': 0.008},
    'SUPL003': {'name': 'COLAGENO HIDROLIZADO 300G', 'cost': 15000, 'price': 28000, 'category': 'supplement', 'popularity': 0.006},
    
    # DEAD INVENTORY CANDIDATES (Specialty/Slow-moving items)
    'SPEC001': {'name': 'HOMEOPATIA ARNICA 30CH', 'cost': 4500, 'price': 8500, 'category': 'homeopathy', 'popularity': 0.002},
    'SPEC002': {'name': 'ACEITE ESENCIAL LAVANDA 10ML', 'cost': 3500, 'price': 7000, 'category': 'aromatherapy', 'popularity': 0.001},
    'OLD001': {'name': 'ANTIGUO JARABE PEDIATRICO DESC', 'cost': 2000, 'price': 4000, 'category': 'discontinued', 'popularity': 0.0008},
    'RARE001': {'name': 'MEDICAMENTO ORFANO ESPECIAL', 'cost': 25000, 'price': 45000, 'category': 'rare', 'popularity': 0.0005},
    'DIET001': {'name': 'BATIDO DIETA PROTEICO 500G', 'cost': 8000, 'price': 15000, 'category': 'diet', 'popularity': 0.003},
    'HERB001': {'name': 'TE HIERBAS DIGESTIVO 20 SOBRES', 'cost': 2500, 'price': 4800, 'category': 'herbal', 'popularity': 0.004}
}

# Pharmacy locations
locations = ['SALUD_PROVIDENCIA', 'SALUD_LAS_CONDES', 'SALUD_MAIPU', 'SALUD_ONLINE']
