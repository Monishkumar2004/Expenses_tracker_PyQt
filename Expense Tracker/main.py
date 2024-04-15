# Import Modules
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QMessageBox, QHeaderView

import psycopg2

 # Database Processes


# App classes
class ExpenseApp(QWidget):
    

     # Database Processes

    def load_items(self):

        conn = psycopg2.connect(dbname='expenses', password='120204', port=5432, user='postgres')
        curr = conn.cursor()

        query = "SELECT * FROM EXPENSE_DETAILS"
        curr.execute(query)
        rows = curr.fetchall()

        self.items.setRowCount(0)  # Clear existing rows in the table

        for row_number, row_data in enumerate(rows):
            # sets how many rows to be shown in the table widget
            self.items.insertRow(row_number)
            
            # this for loop populates the rows created
            for column_number , data in enumerate(row_data):
                self.items.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
            
            
    # function to add expenses to the database
    def add_details(self):
        # self.create_database()    
        date = self.date_edit.date().toString("dd-MM-yyyy")
        category = self.category_box.currentText()
        amount = self.amount_box.text()
        description = self.description_box.text()

        conn = psycopg2.connect(dbname = 'expenses', password = 120204, port = 5432, user = 'postgres')

        curr = conn.cursor()

        query = '''
                INSERT INTO EXPENSE_DETAILS (DATE, CATEGORY, AMOUNT, DESCRIPTION) VALUES(%s , %s, %s, %s)
                
        '''
        curr.execute(query, (date, category, amount, description))
        
        conn.commit()
        conn.close()

        self.amount_box.clear()
        self.description_box.clear()
        self.load_items()
        

    # function to delete exxpense entry from the table
    def delete_entry(self):
        selected_row = self.items.currentRow()
        if selected_row == -1:
            message = QMessageBox()
            message.setText("No rows selected.")
            message.exec()
        
        confirm = QMessageBox.question(self, "Are you sure?", "Delete Expense?", QMessageBox.Yes | QMessageBox.No)
            # print(selected_row)
        selected_id = self.items.item(selected_row, 0).text()
            # print(selected_id)
            
        if confirm == QMessageBox.No:
            return
            
        conn = psycopg2.connect(user = 'postgres', port = 5432, dbname = 'expenses', password= 120204)
        curr = conn.cursor()
        query = '''
                    DELETE FROM EXPENSE_DETAILS WHERE id = %s
                    '''
        curr.execute(query, (selected_id,))
        conn.commit()
        conn.close()
            
        self.load_items()
                
    
    
    def __init__(self):
        super().__init__()  #This is needed because we are accessing the properties of superclass which is QWidget
        # main app objects and settings
        self.resize(700,600)
        self.setWindowTitle("Expense Tracker App")
        
        
        # create objects -- here we are creating the common widgets like push-button, label, dropdown menu etc.
        self.date_label = QLabel("Date: ")
        self.date_edit = QDateEdit()
        self.category_label = QLabel("Category: ")
        self.category_box = QComboBox()
        self.amount_label = QLabel("Amount: ")
        self.amount_box = QLineEdit()
        self.description_label = QLabel("Description: ")
        self.description_box = QLineEdit()
        self.add = QPushButton("Add Expense", )
        self.delete = QPushButton("delete Expense")

        # QTableWidget is used to show a table in the Gui ...... It uses ".setColumn("Any number")" to show no. of columns ........ and .setHorizontalHeaderLables to show the name of columns in the Table.
        self.items = QTableWidget()
        self.items.setColumnCount(5)
        self.items.setHorizontalHeaderLabels(["ID", "Date", "Category" ,"Amount", "Description"])
        self.items.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.items.sortByColumn(1,Qt.DescendingOrder)


        # below i have used .addItems to add names in the dropdown menu of the category.
        self.category_box.addItems(["Food", "Rent", "Transportaion", "Shooping", "Entertainment", "Bills", "Others"])

        # below we have used Qdate.currentDate() 
        self.date_edit.setDate(QDate.currentDate())
        
        

        # Connecting buttons with the 
        self.add.clicked.connect(self.add_details)
        self.delete.clicked.connect(self.delete_entry)
        
        self.load_items()
    


        # design App with layouts
        # master layout works like a column in which QHBox layout works as rows to display the items we have inserted in the Rows
        master_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(self.date_label)
        row1.addWidget(self.date_edit)
        row1.addWidget(self.category_label)
        row1.addWidget(self.category_box)
        row2.addWidget(self.amount_label)
        row2.addWidget(self.amount_box)
        row2.addWidget(self.description_label)
        row2.addWidget(self.description_box)
        row3.addWidget(self.add)
        row3.addWidget(self.delete)

        
        master_layout.addLayout(row1)
        master_layout.addLayout(row2)
        master_layout.addLayout(row3)
        master_layout.addWidget(self.items)

        self.setLayout(master_layout)

    
    
        
        


# Run the apps

if __name__ == '__main__':
    app = QApplication([])
    main_window = ExpenseApp()
    main_window.show()
    app.exec_()