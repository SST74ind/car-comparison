import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = 'cars.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with an unabridged mapping of the Indian automotive market."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            variant TEXT,
            segment TEXT,
            price_min INTEGER,
            price_max INTEGER,
            mileage_kmpl REAL,
            ev_range_km INTEGER,
            fuel_type TEXT,
            engine_cc INTEGER,
            power_bhp INTEGER,
            torque_nm INTEGER,
            transmission TEXT,
            seating INTEGER,
            boot_space INTEGER,
            safety_rating INTEGER,
            resale_3yr INTEGER,
            resale_5yr INTEGER,
            features TEXT
        )
    ''')
    
    # Unabridged Master Catalog Matrix of the Indian Market
    market_matrix = [
        # === MARUTI SUZUKI ===
        ("Maruti Suzuki", "Alto K10", "Hatchback", 399000, "Petrol", 998, 66, 89, 24.39, 0, 5, 214, 2, ["Std", "LXi", "VXi", "VXi+"]),
        ("Maruti Suzuki", "S-Presso", "Hatchback", 426000, "Petrol", 998, 66, 89, 24.12, 0, 5, 270, 2, ["Std", "LXi", "VXi", "VXi+"]),
        ("Maruti Suzuki", "Wagon R", "Hatchback", 554000, "Petrol", 1197, 88, 113, 24.35, 0, 5, 341, 2, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "Celerio", "Hatchback", 536000, "Petrol", 998, 66, 89, 25.24, 0, 5, 313, 2, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "Swift", "Hatchback", 649000, "Petrol", 1197, 80, 112, 25.75, 0, 5, 265, 4, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "Dzire", "Sedan", 679000, "Petrol", 1197, 80, 112, 24.12, 0, 5, 382, 5, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "Baleno", "Hatchback", 666000, "Petrol", 1197, 88, 113, 22.35, 0, 5, 318, 4, ["Sigma", "Delta", "Zeta", "Alpha"]),
        ("Maruti Suzuki", "Fronx", "Compact SUV", 751000, "Petrol", 1197, 88, 113, 22.89, 0, 5, 308, 4, ["Sigma", "Delta", "Zeta", "Alpha"]),
        ("Maruti Suzuki", "Brezza", "Compact SUV", 834000, "Petrol", 1462, 102, 137, 19.89, 0, 5, 328, 4, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "Eeco", "Utility Van", 532000, "Petrol", 1197, 81, 104, 19.71, 0, 7, 60, 2, ["5-Seater Standard", "7-Seater Standard", "5-Seater AC"]),
        ("Maruti Suzuki", "Ertiga", "MPV", 869000, "Petrol", 1462, 102, 137, 20.51, 0, 7, 209, 3, ["LXi", "VXi", "ZXi", "ZXi+"]),
        ("Maruti Suzuki", "XL6", "MPV", 1161000, "Petrol", 1462, 102, 137, 20.97, 0, 6, 209, 3, ["Zeta", "Alpha", "Alpha+"]),
        ("Maruti Suzuki", "Grand Vitara", "SUV", 1080000, "Petrol", 1462, 102, 137, 21.11, 0, 5, 373, 4, ["Sigma", "Delta", "Zeta", "Alpha"]),
        ("Maruti Suzuki", "Ciaz", "Sedan", 940000, "Petrol", 1462, 103, 138, 20.65, 0, 5, 510, 4, ["Sigma", "Delta", "Zeta", "Alpha"]),
        ("Maruti Suzuki", "Jimny", "Offroader", 1274000, "Petrol", 1462, 103, 134, 16.94, 0, 4, 211, 4, ["Zeta", "Alpha"]),
        ("Maruti Suzuki", "Invicto", "Premium MPV", 2521000, "Hybrid", 1987, 184, 188, 23.24, 0, 7, 239, 5, ["Zeta+", "Alpha+"]),

        # === TATA MOTORS ===
        ("Tata", "Tiago", "Hatchback", 565000, "Petrol", 1199, 85, 113, 19.01, 0, 5, 242, 4, ["XE", "XM", "XT", "XZ+"]),
        ("Tata", "Tigor", "Sedan", 630000, "Petrol", 1199, 85, 113, 19.28, 0, 5, 419, 4, ["XE", "XM", "XT", "XZ+"]),
        ("Tata", "Altroz", "Premium Hatchback", 665000, "Petrol", 1199, 87, 115, 19.33, 0, 5, 345, 5, ["XE", "XM+", "XT", "XZ+"]),
        ("Tata", "Punch", "Micro SUV", 613000, "Petrol", 1199, 87, 115, 20.09, 0, 5, 366, 5, ["Pure", "Adventure", "Accomplished", "Creative"]),
        ("Tata", "Nexon", "Compact SUV", 800000, "Petrol", 1199, 118, 170, 17.44, 0, 5, 382, 5, ["Smart", "Pure", "Creative", "Fearless"]),
        ("Tata", "Curvv", "SUV Coupe", 999000, "Petrol", 1199, 118, 170, 17.50, 0, 5, 422, 5, ["Smart", "Pure", "Creative", "Accomplished", "Empowered"]),
        ("Tata", "Harrier", "SUV", 1549000, "Diesel", 1956, 168, 350, 16.80, 0, 5, 445, 5, ["Smart", "Pure", "Adventure", "Fearless"]),
        ("Tata", "Safari", "SUV", 1619000, "Diesel", 1956, 168, 350, 16.30, 0, 7, 420, 5, ["Smart", "Pure", "Adventure", "Accomplished"]),
        ("Tata", "Tiago EV", "EV Hatchback", 799000, "Electric", 0, 60, 110, 0, 250, 5, 240, 4, ["XE", "XT", "XZ+"]),
        ("Tata", "Tigor EV", "EV Sedan", 1249000, "Electric", 0, 74, 170, 0, 315, 5, 316, 4, ["XE", "XT", "XZ+"]),
        ("Tata", "Punch EV", "EV SUV", 999000, "Electric", 0, 80, 114, 0, 315, 5, 366, 5, ["Smart", "Adventure", "Empowered"]),
        ("Tata", "Nexon EV", "EV SUV", 1249000, "Electric", 0, 127, 215, 0, 325, 5, 350, 5, ["Creative", "Fearless", "Empowered"]),
        ("Tata", "Curvv EV", "EV SUV Coupe", 1749000, "Electric", 0, 165, 215, 0, 502, 5, 500, 5, ["Creative", "Accomplished", "Empowered"]),

        # === HYUNDAI ===
        ("Hyundai", "Grand i10 Nios", "Hatchback", 592000, "Petrol", 1197, 82, 114, 20.10, 0, 5, 260, 2, ["Era", "Magna", "Sportz", "Asta"]),
        ("Hyundai", "Aura", "Compact Sedan", 649000, "Petrol", 1197, 82, 114, 20.50, 0, 5, 402, 2, ["E", "S", "SX", "SX(O)"]),
        ("Hyundai", "i20", "Premium Hatchback", 704000, "Petrol", 1197, 82, 115, 16.00, 0, 5, 311, 3, ["Magna", "Sportz", "Asta", "Asta(O)"]),
        ("Hyundai", "i20 N Line", "Performance Hatchback", 999000, "Petrol", 998, 118, 172, 20.00, 0, 5, 311, 3, ["N6", "N8"]),
        ("Hyundai", "Exter", "Micro SUV", 613000, "Petrol", 1197, 82, 114, 19.40, 0, 5, 391, 3, ["EX", "S", "SX", "SX(O)"]),
        ("Hyundai", "Venue", "Compact SUV", 794000, "Petrol", 1197, 82, 114, 17.50, 0, 5, 350, 3, ["E", "S", "SX", "SX(O)"]),
        ("Hyundai", "Venue N Line", "Performance SUV", 1208000, "Petrol", 998, 118, 172, 18.00, 0, 5, 350, 3, ["N6", "N8"]),
        ("Hyundai", "Creta", "SUV", 1100000, "Petrol", 1497, 113, 144, 17.40, 0, 5, 433, 3, ["E", "EX", "S", "SX", "SX(O)"]),
        ("Hyundai", "Creta N Line", "Performance SUV", 1682000, "Petrol", 1482, 158, 253, 18.20, 0, 5, 433, 3, ["N8", "N10"]),
        ("Hyundai", "Verna", "Sedan", 1100000, "Petrol", 1497, 113, 144, 18.60, 0, 5, 528, 5, ["EX", "S", "SX", "SX(O)"]),
        ("Hyundai", "Alcazar", "SUV", 1677000, "Petrol", 1482, 158, 253, 14.20, 0, 7, 180, 3, ["Executive", "Prestige", "Platinum", "Signature"]),
        ("Hyundai", "Tucson", "Premium SUV", 2902000, "Petrol", 1999, 154, 192, 13.00, 0, 5, 540, 5, ["Platinum", "Signature"]),
        ("Hyundai", "Ioniq 5", "Premium EV", 4605000, "Electric", 0, 215, 350, 0, 631, 5, 527, 5, ["Long Range RWD"]),

        # === MAHINDRA ===
        ("Mahindra", "XUV 3XO", "Compact SUV", 749000, "Petrol", 1197, 110, 200, 18.89, 0, 5, 364, 5, ["MX1", "MX3", "AX5", "AX7"]),
        ("Mahindra", "Thar", "Offroader", 1135000, "Diesel", 2184, 130, 300, 15.20, 0, 4, 150, 4, ["AX(O)", "LX"]),
        ("Mahindra", "Thar Roxx", "Offroader SUV", 1299000, "Petrol", 1997, 160, 330, 12.40, 0, 5, 447, 5, ["MX1", "MX5", "AX5L", "AX7L"]),
        ("Mahindra", "Scorpio Classic", "SUV", 1362000, "Diesel", 2184, 130, 300, 14.00, 0, 7, 460, 3, ["S", "S11"]),
        ("Mahindra", "Scorpio-N", "SUV", 1385000, "Diesel", 2184, 172, 400, 12.17, 0, 7, 460, 5, ["Z2", "Z4", "Z6", "Z8", "Z8L"]),
        ("Mahindra", "XUV700", "SUV", 1399000, "Diesel", 2184, 182, 420, 13.00, 0, 7, 450, 5, ["MX", "AX3", "AX5", "AX7", "AX7L"]),
        ("Mahindra", "Bolero", "Rugged SUV", 979000, "Diesel", 1493, 75, 210, 16.00, 0, 7, 384, 1, ["B4", "B6", "B6 Opt"]),
        ("Mahindra", "Bolero Neo", "Rugged SUV", 990000, "Diesel", 1493, 100, 260, 17.29, 0, 7, 384, 1, ["N4", "N8", "N10"]),
        ("Mahindra", "XUV400 EV", "EV SUV", 1549000, "Electric", 0, 148, 310, 0, 456, 5, 378, 5, ["EC Pro", "EL Pro"]),

        # === KIA ===
        ("Kia", "Sonet", "Compact SUV", 799000, "Petrol", 1197, 82, 115, 18.70, 0, 5, 385, 3, ["HTE", "HTK", "HTX", "GTX+", "X-Line"]),
        ("Kia", "Seltos", "SUV", 1090000, "Petrol", 1497, 113, 144, 17.00, 0, 5, 433, 3, ["HTE", "HTK", "HTX", "GTX+", "X-Line"]),
        ("Kia", "Carens", "MPV", 1052000, "Petrol", 1497, 113, 144, 17.90, 0, 7, 216, 3, ["Premium", "Prestige", "Luxury", "Luxury+"]),
        ("Kia", "Carnival", "Premium MPV", 6390000, "Diesel", 2199, 197, 440, 14.20, 0, 7, 540, 5, ["Limousine", "Limousine Plus"]),
        ("Kia", "EV6", "Premium EV", 6095000, "Electric", 0, 320, 605, 0, 708, 5, 520, 5, ["GT-Line", "GT-Line AWD"]),
        ("Kia", "EV9", "Premium EV SUV", 13000000, "Electric", 0, 379, 700, 0, 561, 6, 571, 5, ["GT-Line"]),

        # === TOYOTA ===
        ("Toyota", "Glanza", "Hatchback", 686000, "Petrol", 1197, 88, 113, 22.35, 0, 5, 318, 4, ["E", "S", "G", "V"]),
        ("Toyota", "Rumion", "MPV", 1044000, "Petrol", 1462, 102, 137, 20.51, 0, 7, 209, 3, ["S", "G", "V"]),
        ("Toyota", "Urban Cruiser Hyryder", "SUV", 1114000, "Petrol", 1462, 102, 137, 21.12, 0, 5, 373, 4, ["E", "S", "G", "V"]),
        ("Toyota", "Innova Crysta", "MPV", 1999000, "Diesel", 2393, 148, 343, 11.50, 0, 7, 300, 5, ["GX", "VX", "ZX"]),
        ("Toyota", "Innova Hycross", "Premium MPV", 1977000, "Petrol", 1987, 173, 209, 16.13, 0, 7, 300, 5, ["GX", "VX", "ZX"]),
        ("Toyota", "Fortuner", "Premium SUV", 3343000, "Diesel", 2755, 201, 500, 10.00, 0, 7, 296, 5, ["Standard", "Legender", "GR Sport"]),
        ("Toyota", "Hilux", "Pickup Truck", 3040000, "Diesel", 2755, 201, 420, 12.00, 0, 5, 435, 5, ["Standard", "High"]),
        ("Toyota", "Camry", "Luxury Sedan", 4617000, "Hybrid", 2487, 176, 221, 22.70, 0, 5, 524, 5, ["2.5 Hybrid"]),
        ("Toyota", "Vellfire", "Luxury MPV", 11990000, "Hybrid", 2487, 190, 240, 19.28, 0, 7, 450, 5, ["Hi", "VIP Grade"]),

        # === HONDA ===
        ("Honda", "Amaze", "Compact Sedan", 720000, "Petrol", 1199, 89, 110, 18.60, 0, 5, 420, 4, ["E", "S", "VX"]),
        ("Honda", "City", "Sedan", 1182000, "Petrol", 1498, 119, 145, 17.80, 0, 5, 506, 5, ["SV", "V", "VX", "ZX"]),
        ("Honda", "City Hybrid e:HEV", "Hybrid Sedan", 1900000, "Hybrid", 1498, 124, 253, 27.13, 0, 5, 410, 5, ["V", "ZX"]),
        ("Honda", "Elevate", "SUV", 1169000, "Petrol", 1498, 119, 145, 16.90, 0, 5, 458, 5, ["SV", "V", "VX", "ZX"]),

        # === CITROEN ===
        ("Citroen", "C3", "Hatchback", 616000, "Petrol", 1198, 81, 115, 19.30, 0, 5, 315, 2, ["Live", "Feel", "Shine", "Shine Turbo"]),
        ("Citroen", "Aircross", "SUV", 999000, "Petrol", 1199, 109, 190, 18.50, 0, 7, 511, 3, ["You", "Plus", "Max"]),
        ("Citroen", "Basalt", "SUV Coupe", 799000, "Petrol", 1199, 109, 190, 18.00, 0, 5, 470, 4, ["You", "Plus", "Max"]),
        ("Citroen", "C3X", "Crossover Sedan", 950000, "Petrol", 1199, 109, 190, 18.20, 0, 5, 480, 4, ["Live", "Feel", "Shine"]),
        ("Citroen", "eC3X", "EV Hatchback Crossover", 1025000, "Electric", 0, 57, 143, 0, 325, 5, 315, 3, ["Live", "Live (O)", "Shine"]),
        ("Citroen", "C5 Aircross", "Premium SUV", 3767000, "Diesel", 1997, 174, 400, 17.50, 0, 5, 580, 5, ["Shine"]),

        # === MERCEDES-BENZ ===
        ("Mercedes-Benz", "A-Class Limousine", "Luxury Sedan", 4600000, "Petrol", 1332, 161, 270, 17.50, 0, 5, 405, 5, ["A200", "A200d Progressive"]),
        ("Mercedes-Benz", "C-Class", "Luxury Sedan", 6100000, "Petrol", 1496, 201, 300, 16.90, 0, 5, 455, 5, ["C200", "C220d", "C300d"]),
        ("Mercedes-Benz", "E-Class LWB", "Luxury Executive Sedan", 7600000, "Petrol", 1999, 194, 320, 15.00, 0, 5, 540, 5, ["E200", "E220d", "E450"]),
        ("Mercedes-Benz", "S-Class", "Flagship Luxury Sedan", 17700000, "Diesel", 2925, 282, 600, 13.50, 0, 5, 550, 5, ["S350d", "S450"]),
        ("Mercedes-Benz", "GLA", "Luxury Compact SUV", 5100000, "Petrol", 1332, 161, 270, 17.40, 0, 5, 425, 5, ["GLA200", "GLA220d"]),
        ("Mercedes-Benz", "GLC", "Luxury Midsize SUV", 7500000, "Petrol", 1999, 254, 400, 14.70, 0, 5, 620, 5, ["GLC200", "GLC220d"]),
        ("Mercedes-Benz", "GLE", "Luxury SUV", 9700000, "Diesel", 1993, 265, 550, 14.00, 0, 5, 630, 5, ["GLE300d", "GLE450d", "GLE450"]),
        ("Mercedes-Benz", "GLS", "Luxury Fullsize SUV", 13200000, "Diesel", 2989, 362, 750, 11.00, 0, 7, 470, 5, ["GLS450d", "GLS450"]),
        ("Mercedes-Benz", "G-Class", "Luxury Offroader", 25500000, "Diesel", 2925, 326, 700, 9.30, 0, 5, 480, 5, ["G400d", "AMG G63"]),
        ("Mercedes-Benz", "EQE SUV", "Luxury EV SUV", 13900000, "Electric", 0, 408, 858, 0, 550, 5, 520, 5, ["EQE 500"]),

        # === AUDI ===
        ("Audi", "A4", "Luxury Sedan", 4688000, "Petrol", 1984, 202, 320, 17.40, 0, 5, 460, 5, ["Premium", "Premium Plus", "Technology"]),
        ("Audi", "A6", "Luxury Fullsize Sedan", 6481000, "Petrol", 1984, 241, 370, 14.00, 0, 5, 530, 5, ["Premium Plus", "Technology"]),
        ("Audi", "S5 Sportback", "Luxury Performance Sedan", 7357000, "Petrol", 2994, 349, 500, 10.60, 0, 5, 480, 5, ["Base"]),
        ("Audi", "Q3", "Luxury Compact SUV", 4367000, "Petrol", 1984, 190, 320, 14.93, 0, 5, 530, 5, ["Premium", "Premium Plus", "Technology"]),
        ("Audi", "Q3 Sportback", "Luxury Coupe SUV", 5425000, "Petrol", 1984, 190, 320, 14.93, 0, 5, 530, 5, ["Technology S-Line"]),
        ("Audi", "Q5", "Luxury Midsize SUV", 6555000, "Petrol", 1984, 245, 370, 13.40, 0, 5, 520, 5, ["Premium Plus", "Technology"]),
        ("Audi", "Q7", "Luxury Fullsize SUV", 8717000, "Petrol", 2995, 335, 500, 11.20, 0, 7, 295, 5, ["Premium Plus", "Technology"]),
        ("Audi", "Q8", "Flagship Luxury SUV", 11300000, "Petrol", 2995, 335, 500, 9.80, 0, 5, 605, 5, ["Celebration Edition", "Standard"]),
        ("Audi", "SQ8", "High Performance SUV", 17800000, "Petrol", 3996, 507, 770, 8.50, 0, 5, 605, 5, ["Standard"]),
        ("Audi", "RS Q8", "Super SUV", 23400000, "Petrol", 3996, 591, 800, 8.00, 0, 5, 605, 5, ["Standard"]),
        ("Audi", "Q8 e-tron", "Luxury EV SUV", 13300000, "Electric", 0, 402, 664, 0, 491, 5, 569, 5, ["50 e-tron", "55 e-tron"]),
        ("Audi", "Q8 e-tron Sportback", "Luxury EV Coupe SUV", 11900000, "Electric", 0, 402, 664, 0, 600, 5, 528, 5, ["50 e-tron", "55 e-tron"]),

        # === BMW ===
        ("BMW", "2 Series Gran Coupe", "Luxury Sedan", 4580000, "Petrol", 1998, 176, 280, 14.82, 0, 5, 430, 5, ["220i M Sport", "220d M Sport"]),
        ("BMW", "3 Series Gran Limousine", "Luxury Sedan", 6060000, "Petrol", 1998, 255, 400, 15.39, 0, 5, 480, 5, ["320Li M Sport", "330Li M Sport"]),
        ("BMW", "3 Series M340i", "Performance Sedan", 7290000, "Petrol", 2998, 374, 500, 13.02, 0, 5, 480, 5, ["xDrive"]),
        ("BMW", "5 Series", "Luxury Sedan", 7580000, "Petrol", 1998, 248, 350, 14.80, 0, 5, 530, 5, ["520d M Sport", "520i M Sport"]),
        ("BMW", "7 Series", "Flagship Luxury Sedan", 18100000, "Petrol", 2998, 375, 520, 12.50, 0, 5, 540, 5, ["740i M Sport", "740d M Sport"]),
        ("BMW", "X1", "Luxury SUV", 4950000, "Petrol", 1499, 134, 230, 16.35, 0, 5, 476, 5, ["sDrive18i M Sport", "sDrive18d M Sport"]),
        ("BMW", "X3", "Luxury SUV", 7250000, "Diesel", 1995, 188, 400, 16.55, 0, 5, 550, 5, ["xDrive20d M Sport", "xDrive30i M Sport"]),
        ("BMW", "X5", "Luxury SUV", 9700000, "Diesel", 2998, 282, 650, 12.00, 0, 5, 650, 5, ["xDrive30d M Sport", "xDrive40i M Sport"]),
        ("BMW", "X7", "Luxury Fullsize SUV", 13000000, "Diesel", 2998, 335, 700, 11.20, 0, 7, 325, 5, ["xDrive40i M Sport", "xDrive40d M Sport"]),
        ("BMW", "Z4 Roadster", "Luxury Sports Car", 9090000, "Petrol", 2998, 335, 500, 12.09, 0, 2, 281, 5, ["M40i"]),
        ("BMW", "M2", "Track Performance Coupe", 9990000, "Petrol", 2993, 453, 550, 10.13, 0, 4, 390, 5, ["Standard", "CS"]),
        ("BMW", "M4 Competition", "Track Performance Coupe", 15300000, "Petrol", 2993, 503, 650, 9.70, 0, 4, 440, 5, ["xDrive"]),
        ("BMW", "M5", "High Performance Super Sedan", 20800000, "Petrol", 4395, 617, 750, 8.60, 0, 5, 530, 5, ["Standard"]),
        ("BMW", "XM", "High Performance Luxury SUV", 26000000, "Hybrid", 4395, 644, 800, 61.90, 0, 5, 527, 5, ["Standard"]),
        ("BMW", "i4", "Luxury EV Sedan", 7390000, "Electric", 0, 335, 430, 0, 590, 5, 470, 5, ["eDrive40"]),
        ("BMW", "i5", "Luxury EV Sedan", 12000000, "Electric", 0, 593, 795, 0, 516, 5, 490, 5, ["M60 xDrive"]),
        ("BMW", "i7", "Flagship Luxury EV Sedan", 21300000, "Electric", 0, 536, 745, 0, 625, 5, 500, 5, ["eDrive50", "M70 xDrive"]),
        ("BMW", "iX1 LWB", "Luxury EV SUV", 5140000, "Electric", 0, 308, 494, 0, 440, 5, 490, 5, ["xDrive30"]),
        ("BMW", "iX", "Luxury EV SUV", 12100000, "Electric", 0, 322, 630, 0, 425, 5, 500, 5, ["xDrive50"]),

        # === MG MOTOR ===
        ("MG", "Comet EV", "Micro EV", 698000, "Electric", 0, 41, 110, 0, 230, 4, 0, 3, ["Pace", "Play", "Plush"]),
        ("MG", "Windsor EV", "EV Crossover", 1350000, "Electric", 0, 136, 200, 0, 332, 5, 604, 4, ["Excite", "Exclusive", "Essence"]),
        ("MG", "Astor", "SUV", 998000, "Petrol", 1498, 108, 144, 14.34, 0, 5, 400, 5, ["Sprint", "Shine", "Select", "Sharp Pro"]),
        ("MG", "Hector", "SUV", 1399000, "Petrol", 1451, 141, 250, 13.79, 0, 5, 587, 5, ["Style", "Shine", "Smart", "Sharp Pro"]),
        ("MG", "Hector Plus", "SUV", 1730000, "Diesel", 1956, 168, 350, 15.00, 0, 7, 530, 5, ["Style", "Smart", "Sharp Pro"]),
        ("MG", "ZS EV", "EV SUV", 1898000, "Electric", 0, 174, 280, 0, 461, 5, 448, 5, ["Executive", "Excite", "Exclusive"]),
        ("MG", "Gloster", "Full Size SUV", 3880000, "Diesel", 1996, 212, 478, 12.00, 0, 7, 343, 5, ["Sharp", "Savvy"]),

        # === SKODA & VOLKSWAGEN ===
        ("Skoda", "Kylaq", "Compact SUV", 789000, "Petrol", 999, 114, 178, 17.80, 0, 5, 446, 5, ["Classic", "Signature", "Prestige"]),
        ("Skoda", "Slavia", "Sedan", 1150000, "Petrol", 999, 114, 178, 18.73, 0, 5, 521, 5, ["Classic", "Signature", "Prestige"]),
        ("Skoda", "Kushaq", "SUV", 1199000, "Petrol", 999, 114, 178, 18.09, 0, 5, 385, 5, ["Classic", "Signature", "Prestige"]),
        ("Skoda", "Kodiaq", "Premium SUV", 3999000, "Petrol", 1984, 187, 320, 12.78, 0, 7, 270, 5, ["Style", "Sportline", "L&K"]),
        ("Skoda", "Superb", "Luxury Sedan", 5400000, "Petrol", 1984, 188, 320, 15.10, 0, 5, 625, 5, ["L&K"]),
        ("Volkswagen", "Virtus", "Sedan", 1155000, "Petrol", 999, 114, 178, 18.45, 0, 5, 521, 5, ["Comfortline", "Highline", "Topline", "GT"]),
        ("Volkswagen", "Taigun", "SUV", 1170000, "Petrol", 999, 114, 178, 18.15, 0, 5, 385, 5, ["Comfortline", "Highline", "Topline", "GT"]),
        ("Volkswagen", "Tiguan", "Premium SUV", 3517000, "Petrol", 1984, 187, 320, 12.60, 0, 5, 615, 5, ["Elegance"]),

        # === NISSAN & RENAULT ===
        ("Nissan", "Magnite", "Compact SUV", 599000, "Petrol", 999, 71, 96, 19.35, 0, 5, 336, 4, ["XE", "XL", "XV", "XV Premium"]),
        ("Nissan", "X-Trail", "Premium SUV", 4992000, "Petrol", 1498, 161, 300, 13.00, 0, 7, 585, 5, ["AWD"]),
        ("Renault", "Kwid", "Hatchback", 470000, "Petrol", 999, 67, 91, 21.46, 0, 5, 279, 1, ["RXE", "RXL", "RXT", "Climber"]),
        ("Renault", "Triber", "MPV", 600000, "Petrol", 999, 71, 96, 18.20, 0, 7, 84, 4, ["RXE", "RXL", "RXT", "RXZ"]),
        ("Renault", "Kiger", "Compact SUV", 600000, "Petrol", 999, 71, 96, 19.83, 0, 5, 405, 4, ["RXE", "RXT", "RXZ"]),

        # === JEEP ===
        ("Jeep", "Compass", "Premium SUV", 1899000, "Diesel", 1956, 168, 350, 14.90, 0, 5, 438, 5, ["Sport", "Longitudes", "Limited", "Model S"]),
        ("Jeep", "Meridian", "Premium SUV", 2499000, "Diesel", 1956, 168, 350, 13.90, 0, 7, 481, 5, ["Limited", "Limited Plus"]),

        # === BYD & ISUZU ===
        ("BYD", "E6", "EV MPV", 2915000, "Electric", 0, 94, 180, 0, 520, 5, 580, 5, ["GLX"]),
        ("BYD", "Atto 3", "EV SUV", 2499000, "Electric", 0, 201, 310, 0, 468, 5, 440, 5, ["Dynamic", "Premium", "Superior"]),
        ("BYD", "Seal", "EV Luxury Sedan", 4100000, "Electric", 0, 523, 670, 0, 650, 5, 400, 5, ["Dynamic", "Premium", "Performance"]),
        ("Isuzu", "D-Max V-Cross", "Adventure Pickup", 2300000, "Diesel", 1898, 161, 360, 12.00, 0, 5, 450, 4, ["Hi-Lander", "Z", "Z Prestige"]),

        # === VOLVO ===
        ("Volvo", "XC40 Recharge", "Luxury EV SUV", 5495000, "Electric", 0, 408, 660, 0, 530, 5, 419, 5, ["Single", "Twin Motor"]),
        ("Volvo", "XC60", "Luxury SUV", 6890000, "Petrol", 1969, 250, 350, 12.40, 0, 5, 483, 5, ["B5 Ultimate"])
    ]
    
    for entry in market_matrix:
        brand, model, segment, base_price, fuel, cc, bhp, torque, mileage, ev_range, seating, boot, safety, trims = entry
        
        for idx, trim in enumerate(trims):
            trim_price_min = base_price + (idx * 115000)
            trim_price_max = trim_price_min + 80000
            
            if fuel == "Electric" or "Luxury" in segment or idx >= 2:
                transmission = "Automatic"
            else:
                transmission = "Manual"
                
            trim_ev_range = ev_range + (idx * 35) if ev_range > 0 else 0
            
            if fuel == "Electric":
                if idx == 0:
                    feats = "Regenerative Braking • Digital instrument panel • Smart Keyless entry • Connected car tech"
                else:
                    feats = "ADAS Pilot • Large Panoramic Glass Roof • Ventilated front seats • V2L power output"
            elif "Luxury" in segment or "Performance" in segment:
                feats = "Premium leather upholstery • Multi-zone ambient cabin lighting • Soft-closing doors • Level-2 Autonomous ADAS"
            else:
                if idx == 0:
                    feats = "Basic power windows • Dual front airbags • ABS with EBD • Reverse distance warnings"
                elif idx == 1:
                    feats = "Steering-mounted phone layouts • 7-inch Smart touchscreen audio • Day/night rear view adjustment"
                else:
                    feats = "Precision alloy wheels • Engine start/stop push layout • Automated climate adjustment • 360-degree environment camera view"
                    
            r3 = 82 if brand in ["Maruti Suzuki", "Toyota"] else (76 if brand in ["Hyundai", "Kia", "Mahindra"] else 68)
            r5 = r3 - 12
            
            cursor.execute('''
                INSERT INTO cars (brand, model, variant, segment, price_min, price_max, mileage_kmpl, ev_range_km, fuel_type, engine_cc, power_bhp, torque_nm, transmission, seating, boot_space, safety_rating, resale_3yr, resale_5yr, features)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (brand, model, trim, segment, trim_price_min, trim_price_max, mileage, trim_ev_range, fuel, cc, bhp, torque, transmission, seating, boot, safety, r3, r5, feats))
            
    conn.commit()
    conn.close()

# --- WEB APP ROUTING AND CONTROLLERS ---

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    rows = cursor.execute('SELECT brand, model, variant FROM cars ORDER BY brand ASC, model ASC, id ASC').fetchall()
    cars_dropdown = []
    for r in rows:
        val = f"{r['brand']}|{r['model']}|{r['variant']}"
        disp = f"{r['brand']} {r['model']} — {r['variant']}"
        cars_dropdown.append({"value": val, "display": disp})
        
    conn.close()
    
    compared = False
    car1_data = car2_data = None
    winners = {}
    chart_cost1 = chart_cost2 = []
    resale1_3yr = resale1_5yr = resale2_3yr = resale2_5yr = 0
    fuel_cost1 = fuel_cost2 = emi1 = emi2 = 0
    mode = request.args.get('mode', 'quick')
    
    car1_param = request.args.get('car1')
    car2_param = request.args.get('car2')
    
    if car1_param and car2_param:
        compared = True
        p1 = car1_param.split('|')
        p2 = car2_param.split('|')
        
        conn = get_db_connection()
        car1_row = conn.execute('SELECT * FROM cars WHERE brand=? AND model=? AND variant=?', (p1[0], p1[1], p1[2])).fetchone()
        car2_row = conn.execute('SELECT * FROM cars WHERE brand=? AND model=? AND variant=?', (p2[0], p2[1], p2[2])).fetchone()
        conn.close()
        
        if car1_row and car2_row:
            car1_data = dict(car1_row)
            car2_data = dict(car2_row)
            
            winners = {
                "price": "car1" if car1_data['price_min'] <= car2_data['price_min'] else "car2",
                "mileage": "car1" if max(car1_data['mileage_kmpl'], car1_data['ev_range_km']) >= max(car2_data['mileage_kmpl'], car2_data['ev_range_km']) else "car2",
                "engine": "car1" if car1_data['engine_cc'] >= car2_data['engine_cc'] else "car2",
                "power": "car1" if car1_data['power_bhp'] >= car2_data['power_bhp'] else "car2",
                "torque": "car1" if car1_data['torque_nm'] >= car2_data['torque_nm'] else "car2",
                "safety": "car1" if car1_data['safety_rating'] >= car2_data['safety_rating'] else "car2",
                "boot": "car1" if car1_data['boot_space'] >= car2_data['boot_space'] else "car2"
            }
            
            daily_km = float(request.args.get('daily_km', 40))
            fuel_price = float(request.args.get('fuel_price', 103))
            years = int(request.args.get('years', 5))
            
            eff1 = car1_data['mileage_kmpl'] if car1_data['fuel_type'] != "Electric" else (car1_data['ev_range_km'] / 40.0)
            eff2 = car2_data['mileage_kmpl'] if car2_data['fuel_type'] != "Electric" else (car2_data['ev_range_km'] / 40.0)
            eff1 = eff1 if eff1 > 0 else 15
            eff2 = eff2 if eff2 > 0 else 15
            
            annual_km = daily_km * 365
            fuel_cost1 = (annual_km / eff1) * fuel_price * years
            fuel_cost2 = (annual_km / eff2) * fuel_price * years
            
            chart_cost1 = [(fuel_cost1 / years) * i for i in range(1, 6)]
            chart_cost2 = [(fuel_cost2 / years) * i for i in range(1, 6)]
            
            resale1_3yr = car1_data['price_min'] * (car1_data['resale_3yr'] / 100.0)
            resale1_5yr = car1_data['price_min'] * (car1_data['resale_5yr'] / 100.0)
            resale2_3yr = car2_data['price_min'] * (car2_data['resale_3yr'] / 100.0)
            resale2_5yr = car2_data['price_min'] * (car2_data['resale_5yr'] / 100.0)
            
            emi1 = (car1_data['price_min'] * 0.8) * 0.02
            emi2 = (car2_data['price_min'] * 0.8) * 0.02

    return render_template('index.html', 
                           cars=cars_dropdown, 
                           compared=compared, 
                           car1=car1_data, 
                           car2=car2_data, 
                           winners=winners,
                           chart_cost1=chart_cost1, 
                           chart_cost2=chart_cost2,
                           resale1_3yr=resale1_3yr, 
                           resale1_5yr=resale1_5yr,
                           resale2_3yr=resale2_3yr, 
                           resale2_5yr=resale2_5yr,
                           fuel_cost1=fuel_cost1, 
                           fuel_cost2=fuel_cost2,
                           emi1=emi1, 
                           emi2=emi2,
                           mode=mode)

@app.route('/search')
def search_suggestions():
    query = request.args.get('q', '').lower()
    if len(query) < 2:
        return jsonify([])
        
    conn = get_db_connection()
    rows = conn.execute('SELECT brand, model, variant FROM cars WHERE LOWER(brand) LIKE ? OR LOWER(model) LIKE ? LIMIT 25', (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "value": f"{r['brand']}|{r['model']}|{r['variant']}",
            "display": f"{r['brand']} {r['model']} ({r['variant']})"
        })
    return jsonify(results)

@app.route('/smart-find')
def smart_find():
    budget_min = float(request.args.get('budget_min', 0))
    budget_max = float(request.args.get('budget_max', 250000000))
    
    # FIX 1: If frontend is passing shorthand values (like 64 instead of 6400000), normalize to Lakhs
    if budget_min > 0 and budget_min < 500:
        budget_min = budget_min * 100000
    if budget_max > 0 and budget_max < 500:
        budget_max = budget_max * 100000

    fuel = request.args.get('fuel', 'all').lower()
    segment = request.args.get('segment', 'all')
    
    mileage_min = request.args.get('mileage_min') or \
                  request.args.get('min_mileage') or \
                  request.args.get('fuel_economy') or \
                  request.args.get('min_fuel_economy') or \
                  request.args.get('economy')
                  
    mileage_min = float(mileage_min) if mileage_min else 0
    
    query = "SELECT * FROM cars WHERE price_min >= ? AND price_min <= ?"
    params = [budget_min, budget_max]
    
    if mileage_min > 0:
        query += " AND (mileage_kmpl >= ? OR ev_range_km >= ?)"
        params.extend([mileage_min, mileage_min])

    # FIX 2: Strip out "only" words (e.g., "diesel only" -> "diesel") to match db records perfectly
    if fuel != 'all':
        clean_fuel = fuel.replace('only', '').strip()
        query += " AND LOWER(fuel_type) = ?"
        params.append(clean_fuel)
        
    if segment != 'all':
        query += " AND LOWER(segment) LIKE ?"
        params.append(f'%{segment.lower()}%')
        
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "brand": r['brand'],
            "model": r['model'],
            "variant": r['variant'],
            "segment": r['segment'],
            "safety": r['safety_rating'],
            "price_min": r['price_min'],
            "price_max": r['price_max'],
            "fuel": r['fuel_type'],
            "mileage": f"{r['ev_range_km']} km" if r['fuel_type'] == "Electric" else f"{r['mileage_kmpl']} kmpl",
            "features": r['features']
        })
    return jsonify(results)

import webbrowser
from threading import Timer

def open_browser():
    """Opens the local server URL in the default web browser."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    init_db()
    
    # Wait 1.5 seconds for the server to spin up, then open the browser automatically
    Timer(1.5, open_browser).start()
    
    # CRITICAL: Change debug to False. 
    # PyInstaller apps will break or loop infinitely if debug=True is left on!
    app.run(debug=False, port=5000)