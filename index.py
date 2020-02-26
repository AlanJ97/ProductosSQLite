from tkinter import ttk
from tkinter import *
import sqlite3

class Product:
    db_name = 'database.db'
    def __init__(self, window):
        self.wind = window
        self.wind.title("Products APplications")
        #crating a Frame container
        frame = LabelFrame(self.wind, text = "Register a new product")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #Name Input
        Label(frame, text = "Name : ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        #Price Input
        Label(frame, text = "Price : ").grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        #Button Add product
        ttk.Button(frame, text = "Save product", command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        #Output messages
        self.message = Label(text = "", fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text= 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)
        #buttons delete and edit
        ttk.Button(text  = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W +E)
        ttk.Button(text  = 'EDIT').grid(row = 5, column = 1, sticky = W +E)
        
        #getting data at the beginninng
        self.get_products()
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit
        return result
    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)        
        #getting data
        for row in db_rows:
            #filling data            
            self.tree.insert('',0, text = row[1], values = row[2] )        
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0      
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query,parameters)
            self.message['text'] = 'Product {} added succesfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)

        else:
             self.message['text'] = 'Name and price are required. ERROR'
            
        self.get_products()
    def delete_product(self):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.message['text'] = 'Please, select a record'
            return
        self.message['text'] = ""
        name  = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Record {} has been deleted successfully'.format(name)
        self.get_products()
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()