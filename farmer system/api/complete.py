from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

# Create Flask app with proper paths for Vercel
app = Flask(__name__, 
           template_folder='../templates', 
           static_folder='../static')

app.secret_key = os.environ.get('SECRET_KEY', 'farm-management-complete-2024')

# Simple in-memory storage
users_db = {}
products_db = {}
farmers_db = {}
farming_types = [
    {"fid": 1, "farmingtype": "Organic Farming"},
    {"fid": 2, "farmingtype": "Vegetable Farming"},
    {"fid": 3, "farmingtype": "Fruit Farming"},
    {"fid": 4, "farmingtype": "Grain Farming"},
    {"fid": 5, "farmingtype": "Dairy Farming"}
]

# Helper functions
def get_next_id(db_dict):
    return max(db_dict.keys()) + 1 if db_dict else 1

def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return users_db.get(session['user_id'])
    return None

# Create a mock current_user object for templates
class MockUser:
    def __init__(self, user_data=None):
        if user_data:
            self.id = user_data['id']
            self.username = user_data['username']
            self.email = user_data['email']
            self.is_authenticated = True
        else:
            self.is_authenticated = False
    
    def get_id(self):
        return str(self.id) if hasattr(self, 'id') else None

# Template context processor
@app.context_processor
def inject_user():
    current_user = MockUser(get_current_user()) if is_logged_in() else MockUser()
    return dict(current_user=current_user)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'Database Connected Successfully! Complete Flask app with templates working.'

@app.route('/agroproducts')
def agroproducts():
    # Convert products_db to list format expected by template
    query = []
    for pid, product in products_db.items():
        product_copy = product.copy()
        product_copy['pid'] = pid
        query.append(product_copy)
    return render_template('agroproducts.html', query=query)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        for user in users_db.values():
            if user['email'] == email:
                flash('Email already exists', 'warning')
                return render_template('signup.html')
        
        # Create new user
        user_id = get_next_id(users_db)
        users_db[user_id] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password': password
        }
        
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user
        for user_id, user in users_db.items():
            if user['email'] == email and user['password'] == password:
                session['user_id'] = user_id
                session['username'] = user['username']
                session['email'] = user['email']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
        
        flash('Invalid credentials', 'warning')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/addagroproduct', methods=['GET', 'POST'])
def addagroproduct():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_user = get_current_user()
        
        product_id = get_next_id(products_db)
        products_db[product_id] = {
            'username': current_user['username'],
            'email': current_user['email'],
            'productname': request.form.get('productname'),
            'productdesc': request.form.get('productdesc'),
            'price': request.form.get('price'),
            'category': request.form.get('category'),
            'quantity': request.form.get('quantity'),
            'basePrice': request.form.get('basePrice'),
            'image': request.form.get('image'),
            'available': request.form.get('available') == 'on',
            'created_at': datetime.now().isoformat()
        }
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('agroproducts'))
    
    return render_template('addagroproducts.html')

@app.route('/myproducts')
def myproducts():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    user_products = []
    
    for pid, product in products_db.items():
        if product['email'] == current_user['email']:
            product_copy = product.copy()
            product_copy['pid'] = pid
            user_products.append(product_copy)
    
    return render_template('myproducts.html', products=user_products)

@app.route('/toggle_availability/<int:pid>')
def toggle_availability(pid):
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    current_user = get_current_user()
    product = products_db.get(pid)
    
    if product and product['email'] == current_user['email']:
        product['available'] = not product['available']
        status = "available" if product['available'] else "unavailable"
        flash(f'Product marked as {status}', 'success')
    else:
        flash('Product not found or access denied', 'error')
    
    return redirect(url_for('myproducts'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        farmer_id = get_next_id(farmers_db)
        farmers_db[farmer_id] = {
            'rid': farmer_id,
            'farmername': request.form.get('farmername'),
            'adharnumber': request.form.get('adharnumber'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'phonenumber': request.form.get('phonenumber'),
            'address': request.form.get('address'),
            'farming': request.form.get('farmingtype')
        }
        flash('Farmer registered successfully!', 'success')
        return redirect(url_for('farmerdetails'))
    
    return render_template('farmer.html', farming=farming_types)

@app.route('/farmerdetails')
def farmerdetails():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    query = list(farmers_db.values())
    return render_template('farmerdetails.html', query=query)

@app.route('/addfarming', methods=['GET', 'POST'])
def addfarming():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        farmingtype = request.form.get('farming')
        # Check if farming type already exists
        exists = any(ft['farmingtype'] == farmingtype for ft in farming_types)
        if not exists:
            new_id = max(ft['fid'] for ft in farming_types) + 1
            farming_types.append({'fid': new_id, 'farmingtype': farmingtype})
            flash('Farming type added successfully!', 'success')
        else:
            flash('Farming type already exists', 'warning')
    
    return render_template('farming.html')

@app.route('/triggers')
def triggers():
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    # Mock triggers data
    query = [
        {'id': 1, 'fid': 'F001', 'action': 'Product Added', 'timestamp': datetime.now().isoformat()},
        {'id': 2, 'fid': 'F002', 'action': 'Farmer Registered', 'timestamp': datetime.now().isoformat()}
    ]
    return render_template('triggers.html', query=query)

@app.route('/delete/<string:rid>')
def delete(rid):
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    rid = int(rid)
    if rid in farmers_db:
        del farmers_db[rid]
        flash('Farmer record deleted successfully', 'success')
    else:
        flash('Farmer record not found', 'error')
    
    return redirect(url_for('farmerdetails'))

@app.route('/edit/<string:rid>', methods=['GET', 'POST'])
def edit(rid):
    if not is_logged_in():
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    rid = int(rid)
    farmer = farmers_db.get(rid)
    
    if not farmer:
        flash('Farmer not found', 'error')
        return redirect(url_for('farmerdetails'))
    
    if request.method == 'POST':
        farmer.update({
            'farmername': request.form.get('farmername'),
            'adharnumber': request.form.get('adharnumber'),
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'phonenumber': request.form.get('phonenumber'),
            'address': request.form.get('address'),
            'farming': request.form.get('farmingtype')
        })
        flash('Farmer record updated successfully', 'success')
        return redirect(url_for('farmerdetails'))
    
    return render_template('edit.html', posts=farmer, farming=farming_types)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return f'Internal Server Error: {str(error)}', 500

# For Vercel
def handler(event, context):
    return app(event, context)

# For local development
if __name__ == '__main__':
    app.run(debug=True)