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
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])


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


# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
#    if 'username' not in login_session:
 #       return render_template('publiccategories.html', categories=categories)
 #   else:
    return render_template('categories.html', categories=categories)


# Create a category
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    categoryToEdit = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            categoryToEdit.name = request.form['name']
            session.add(categoryToEdit)
            session.commit()
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=categoryToEdit)


# Delete a category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)


# Show all items within a category
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category, category_id = category_id)


# Create an item
@app.route('/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newMenuItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form[
                'description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)


# Edit an item
@app.route('/categories/<int:category_id>/<int:item_id>/')
@app.route('/categories/<int:category_id>/items/<int:item_id>/')
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToEdit = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('edititem.html', item=itemToEdit, category=category)

# Delete an item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete, category=category)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)