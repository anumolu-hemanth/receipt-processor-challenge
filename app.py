from flask import Flask, request, jsonify
import uuid
import json
import math

app = Flask(__name__)
receipts = {}


@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt_data = request.json
    
    receipt_id = str(uuid.uuid4())
    
    receipts[receipt_id] = receipt_data
    
    return jsonify({"id": receipt_id})


@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    receipt_data = receipts.get(receipt_id)
    
    if receipt_data is None:
        return jsonify({"error": "Receipt not found"}), 404
    
    points = calculate_points(receipt_data)
    
    return jsonify({"points": points})


def calculate_points(receipt_data):
    points = 0
    
    points += sum(c.isalnum() for c in receipt_data.get('retailer'))
    print("characters points: "+str(points))
    total = float(receipt_data.get('total'))
    if total.is_integer():
        points += 50
    
    if total % 0.25 == 0:
        points += 25
    print("total points: "+str(points))
    points += len(receipt_data.get('items', [])) // 2 * 5
    print("items pairs points: "+str(points))
    for item in receipt_data.get('items', []):
        if len(item.get('shortDescription').strip()) % 3 == 0:
            points += math.ceil(float(item.get('price')) * 0.2)
    print("items points: "+str(points))
    purchase_date = receipt_data.get('purchaseDate')
    if int(purchase_date.split('-')[2]) % 2 != 0:
        points += 6
    print("date points: "+str(points))
    purchase_time = receipt_data.get('purchaseTime')
    if int(purchase_time.split(':')[0]) >= 14 and int(purchase_time.split(':')[0]) < 16:
        points += 10
    print("time points: "+str(points))
    return points


if __name__ == '__main__':
    app.run(debug=True)
