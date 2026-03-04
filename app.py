from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = "bitrade_ultra_premium_key"

# Configuration
ADMIN_ADDRESS = "TDo2pnvaAZRNzmL1a47SmYbLcBftJF7pYa"
MASTER_USDT_ADDR = "TCxzW5RzSdzHxzaVXFcYeNH5VWdf6oGcgL"

# Mock Database
users = {} 
deposits = []

@app.route('/')
def index():
    if 'user' in session: return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    w = request.json.get('wallet')
    ref = request.json.get('ref')
    if not w or not w.startswith('T') or len(w) != 34:
        return jsonify({"error": "Invalid TRC20 Address"}), 400
    if w not in users:
        users[w] = {
            'wallet': w, 'balance': 0.0, 'referral_code': str(uuid.uuid4())[:6].upper(),
            'referred_by': ref, 'total_referrals': 0, 'referral_earnings': 0.0, 'plans': []
        }
        if ref:
            for u in users.values():
                if u['referral_code'] == ref: u['total_referrals'] += 1
    session['user'] = w
    return jsonify({"success": True})

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('index'))
    return render_template('dashboard.html', user=users[session['user']], admin_addr=ADMIN_ADDRESS, admin_wallet=MASTER_USDT_ADDR)

@app.route('/admin')
def admin():
    if session.get('user') != ADMIN_ADDRESS: return "Forbidden", 403
    return render_template('admin.html', deposits=deposits, admin_addr=ADMIN_ADDRESS)

@app.route('/submit_dep', methods=['POST'])
def submit_dep():
    data = request.json
    deposits.append({"id": len(deposits), "wallet": session['user'], "txid": data['txid'], "amount": float(data['amount']), "plan": data['plan'], "status": "Pending"})
    return jsonify({"success": True})

@app.route('/approve/<int:did>')
def approve(did):
    if session.get('user') != ADMIN_ADDRESS: return redirect('/')
    for d in deposits:
        if d['id'] == did and d['status'] == "Pending":
            d['status'] = "Approved"
            users[d['wallet']]['plans'].append({
                "plan_name": d['plan'], "amount": d['amount'],
                "end_time": (datetime.now() + timedelta(days=20)).isoformat()
            })
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)