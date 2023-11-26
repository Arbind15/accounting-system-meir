import base64
from datetime import datetime
import json
import os

import webview
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, SupplierDetail

winh = webview.screens[0].height
winw = webview.screens[0].width
supplier_win = None
add_supplier_win=None


# Replace 'sqlite:///your_database_name.db' with the actual database connection string
engine = create_engine('sqlite:///data.db')
# Bind the engine to the Base class
Base.metadata.bind = engine
# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()


def py_js_str(py_string):
    # Replace special characters with their escaped Unicode sequences
    # Encode the string as bytes
    encoded_bytes = py_string.encode('utf-8')
    # Base64 encode the bytes
    js_string = base64.b64encode(encoded_bytes).decode('utf-8')

    return js_string

def loadSuppliers():
    global supplier_win
    suppliers = session.query(SupplierDetail.id, SupplierDetail.supplier_name).order_by(SupplierDetail.supplier_name).all()
    sups=[]
    for supplier in suppliers:
        supplier_id, supplier_name = supplier
        sups.append({
            "id":supplier_id,
            "name":supplier_name
        })
    sups=py_js_str(json.dumps(sups))
    print('h ',sups)
    supplier_win.evaluate_js("populateSuppliers('"+str(sups)+"');")


def runtimes():
    global info_window, manager_window, model_path, model, recognizer
    loadSuppliers()

class API():
    def cancelAddSupplier(self, data):
        global supplier_win, add_supplier_win
        add_supplier_win.destroy()
        add_supplier_win=None
        supplier_win.show()

    def addSupplier(self, data):
        global supplier_win, add_supplier_win
        api = API()
        if add_supplier_win!=None:
            add_supplier_win.destroy()
        add_supplier_win=webview.create_window("Add Supplier", url="add_supplier.html", width=int(winw * 0.3),
                                         height=int(winh * 0.5), js_api=api, frameless=True)

    def saveSupplier(self, data):
        global session, add_supplier_win, supplier_win
        try:
            data=json.loads(data)
            new_supplier = SupplierDetail(
                supplier_name=data['s-name'],
                invoice_date=datetime.strptime(data['i-date'], "%Y-%m-%d").date(),
                invoice_type=data['i-type'],
                invoice_number=data['i-num'],
                building_name=data['b-name'],
                budget_type_1=data['b1-type'],
                budget_type_2=data['b2-type'],
                supplier_type=data['s-type'],
                account_details=data['a-detail'],
                affiliation_period=data['a-period']
            )
            session.add(new_supplier)
            session.commit()
            add_supplier_win.destroy()
            add_supplier_win=None
            supplier_win.show()
            supplier_win.evaluate_js("alert('Supplier added!');")
            loadSuppliers()

        except Exception as e:
            add_supplier_win.destroy()
            add_supplier_win = None
            supplier_win.show()
            e = "Error: " + str(type(e).__name__)
            supplier_win.evaluate_js("alert('" + e + "');")


def create_window():
    global supplier_win
    api = API()
    # window=webview.create_window("Pywebview Example", url="main.html", width=800, height=600, js_api=api)
    # commit_window = webview.create_window("Commits", url="commit.html", width=800, height=900, js_api=api)
    supplier_win = webview.create_window("Suppliers", url="supplier.html", width=int(winw * 0.6),
                                         height=int(winh * 0.8), js_api=api)
    supplier_win.events.closed += on_closed
    webview.start(runtimes, debug=True)


def on_closed():
    os._exit(0)


if __name__ == "__main__":
    create_window()
