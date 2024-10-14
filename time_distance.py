# time_distance.py

# Dictionary mapping routes to (time, distance) tuples
routes = {
    ('Recife (PE)', 'Florianopolis (SC)'): (1.76, 676.53),
    ('Florianopolis (SC)', 'Recife (PE)'): (1.76, 676.53),
    ('Brasilia (DF)', 'Florianopolis (SC)'): (1.66, 637.56),
    ('Florianopolis (SC)', 'Brasilia (DF)'): (1.66, 637.56),
    ('Aracaju (SE)', 'Salvador (BH)'): (2.16, 830.86),
    ('Salvador (BH)', 'Aracaju (SE)'): (2.16, 830.86),
    ('Aracaju (SE)', 'Campo Grande (MS)'): (1.69, 650.1),
    ('Campo Grande (MS)', 'Aracaju (SE)'): (1.69, 650.1),
    ('Brasilia (DF)', 'Aracaju (SE)'): (1.11, 425.98),
    ('Aracaju (SE)', 'Brasilia (DF)'): (1.11, 425.98),
    ('Recife (PE)', 'Sao Paulo (SP)'): (1.26, 486.52),
    ('Sao Paulo (SP)', 'Recife (PE)'): (1.26, 486.52),
    ('Brasilia (DF)', 'Campo Grande (MS)'): (0.72, 277.7),
    ('Campo Grande (MS)', 'Brasilia (DF)'): (0.72, 277.7),
    ('Brasilia (DF)', 'Sao Paulo (SP)'): (0.67, 257.81),
    ('Sao Paulo (SP)', 'Brasilia (DF)'): (0.67, 257.81),
    ('Brasilia (DF)', 'Salvador (BH)'): (1.76, 676.56),
    ('Salvador (BH)', 'Brasilia (DF)'): (1.76, 676.56),
    ('Recife (PE)', 'Natal (RN)'): (0.58, 222.67),
    ('Natal (RN)', 'Recife (PE)'): (0.58, 222.67),
    ('Brasilia (DF)', 'Natal (RN)'): (1.43, 550.69),
    ('Natal (RN)', 'Brasilia (DF)'): (1.43, 550.69),
    ('Recife (PE)', 'Salvador (BH)'): (2.05, 788.55),
    ('Salvador (BH)', 'Recife (PE)'): (2.05, 788.55),
    ('Recife (PE)', 'Campo Grande (MS)'): (1.39, 535.4),
    ('Campo Grande (MS)', 'Recife (PE)'): (1.39, 535.4),
    ('Brasilia (DF)', 'Recife (PE)'): (0.63, 242.21),
    ('Recife (PE)', 'Brasilia (DF)'): (0.63, 242.21),
    ('Aracaju (SE)', 'Sao Paulo (SP)'): (1.02, 392.76),
    ('Sao Paulo (SP)', 'Aracaju (SE)'): (1.02, 392.76),
    ('Aracaju (SE)', 'Natal (RN)'): (0.46, 176.33),
    ('Natal (RN)', 'Aracaju (SE)'): (0.46, 176.33),
    ('Aracaju (SE)', 'Recife (PE)'): (1.44, 555.74),
    ('Recife (PE)', 'Aracaju (SE)'): (1.44, 555.74),
    ('Aracaju (SE)', 'Rio de Janeiro (RJ)'): (1.55, 597.61),
    ('Rio de Janeiro (RJ)', 'Aracaju (SE)'): (1.55, 597.61),
    ('Aracaju (SE)', 'Florianopolis (SC)'): (2.1, 808.85),
    ('Florianopolis (SC)', 'Aracaju (SE)'): (2.1, 808.85),
    ('Brasilia (DF)', 'Rio de Janeiro (RJ)'): (0.48, 183.37),
    ('Rio de Janeiro (RJ)', 'Brasilia (DF)'): (0.48, 183.37),
    ('Recife (PE)', 'Rio de Janeiro (RJ)'): (2.3, 885.57),
    ('Rio de Janeiro (RJ)', 'Recife (PE)'): (2.3, 885.57),
    ('Campo Grande (MS)', 'Florianopolis (SC)'): (1.49, 573.81),
    ('Florianopolis (SC)', 'Campo Grande (MS)'): (1.49, 573.81),
    ('Campo Grande (MS)', 'Salvador (BH)'): (1.36, 522.34),
    ('Salvador (BH)', 'Campo Grande (MS)'): (1.36, 522.34),
    ('Campo Grande (MS)', 'Sao Paulo (SP)'): (0.44, 168.22),
    ('Sao Paulo (SP)', 'Campo Grande (MS)'): (0.44, 168.22),
    ('Campo Grande (MS)', 'Natal (RN)'): (0.65, 250.68),
    ('Natal (RN)', 'Campo Grande (MS)'): (0.65, 250.68),
    ('Campo Grande (MS)', 'Rio de Janeiro (RJ)'): (2.09, 806.48),
    ('Rio de Janeiro (RJ)', 'Campo Grande (MS)'): (2.09, 806.48),
    ('Natal (RN)', 'Rio de Janeiro (RJ)'): (1.55, 595.03),
    ('Rio de Janeiro (RJ)', 'Natal (RN)'): (1.55, 595.03),
    ('Sao Paulo (SP)', 'Salvador (BH)'): (1.04, 401.66),
    ('Salvador (BH)', 'Sao Paulo (SP)'): (1.04, 401.66),
    ('Sao Paulo (SP)', 'Natal (RN)'): (0.85, 327.55),
    ('Natal (RN)', 'Sao Paulo (SP)'): (0.85, 327.55),
    ('Sao Paulo (SP)', 'Rio de Janeiro (RJ)'): (0.86, 331.89),
    ('Rio de Janeiro (RJ)', 'Sao Paulo (SP)'): (0.86, 331.89),
    ('Sao Paulo (SP)', 'Florianopolis (SC)'): (1.46, 562.14),
    ('Florianopolis (SC)', 'Sao Paulo (SP)'): (1.46, 562.14),
    ('Natal (RN)', 'Salvador (BH)'): (1.85, 710.57),
    ('Salvador (BH)', 'Natal (RN)'): (1.85, 710.57),
    ('Natal (RN)', 'Florianopolis (SC)'): (1.84, 709.37),
    ('Florianopolis (SC)', 'Natal (RN)'): (1.84, 709.37),
    ('Florianopolis (SC)', 'Rio de Janeiro (RJ)'): (1.21, 466.3),
    ('Rio de Janeiro (RJ)', 'Florianopolis (SC)'): (1.21, 466.3),
    ('Florianopolis (SC)', 'Salvador (BH)'): (2.44, 937.77),
    ('Salvador (BH)', 'Florianopolis (SC)'): (2.44, 937.77),
}

def get_route_info(from_city, to_city):
    """
    Get travel time and distance for a specific route.
    
    Parameters:
    - from_city (str): Departure city
    - to_city (str): Destination city

    Returns:
    - tuple: (time, distance) if route exists, None otherwise
    """
    return routes.get((from_city, to_city), None)
