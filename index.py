from flask import Flask, render_template, session, redirect, url_for, request, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션용

# 샘플 메뉴 데이터
MENU = [
	{'id': 1, 'name': '아메리카노', 'price': 3000},
	{'id': 2, 'name': '카페라떼', 'price': 3500},
	{'id': 3, 'name': '녹차', 'price': 3200},
	{'id': 4, 'name': '샌드위치', 'price': 4500},
	{'id': 5, 'name': '', 'price': 0}
]

@app.route('/')
def index():
	return render_template('menu.html', menu=MENU)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
	item_id = request.json.get('id')
	try:
		item_id = int(item_id)
	except (TypeError, ValueError):
		return jsonify({'success': False, 'message': '잘못된 메뉴 ID입니다.'}), 400
	item = next((m for m in MENU if m['id'] == item_id), None)
	if not item:
		return jsonify({'success': False, 'message': '메뉴를 찾을 수 없습니다.'}), 404
	cart = session.get('cart', [])
	cart.append(item)
	session['cart'] = cart
	return jsonify({'success': True, 'cart': cart})

@app.route('/cart')
def cart():
	cart = session.get('cart', [])
	return render_template('cart.html', cart=cart)

@app.route('/checksout', methods=['POST'])
def checkout():
	cart = session.get('cart', [])
	session.pop('cart', None)  
	return render_template('complete.html', cart=cart)

if __name__ == '__main__':
	app.run(debug=True)
