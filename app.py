from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'cars.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite Database with an expansive market variant catalog."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Overwrites clean to prevent data overlap and apply new feature schemas

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
    
    # Diversified master matrix: Entry-level, mass-market, mid-size premium SUVs, and flagship luxury.
    base_cars_data = [
        # === ENTRY LEVEL & BUDGET SEGMENT ===
        ("Maruti", "Alto K10", ["Std", "LXi", "VXi", "VXi+"], "Hatchback", 399000, 24.3, 0, "Petrol", 998, 66, 89, 5, 214, 2, 75, 60),
        ("Maruti", "Wagon R", ["LXi", "VXi", "ZXi", "ZXi+"], "Hatchback", 554000, 24.4, 0, "Petrol", 1197, 89, 113, 5, 341, 2, 74, 59),
        ("Tata", "Tiago", ["XE", "XM", "XT", "XZ+"], "Hatchback", 469000, 19.0, 0, "Petrol", 1199, 85, 113, 5, 242, 4, 66, 52),
        
        # === MASS MARKET POPULAR SEGMENT ===
        ("Maruti", "Swift", ["LXi", "VXi", "ZXi", "ZXi+"], "Hatchback", 649000, 24.8, 0, "Petrol", 1197, 80, 112, 5, 268, 4, 72, 58),
        ("Maruti", "Dzire", ["LXi", "VXi", "ZXi", "ZXi+"], "Sedan", 679000, 24.7, 0, "Petrol", 1197, 80, 112, 5, 382, 5, 71, 57),
        ("Hyundai", "Verna", ["EX", "S", "SX", "SX(O)"], "Sedan", 1100000, 18.6, 0, "Petrol", 1497, 113, 144, 5, 528, 5, 67, 53),

        # === COMPACT & MID-SIZE SUVs ===
        ("Maruti", "Brezza", ["LXi", "VXi", "ZXi", "ZXi+"], "SUV", 849000, 19.8, 0, "Petrol", 1462, 103, 137, 5, 328, 5, 70, 56),
        ("Tata", "Punch", ["Pure", "Adventure", "Accomplished", "Creative"], "SUV", 612000, 20.1, 0, "Petrol", 1199, 87, 115, 5, 366, 5, 67, 53),
        ("Tata", "Nexon", ["Smart", "Pure", "Creative", "Fearless"], "SUV", 800000, 17.4, 0, "Petrol", 1199, 118, 170, 5, 350, 5, 65, 51),
        ("Hyundai", "Creta", ["E", "EX", "S", "SX", "SX(O)"], "SUV", 1100000, 17.4, 0, "Petrol", 1497, 113, 144, 5, 433, 5, 68, 54),
        ("Honda", "Elevate", ["SV", "V", "VX", "ZX"], "SUV", 1199000, 15.3, 0, "Petrol", 1498, 119, 145, 5, 458, 5, 66, 52),
        
        # === PREMIUM MID-SIZE & RUGGED SUVs ===
        ("Tata", "Harrier", ["Smart", "Pure", "Adventure", "Fearless"], "SUV", 1549000, 16.8, 0, "Diesel", 1956, 168, 350, 5, 445, 5, 63, 49),
        ("Mahindra", "Scorpio-N", ["Z2", "Z4", "Z6", "Z8", "Z8 L"], "SUV", 1385000, 14.2, 0, "Diesel", 2198, 172, 400, 7, 460, 5, 69, 55),
        ("Mahindra", "XUV700", ["MX", "AX3", "AX5", "AX7", "AX7 L"], "SUV", 1399000, 16.0, 0, "Diesel", 2184, 185, 420, 7, 570, 5, 68, 54),
        ("Mahindra", "Thar", ["AX Opt", "LX"], "SUV", 1135000, 15.2, 0, "Diesel", 2184, 130, 300, 4, 150, 4, 73, 61),
        
        # === HYBRIDS & MUVs ===
        ("Toyota", "Innova Hycross", ["VX", "ZX", "ZX+"], "MPV", 2599000, 21.1, 0, "Hybrid", 1987, 152, 188, 7, 320, 5, 74, 60),
        ("Maruti", "Grand Vitara", ["Zeta+", "Alpha+"], "SUV", 1820000, 27.9, 0, "Hybrid", 1490, 116, 122, 5, 373, 5, 71, 57),

        # === HIGH-END LUXURY & FLAGSHIPS ===
        ("Mercedes-Benz", "C-Class", ["C200", "C220d"], "Sedan", 6150000, 16.9, 0, "Petrol", 1496, 201, 300, 5, 455, 5, 52, 38),
        ("Mercedes-Benz", "E-Class", ["E200", "E220d", "E350d"], "Sedan", 7850000, 15.0, 0, "Petrol", 1991, 197, 320, 5, 540, 5, 50, 36),
        ("Mercedes-Benz", "S-Class", ["S450e Launch", "S450e AMG Line"], "Sedan", 22000000, 32.2, 0, "Hybrid", 2999, 435, 680, 5, 345, 5, 45, 30),
        ("BMW", "3 Series GL", ["320Li M Sport", "330Li Luxury"], "Sedan", 6060000, 19.6, 0, "Petrol", 1998, 258, 400, 5, 480, 5, 53, 39),
        ("BMW", "7 Series", ["740i M Sport", "740d M Sport"], "Sedan", 18500000, 16.5, 0, "Petrol", 2998, 381, 520, 5, 540, 5, 44, 29),
        ("BMW", "X5", ["xDrive30d", "xDrive40i"], "SUV", 9700000, 12.0, 0, "Diesel", 2993, 286, 650, 5, 650, 5, 48, 34),

        # === PURE ELECTRIC VEHICLES (EVs) ===
        ("MG", "Windsor EV", ["Excite", "Exclusive", "Essence"], "SUV", 1350000, 0, 332, "Electric", 0, 136, 200, 5, 604, 4, 55, 41),
        ("Tata", "Punch EV", ["Smart", "Adventure", "Empowered+"], "SUV", 1099000, 0, 421, "Electric", 0, 122, 190, 5, 366, 5, 58, 44),
        ("Tata", "Nexon EV", ["Creative", "Fearless", "Empowered"], "SUV", 1449000, 0, 489, "Electric", 0, 143, 215, 5, 350, 5, 57, 43),
        ("Mahindra", "BE 6", ["Pack One", "Pack Two", "Pack Three"], "SUV", 1890000, 0, 557, "Electric", 0, 228, 380, 5, 455, 5, 57, 43),
        ("Mahindra", "XEV 9e", ["Pack One", "Pack Two", "Pack Three"], "SUV", 2190000, 0, 542, "Electric", 0, 282, 380, 5, 663, 5, 56, 42)
    ]

    for brand, model, variants, segment, base_price, mileage, ev_range, fuel, cc, power, torque, seating, boot, safety, r3, r5 in base_cars_data:
        for idx, var in enumerate(variants):
            variant_price_min = base_price + (idx * 95000)
            variant_price_max = variant_price_min + 80000
            trans = "Automatic" if (idx >= 2 or fuel == "Electric" or fuel == "Hybrid") else "Manual"
            
            # Scale EV Driving range across different battery configurations
            v_ev_range = ev_range + (idx * 40) if ev_range > 0 else 0
            
            # PROGRESSIVE FEATURE TIERS - Ensures unique content profiles per card grid node
            if fuel == "Electric":
                if idx == 0: trim_feats = "Base Pack • Regenerative Braking • Digital Cluster • LED DRLs"
                elif idx == 1: trim_feats = "Mid Pack • 10.25-inch Touchscreen • Rear Camera • Alloy Wheels • OTA Updates"
                else: trim_feats = "Top Luxury Pack • Panoramic Sunroof • ADAS Suite • Ventilated Seats • V2L Charging"
            else:
                if idx == 0: trim_feats = "Base Trim • Dual Airbags & ABS • Manual AC • Reverse Parking Sensors"
                elif idx == 1: trim_feats = "Mid Trim • Steering Audio Controls • 7-inch Touchscreen Infotainment • Day/Night IRVM"
                elif idx == 2: trim_feats = "Top Trim • Diamond Cut Alloy Wheels • Engine Push Start • Auto Climate Control"
                else: trim_feats = "Premium Trim • Leatherette Seats • Adaptive Cruise Control • Wireless Charger • 360 Camera"

            cursor.execute('''
                INSERT INTO cars (brand, model, variant, segment, price_min, price_max, mileage_kmpl, ev_range_km, fuel_type, engine_cc, power_bhp, torque_nm, transmission, seating, boot_space, safety_rating, resale_3yr, resale_5yr, features)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (brand, model, var, segment, variant_price_min, variant_price_max, mileage, v_ev_range, fuel, cc, power, torque, trans, seating, boot, safety, r3, r5, trim_feats))
            
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    cars = conn.execute("SELECT brand, model, variant FROM cars ORDER BY brand, model, variant").fetchall()
    conn.close()
    options = [{'value': f"{c['brand']}|{c['model']}|{c['variant']}", 'display': f"{c['brand']} {c['model']} - {c['variant']}"} for c in cars]
    return render_template('index.html', cars=options, compared=False)

@app.route('/search')
def search():
    """Asynchronous navbar search completion lookup."""
    q = request.args.get('q', '').strip().lower()
    if len(q) < 2:
        return jsonify([])
        
    conn = get_db_connection()
    query = """
        SELECT brand, model, variant FROM cars 
        WHERE LOWER(brand) LIKE ? OR LOWER(model) LIKE ? OR LOWER(variant) LIKE ? 
        LIMIT 8
    """
    term = f"%{q}%"
    rows = conn.execute(query, (term, term, term)).fetchall()
    conn.close()
    
    return jsonify([{
        'value': f"{r['brand']}|{r['model']}|{r['variant']}",
        'display': f"{r['brand']} {r['model']} - {r['variant']}"
    } for r in rows])

@app.route('/compare')
def compare():
    """Handles deep-dive split comparison logic math payloads."""
    car1_raw = request.args.get('car1', '')
    car2_raw = request.args.get('car2', '')
    
    if not car1_raw or not car2_raw:
        return "Error: Two cars must be specified.", 400
        
    b1, m1, v1 = car1_raw.split('|')
    b2, m2, v2 = car2_raw.split('|')
    
    daily_km = float(request.args.get('daily_km', 40))
    fuel_price = float(request.args.get('fuel_price', 103))
    years = int(request.args.get('years', 5))
    mode = request.args.get('mode', 'quick')
    
    conn = get_db_connection()
    car1 = conn.execute("SELECT * FROM cars WHERE brand=? AND model=? AND variant=?", (b1, m1, v1)).fetchone()
    car2 = conn.execute("SELECT * FROM cars WHERE brand=? AND model=? AND variant=?", (b2, m2, v2)).fetchone()
    all_cars = conn.execute("SELECT brand, model, variant FROM cars ORDER BY brand, model, variant").fetchall()
    conn.close()
    
    options = [{'value': f"{c['brand']}|{c['model']}|{c['variant']}", 'display': f"{c['brand']} {c['model']} - {c['variant']}"} for c in all_cars]
    
    if not car1 or not car2:
        return "Error: Selected vehicles could not be located in database.", 404

    # Financial Cost Estimation Equations
    def calc_running_cost(car):
        if car['fuel_type'] == 'Electric':
            cost_per_km = 8.0 / (car['ev_range_km'] / 40.0 if car['ev_range_km'] > 0 else 5.0)
        else:
            cost_per_km = fuel_price / car['mileage_kmpl'] if car['mileage_kmpl'] > 0 else 7.0
        return daily_km * 365 * cost_per_km * years

    fuel_cost1 = calc_running_cost(car1)
    fuel_cost2 = calc_running_cost(car2)
    
    chart_cost1 = [(fuel_cost1 / years) * i for i in range(1, 6)]
    chart_cost2 = [(fuel_cost2 / years) * i for i in range(1, 6)]

    resale1_3yr = car1['price_min'] * (car1['resale_3yr'] / 100.0)
    resale1_5yr = car1['price_min'] * (car1['resale_5yr'] / 100.0)
    resale2_3yr = car2['price_min'] * (car2['resale_3yr'] / 100.0)
    resale2_5yr = car2['price_min'] * (car2['resale_5yr'] / 100.0)

    emi1, emi2 = 0, 0
    dp_pct = float(request.args.get('down_payment', 20))
    loan_tenure = int(request.args.get('loan_tenure', 60))
    roi = float(request.args.get('interest_rate', 9.5))
    
    if mode == 'detail':
        def calc_emi(price):
            principal = price * (1 - (dp_pct / 100.0))
            r = (roi / 12) / 100
            return (principal * r * ((1 + r) ** loan_tenure)) / (((1 + r) ** loan_tenure) - 1)
        emi1 = calc_emi(car1['price_min'])
        emi2 = calc_emi(car2['price_min'])

    winners = {
        'price': 'car1' if car1['price_min'] < car2['price_min'] else ('car2' if car1['price_min'] > car2['price_min'] else 'tie'),
        'mileage': 'car1' if (car1['mileage_kmpl'] > car2['mileage_kmpl'] or car1['ev_range_km'] > car2['ev_range_km']) else 'car2',
        'engine': 'car1' if car1['engine_cc'] > car2['engine_cc'] else ('car2' if car1['engine_cc'] < car2['engine_cc'] else 'tie'),
        'power': 'car1' if car1['power_bhp'] > car2['power_bhp'] else ('car2' if car1['power_bhp'] < car2['power_bhp'] else 'tie'),
        'torque': 'car1' if car1['torque_nm'] > car2['torque_nm'] else ('car2' if car1['torque_nm'] < car2['torque_nm'] else 'tie'),
        'safety': 'car1' if car1['safety_rating'] > car2['safety_rating'] else ('car2' if car1['safety_rating'] < car2['safety_rating'] else 'tie'),
        'boot': 'car1' if car1['boot_space'] > car2['boot_space'] else ('car2' if car1['boot_space'] < car2['boot_space'] else 'tie')
    }

    return render_template(
        'index.html', cars=options, compared=True, mode=mode,
        car1=car1, car2=car2, fuel_cost1=fuel_cost1, fuel_cost2=fuel_cost2,
        chart_cost1=chart_cost1, chart_cost2=chart_cost2,
        resale1_3yr=resale1_3yr, resale1_5yr=resale1_5yr,
        resale2_3yr=resale2_3yr, resale2_5yr=resale2_5yr,
        emi1=emi1, emi2=emi2, winners=winners,
        daily_km=daily_km, fuel_price=fuel_price, years=years,
        down_payment_pct=dp_pct, loan_tenure=loan_tenure, interest_rate=roi
    )

@app.route('/smart-find')
def smart_find():
    """Reactive query engine matching frontend parameters across a dual budget range."""
    budget_min = float(request.args.get('budget_min', 0))
    budget_max = float(request.args.get('budget_max', 25000000))
    fuel = request.args.get('fuel', 'all').strip().lower()
    segment = request.args.get('segment', 'all').strip().lower()
    
    query = "SELECT * FROM cars WHERE price_min >= ? AND price_min <= ?"
    params = [budget_min, budget_max]

    if fuel == 'electric':
        min_range = float(request.args.get('ev_range', 0))
        query += " AND fuel_type = 'Electric' AND ev_range_km >= ?"
        params.append(min_range)
    elif fuel in ['petrol', 'diesel', 'hybrid']:
        min_mileage = float(request.args.get('mileage', 0))
        query += " AND LOWER(fuel_type) = ? AND mileage_kmpl >= ?"
        params.extend([fuel, min_mileage])
    else:
        min_mileage = float(request.args.get('mileage', 0))
        query += " AND (mileage_kmpl >= ? OR ev_range_km >= 200)"
        params.append(min_mileage)

    if segment != 'all':
        query += " AND LOWER(segment) = ?"
        params.append(segment)

    query += " ORDER BY safety_rating DESC, price_min ASC"

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([{
        'brand': r['brand'], 'model': r['model'], 'variant': r['variant'], 'segment': r['segment'],
        'fuel': r['fuel_type'], 'price_min': r['price_min'], 'price_max': r['price_max'],
        'mileage': f"{r['mileage_kmpl']} Kmpl" if r['fuel_type'] != 'Electric' else f"{r['ev_range_km']} km Range",
        'safety': r['safety_rating'], 'features': r['features']
    } for r in rows])

if __name__ == '__main__':
    # Automatically opens the user's default browser on launch
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open_browser("http://127.0.0.1:5000/")

    # Delay browser launch by 1.5 seconds to give the Flask server time to spin up
    Timer(1.5, open_browser).start()
    
    # Run server without debug mode so friends don't see raw code errors if something misbehaves
    app.run(debug=False, port=5000)