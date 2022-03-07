# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Customer(db.Model):
    __tablename__ = 'customers'

    customerNumber = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(50), nullable=False)
    contactLastName = db.Column(db.String(50), nullable=False)
    contactFirstName = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    addressLine1 = db.Column(db.String(50), nullable=False)
    addressLine2 = db.Column(db.String(50))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50))
    postalCode = db.Column(db.String(15))
    country = db.Column(db.String(50), nullable=False)
    salesRepEmployeeNumber = db.Column(db.ForeignKey('employees.employeeNumber'), index=True)
    creditLimit = db.Column(db.Numeric(10, 2))

    employee = db.relationship('Employee', primaryjoin='Customer.salesRepEmployeeNumber == Employee.employeeNumber', backref='customers')



class Employee(db.Model):
    __tablename__ = 'employees'

    employeeNumber = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    officeCode = db.Column(db.ForeignKey('offices.officeCode'), nullable=False, index=True)
    reportsTo = db.Column(db.ForeignKey('employees.employeeNumber'), index=True)
    jobTitle = db.Column(db.String(50), nullable=False)

    office = db.relationship('Office', primaryjoin='Employee.officeCode == Office.officeCode', backref='employees')
    parent = db.relationship('Employee', remote_side=[employeeNumber], primaryjoin='Employee.reportsTo == Employee.employeeNumber', backref='employees')



class Office(db.Model):
    __tablename__ = 'offices'

    officeCode = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    addressLine1 = db.Column(db.String(50), nullable=False)
    addressLine2 = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50), nullable=False)
    postalCode = db.Column(db.String(15), nullable=False)
    territory = db.Column(db.String(10), nullable=False)



class Orderdetail(db.Model):
    __tablename__ = 'orderdetails'

    orderNumber = db.Column(db.ForeignKey('orders.orderNumber'), primary_key=True, nullable=False)
    productCode = db.Column(db.ForeignKey('products.productCode'), primary_key=True, nullable=False, index=True)
    quantityOrdered = db.Column(db.Integer, nullable=False)
    priceEach = db.Column(db.Numeric(10, 2), nullable=False)
    orderLineNumber = db.Column(db.SmallInteger, nullable=False)

    order = db.relationship('Order', primaryjoin='Orderdetail.orderNumber == Order.orderNumber', backref='orderdetails')
    product = db.relationship('Product', primaryjoin='Orderdetail.productCode == Product.productCode', backref='orderdetails')



class Order(db.Model):
    __tablename__ = 'orders'

    orderNumber = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.Date, nullable=False)
    requiredDate = db.Column(db.Date, nullable=False)
    shippedDate = db.Column(db.Date)
    status = db.Column(db.String(15), nullable=False)
    comments = db.Column(db.Text)
    customerNumber = db.Column(db.ForeignKey('customers.customerNumber'), nullable=False, index=True)

    customer = db.relationship('Customer', primaryjoin='Order.customerNumber == Customer.customerNumber', backref='orders')



class Payment(db.Model):
    __tablename__ = 'payments'

    customerNumber = db.Column(db.ForeignKey('customers.customerNumber'), primary_key=True, nullable=False)
    checkNumber = db.Column(db.String(50), primary_key=True, nullable=False)
    paymentDate = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    customer = db.relationship('Customer', primaryjoin='Payment.customerNumber == Customer.customerNumber', backref='payments')



class Productline(db.Model):
    __tablename__ = 'productlines'

    productLine = db.Column(db.String(50), primary_key=True)
    textDescription = db.Column(db.String(4000))
    htmlDescription = db.Column(db.String)
    image = db.Column(db.MEDIUMBLOB)



class Product(db.Model):
    __tablename__ = 'products'

    productCode = db.Column(db.String(15), primary_key=True)
    productName = db.Column(db.String(70), nullable=False)
    productLine = db.Column(db.ForeignKey('productlines.productLine'), nullable=False, index=True)
    productScale = db.Column(db.String(10), nullable=False)
    productVendor = db.Column(db.String(50), nullable=False)
    productDescription = db.Column(db.Text, nullable=False)
    quantityInStock = db.Column(db.SmallInteger, nullable=False)
    buyPrice = db.Column(db.Numeric(10, 2), nullable=False)
    MSRP = db.Column(db.Numeric(10, 2), nullable=False)

    productline = db.relationship('Productline', primaryjoin='Product.productLine == Productline.productLine', backref='products')
