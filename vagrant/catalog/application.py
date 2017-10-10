from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

app = Flask(__name__)

# Connect to database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON API for categories
@app.route('/categories.json')
def categoryJSON():
    category = session.query(Category).all()
    return jsonify(category=[c.serialize for c in category])


# JSON API for items within a cateogry
@app.route('/category/<int:category_id>.json')
def categoryItemsJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Category_Items=[i.serialize for i in items])

# JSON API for an item
@app.route('/category/<int:category_id>/item/<int:item_id>.json')
def ItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).one()
    return jsonify(Item=item.serialize)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)