from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12668248:9z7WzgVFEu@sql12.freesqldatabase.com/sql12668248'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280  
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20   
app.config['SQLALCHEMY_POOL_SIZE'] = 50      
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

# Root path
@app.route('/')
def home():
    return 'Welcome to the Library API!'

# Endpoint 1: To Retrieve All Books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    with app.app_context():
        books = Book.query.all()
        book_list = [{'id': book.id, 'name': book.name, 'author': book.author, 'description': book.description} for book in books]
        return jsonify({'books': book_list})

# Endpoint 2: To Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    data = request.json

    # Validate request payload
    if 'name' not in data or 'author' not in data:
        return jsonify({'error': 'name and author are required'}), 400

    if 'description' not in data:
        return jsonify({'error': 'description required'}), 400      

    # Check for duplicate entry
    with app.app_context():
        existing_book = Book.query.filter_by(name=data['name']).first()
        if existing_book:
            return jsonify({'error': 'Book already exists'}), 400

        generated_id = secrets.token_urlsafe(5).upper()

        # Add new book to the database
        new_book = Book(id=generated_id,name=data['name'], author=data['author'], description=data['description'])
        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book added successfully'}), 201

# Endpoint 3: To Update Book Details
@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json

    # Validate request payload
    if 'name' not in data or 'author' not in data:
        return jsonify({'error': 'name and author are required'}), 400

    if 'description' not in data:
        return jsonify({'error': 'description required'}), 400    

    # Retrieve the book from the database
    with app.app_context():
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Update book details
        book.name = data['name']
        book.author = data['author']
        book.description = data['description']
        db.session.commit()

        return jsonify({'message': 'Book updated successfully'})

# Run the app
if _name_ == '_main_':
    app.run(debug=True)