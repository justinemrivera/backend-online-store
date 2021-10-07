from mock_data import mock_data
import json
from flask import Flask, render_template, abort, request
from flask_cors import CORS
from config import db, parse_json
app = Flask(__name__)
CORS(app)

me = {
    "name": "Justine",
    "last": "Rivera",
    "email": "test@mail.com",
    "age": 30,
    "hobbies": [],
    "address": {
            "street": "main",
            "number": "42"
    }
}


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html2")


@app.route("/about")
def about():
    return f"{me['name']} {me['last']}"


@app.route("/about/email")
def get_email():
    return me["email"]


@app.route("/about/address")
def get_addres():
    address = me["address"]
    return address["number"] + " " + address["street"]

# API methods


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    # read products from database and return it
    cursor = db.products.find({})  # get all records/documents
    catalog = []
    for prod in cursor:
        catalog.append(prod)

    #list comprehensions
    #catalog = [prod for prod in cursor] #only works on python 
    return parse_json(catalog)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    if not "price" in product or product["price"] <= 0:
        abort(400, "price is required and should be greater than zero")
    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and should be at least 5 chars long")

    #save product into DB
    #MONOGDB adds a _id with a unique value 
    db.products.insert_one(product)
    
    return parse_json(product)

# end point /api/categories
# return a string
# a for loop and print each dictionary
# print just the category


@app.route("/api/categories")
def get_categories():
    cursor = db.products.find({})
    categories = []
    for product in cursor:
        cat = product["category"]
        if cat not in categories:
            categories.append(cat)

    return parse_json(categories)


@app.route("/api/products/<id>")
def get_by_id(id):
    product = db.products.find_one({"_id": id})
    # find the product with such id
    # return the product as jsn string


    if not product:
        abort(404)
    return parse_json(product)


@app.route("/api/catalog/<cat>")
def get_by_category(cat):
    cursor = db.products.find({"category" : cat})
    prods = []
    for prod in cursor:
        prods.append(prod)
    
           
    return parse_json(prods)


@app.route("/api/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    cheapest = cursor[0]
    for prod in cursor:
        if prod["price"] < cheapest["price"]:
            cheapest = prod
       
    return parse_json(cheapest)

@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    if not "code" in coupon or len( coupon["code"] ) <5:
        abort(400,"Code is required and should be at least 5 chars long")
    if not "discount" in coupon or coupon["discount"] <= 0:
        abort (400,"Discount is required and should be greater than zero")
    db.couponCodes.insert_one(coupon)

    return parse_json(coupon)

@app.route("/api/couponCode", methods=["GET"])
def get_coupons():
    cursor = db.couponCodes.find({})
    codes = []
    for code in cursor:
        codes.append(code) 

    return parse_json(codes)


#/api/couponCode/abcde
@app.route("/api/couponCode/<code>")
def validate_coupon(code):
    coupon = db.couponCodes.find_one({"code":code})
    # find the product with such id
    # return the product as jsn string


    if not coupon:
        abort(404, "Invalid coupon")
    return parse_json(coupon)

@app.route("/api/orders", methods=["POST"])
def save_Order():
    order = request.get_json()
    db.orders.insert_one(order)

    return parse_json(order)




@app.route("/api/test/loadData")
def load_data():
    #return "Data already loaded"
    # load every product in mock_data into the database
    for prod in mock_data:
        db.products.insert_one(prod)
    return "Data loaded"


app.run(debug=True)

# hacker rank
