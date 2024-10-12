from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    addresses = db.relationship('Address', backref='contact', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    new_contact = Contact(
        name=data['name'],
        phone=data['phone'],
        email=data['email']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"message": "Contact added successfully!"}), 201

@app.route('/contacts/<int:contact_id>/addresses', methods=['POST'])
def add_address(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    new_address = Address(
        street=data['street'],
        city=data['city'],
        state=data['state'],
        contact_id=contact.id
    )
    db.session.add(new_address)
    db.session.commit()
    return jsonify({"message": "Address added successfully!"}), 201

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    result = []
    for contact in contacts:
        addresses = [{"street": a.street, "city": a.city, "state": a.state} for a in contact.addresses]
        result.append({
            "name": contact.name,
            "phone": contact.phone,
            "email": contact.email,
            "addresses": addresses
        })
    return jsonify(result), 200

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    addresses = [{"street": a.street, "city": a.city, "state": a.state} for a in contact.addresses]
    result = {
        "name": contact.name,
        "phone": contact.phone,
        "email": contact.email,
        "addresses": addresses
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)