# Suas rotas aqui

from math import prod
from flask import Flask, jsonify, request
from http import HTTPStatus

from app.products import read_events_from_csv, update_event_in_csv, validate_keys, write_event_in_csv, normalize_variables

app = Flask(__name__)


@app.get('/products')
def products():
    events = read_events_from_csv()

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 3))

    itens = []
    
    for index in range(per_page):
        itens.append(events[index + ((page - 1) * per_page)])

    for product in itens:
        normalize_variables(product)

    return jsonify(itens), HTTPStatus.OK


@app.get('/products/<int:id>')
def product_by_id(id):
    events = read_events_from_csv()
    product = []

    for item in events:
        if int(item['id']) == id:
            product.append(item)
    
    if len(product) == 0:
        return {"msg": 'product not found'}, HTTPStatus.BAD_REQUEST

    normalize_variables(product[0])

    return jsonify(product), HTTPStatus.OK


@app.post('/products')
def create_product():
    expected_keys = {'name', 'price'}
    data = request.get_json()

    try:
        validate_keys(data, expected_keys)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST
    
    events = read_events_from_csv()
    last_event = events[-1]
    data['id'] = str(int(last_event['id']) + 1)

    write_event_in_csv(data)

    normalize_variables(data)

    return data, HTTPStatus.CREATED


@app.patch('/products/<product_id>')
def update_product(product_id):
    data = request.get_json()
    events = read_events_from_csv()
    product = []

    for item in events:
        if item['id'] == product_id:
            item['name'] = data.get('name', item['name'])
            item['price'] = data.get('price', item['price'])
            product.append(item)

    if len(product) == 0:
        return {"error": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND

    update_event_in_csv(events)

    normalize_variables(product[0])

    return jsonify(product), HTTPStatus.OK


@app.delete('/products/<product_id>')
def delete_product(product_id):
    events = read_events_from_csv()
    product = []

    for index, item in enumerate(events):
        if item['id'] == product_id:
            product.append(events.pop(index))
    
    if len(product) == 0:
        return {"error": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND

    update_event_in_csv(events)

    normalize_variables(product[0])

    return product[0], HTTPStatus.OK