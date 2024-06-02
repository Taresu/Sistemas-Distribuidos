from auth import verify_signature
from flask import Flask, jsonify, request
from models import Item
from sse import notify


def setup_routes(app, db):
    @app.route('/items', methods=['POST'])
    def create_item():
        data = request.json
        if verify_signature(data['message'], data['signature']):
            new_item = Item(name=data['name'], description=data['description'])
            db.session.add(new_item)
            db.session.commit()
            notify('item_created', {'name': data['name']})
            return jsonify({'message': 'Item created!'}), 201
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    @app.route('/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

    @app.route('/items/<int:id>', methods=['PUT'])
    def update_item(id):
        data = request.json
        item = Item.query.get(id)
        if item:
            item.name = data['name']
            item.description = data['description']
            db.session.commit()
            notify('item_updated', {'id': id, 'name': data['name']})
            return jsonify({'message': 'Item updated!'})
        return jsonify({'message': 'Item not found'}), 404

    @app.route('/items/<int:id>', methods=['DELETE'])
    def delete_item(id):
        item = Item.query.get(id)
        if item:
            db.session.delete(item)
            db.session.commit()
            notify('item_deleted', {'id': id})
            return jsonify({'message': 'Item deleted!'})
        return jsonify({'message': 'Item not found'}), 404