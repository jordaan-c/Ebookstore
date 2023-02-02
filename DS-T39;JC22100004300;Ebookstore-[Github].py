# Title: Ebookstore
# Date: 2023-01-10
# Author: Jordaan Clarke

# Description:
# Bookstore program that allows the user to add, update, delete, or search for specific books.


# Define a function that houses all of the logic for the ebookstore program.
def ebookstore():
    

        
    # Import the required libraries.
    import sqlite3 as s3
    
    # Create a new database called "ebookstore".
    db = s3.connect("ebookstore")
    
    # Assign the cursor to a variable.
    c = db.cursor()
        

    # Try block that generates the basic book database.
    try:
                
        # Create a new table called 'books'.
        c.execute("""CREATE TABLE IF NOT EXISTS books(
            id CHAR(4) PRIMARY KEY,
            title VARCHAR(40),
            author VARCHAR(25),
            qty INT(3));""")
        
        # Insert values from the task description into the table.
        c.execute("""INSERT INTO books(id, title, author, qty)
                  VALUES(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                  (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                  (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                  (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                  (3005, "Alice in Wonderland", "Lewis Carroll", 12);""")
        
    
    except s3.IntegrityError: print("Database 'ebookstore' exists.")
    finally: db.commit(); db.close()
    

# Functions.
# Block defining various functions used in the program.
    
    
    # Define a function that calls other functions defined later in the program.
    def home(): menu()    
    
    
    # Define a function that accesses the database and executes queries.
    def access_db(q1, operation = "", lst = []):
        '''
        
        Parameters
        ----------
        q1: String
            Query to be executed.
        
        operation: String
            Type of operation to be executed. Values can be: ["read", "write", "id"]
            
        lst: List
            List of values to replace placeholders in the query.


        '''
        
        # Define some messages that can be reused.
        connected = "\nDatabase connection established...\n"
        changed = "Changes made successfully.\n"
        added = "Book successfully added.\n"
        deleted = "Book successfully deleted.\n"
        saving = "Saving changes...\n"
        closing = "Database connection terminated.\n"
        
    
    ### OPEN DATABASE ###    
    
        # Connect to the database.
        db = s3.connect("ebookstore")
        print(connected)
        
        # Assign the cursor to a variable.
        c = db.cursor()
        
        # Exectute the query.
        c.execute(q1)

        
    ### DISPLAY BLOCK ###
        
        # Define a function that returns all values from the query.
        def get_record(result):

            
            # Iterate through the query results and display in a user-friendly format.
            for x in result:
                
                print(f"""
ID: {x[0]}
Title: {x[1]}
Author: {x[2]}
Quantity: {x[3]}""")

            print()
        
        
        # Conditional block that displays a list of books in the database.
        if operation == "fetch":
            
            get_record(c.fetchall())
        
        
    ### ID BLOCK ###
        
        # Conditional block that retrieves and returns the max id for the primary key.
        elif operation == "id":

            # Capture the max id.
            max_id = c.fetchone()
            
            # Return the value.
            db.commit()
            db.close()
            return max_id
                
        
        elif operation == "check_id":
            
            c.execute("""SELECT EXISTS (SELECT id FROM books
                  WHERE id = ?);""", (lst,))
            
            # Capture the result of the ID check.
            id_check = c.fetchone()     
            
            # Return the value.
            db.commit()
            db.close()
            return id_check     


    ### ADD BLOCK ###
        
        # Conditional block that adds a new book.
        elif operation == "add":
            
            c.execute("""INSERT INTO books(id, title, author, qty) 
                      VALUES(?,?,?,?);""", (lst[0], lst[1], lst[2], lst[3]))
        
            print(added, saving)
        
        
    ### UPDATE BLOCK ###
    
        # Conditional block that updates the book title.
        elif operation == "update_t":

            # Update the book title with the values passed.
            c.execute("""UPDATE books SET title = ?
                      WHERE id = ?;""", (lst[0], lst[1]))

            print(changed, saving)

        # Conditional block that updates the book author.
        elif operation == "update_a":

            # Update the book author with the values passed.
            c.execute("""UPDATE books SET author = ?
                      WHERE id = ?;""", (lst[0], lst[1]))

            print(changed, saving)

        # Conditional block that updates the book quantity.
        elif operation == "update_q":

            # Update the book quantity with the values passed.
            c.execute("""UPDATE books SET qty = ?
                      WHERE id = ?;""", (lst[0], lst[1]))
        
            print(changed, saving)    
        
        
    ### DELETE BLOCK ###
    
        # Conditional block that deletes a book.
        elif operation == "del":
            
            # Try block that attempts to delete the book.
            try:
            
                # Delete the book matching the ID input by the user.
                c.execute("""DELETE FROM books 
                          WHERE id = ?;""", (lst,))
                
                print(deleted, saving)
                            
            # Capture input for IDs that don't exist and handle the error.
            except s3.InterfaceError: print("Error: ID not recognised. Returning to the menu...\n")
            
        
    ### SEARCH BLOCK ###
    
        # Conditional block that searches by book title.
        elif operation == "search_t":

            # Search for book title using the value passed.
            get_record(c.execute("""SELECT * FROM books 
                      WHERE title LIKE '%' || ? || '%';""", (lst,)))   


        # Conditional block that searches by book author.
        elif operation == "search_a":

            # Search for book author using the value passed.
            get_record(c.execute("""SELECT * FROM books 
                      WHERE author LIKE '%' || ? || '%';""", (lst,)))

    
    ### CLOSE DATABASE ###                
            
        # Save changes and close the database. 
        db.commit()
        db.close()
        print(closing)
        
        
    # Define a function that can add books to the database.
    def add_new():
        
        
        # Retrieve the max ID for the primary key and cast to int(). 
        get_id = access_db("""SELECT MAX(id) FROM books;""", "id")
        n_id = get_id[0]
        n_id = int(n_id)
        
        # Make the ID unique.
        n_id += 1
        
        # Capture input for information about the book.
        n_title = input("Enter the book title: ")
        n_author = input("Enter the name of the author: ")
        n_qty = int(input("Enter the quantity of stock on hand: "))        
        
        # Capture the new values in a list and call the database.
        row_val = [n_id, n_title, n_author, n_qty]
        access_db("", "add", row_val) 
    
    
    # Define a function that updates books in the database.
    def update_book():
        
                
        # Display all books to the user.
        access_db("""SELECT * FROM books;""", "fetch")
        
        # Read ID for the book to be updated.
        u_id = int(input("Enter the ID of the book to be updated: "))
        
        # Validate the book ID and cast the result to int().
        id_check = access_db("", "check_id", (u_id))        
        id_check = id_check[0]
        
        # Conditional block for invalid IDs.
        if id_check == 0: print("ERROR: This ID does not exist. Returning to the menu."); home()
        
        # Conditional block for valid IDs.
        elif id_check == 1:
        
            # Display menu options to the user.
            print("""
---------------------------------              
|        Update Book Menu       |
---------------------------------
    
    Option 1: Update Title
    Option 2: Update Author
    Option 3: Update Quantity
    Option 4: Cancel
                
                """)
        
            # Read input for the update menu.
            u_option = int(input("Select an option from the menu: "))
            
            # Assign the values 1-4 to a list. This will be used to validate input.
            u_valid = [1, 2, 3, 4]
            
            # Conditional block to capture invalid integer input.
            while u_option not in u_valid:
                print("ERROR: Menu option not recognised. Please try again.")
                u_option = int(input("Enter a number from 1 to 4: "))
                print()
        
            # Conditional block for valid input.
            else:
                
                # Conditional block for updating the title.           
                if u_option ==   u_valid[0]: 
                    
                    # Read input for the new book title.
                    u_title = input("Enter the updated book title: ")
                
                    # Capture the update values in a list and call the database.
                    row_value = [u_title, u_id]
                    access_db("", "update_t", row_value)
                
                
                # Conditional block for updating the author.
                elif u_option == u_valid[1]:
                    
                    # Read input for the new book author.
                    u_author = input("Enter the updated author: ")
                
                    # Capture the update values in a list and call the database.
                    row_value = [u_author, u_id]
                    access_db("", "update_a", row_value)
                
                
                # Conditional block for updating the qunatity.
                elif u_option == u_valid[2]:
                    
                    # Read input for the new book quantity.
                    u_qty = int(input("Enter the updated quantity: "))  
                              
                    # Capture the update values in a list and call the database.
                    row_value = [u_qty, u_id]
                    access_db("", "update_q", row_value)
                    
    
                # Conditional block to cancel and return to the menu.                
                elif u_option == u_valid[3]: menu() 
    

    # Define a function that removes books from the database.
    def delete_book():
        
    
        # Display all books to the user
        access_db("""SELECT * FROM books;""", "fetch")
        
        # Read input for the book to be updated.
        d_id = int(input("Enter the ID of the book to be deleted: "))
        
        # Validate the book ID and cast the result to int().
        id_check = access_db("", "check_id", (d_id))        
        id_check = id_check[0]
        
        # Conditional block for invalid IDs.
        if id_check == 0: print("ERROR: This ID does not exist. Returning to the menu."); home()
        
        # Conditional block for valid IDs.
        elif id_check == 1:
        
            # Call the database.
            access_db("", "del", (d_id))
        
    
    # Define a function that looks for specific books in the database.
    def search():
        

        # Define a function that returns a search term.
        def search_term():
            # Read input for the search term.
            st = input("Enter search term: ")
            return st
        
        # Display menu options to the user.
        print("""
---------------------------------              
|          Search Menu          |
---------------------------------
    
    Option 1: Search by Title
    Option 2: Search by Author
    Option 3: Cancel
        
        """)

        # Read input for the menu option.
        s_option = int(input("Select an option from the menu: "))
                     
        # Assign the values 1-3 to a list. This will be used to validate input.
        s_valid = [1, 2, 3]
        
        # Conditional block to capture invalid integer input.
        while s_option not in s_valid:
            print("ERROR: Menu option not recognised. Please try again.")
            s_option = int(input("Enter a number from 1 to 3: "))
            print()   

        # Conditional block for valid input.
        else:                      
        
            # Conditional block for title search.
            if s_option   == s_valid[0]: access_db("", "search_t", (search_term()))                
                
            # Conditional block for author search.
            elif s_option == s_valid[1]: access_db("", "search_a", (search_term()))

            # Conditional block to cancel and return to the menu.                
            elif s_option   == s_valid[2]: menu()

    
    # Define a function that triggers the exit routine and ends the program.
    def exit_program():
        
        
        # Print a message about ending the program.
        # Raise a SystemExit exception with a '0' argument to indicate a successful termination.
        print("Logging you out.")     
        raise SystemExit(0) 
    
    
    # Define a function that provides access to the other functions.
    def menu():
        
        
        # Display menu options the user.
        print("""              
---------------------------------              
|     E-Bookstore Main Menu     |
---------------------------------
    
    Option 1: Add New Book
    Option 2: Update Book
    Option 3: Delete Book
    Option 4: Search
    Option 5: Exit
    
        """)
            
            
        # Assign the values 1-5 to a list. This will be used to validate input.
        m_valid = [1, 2, 3, 4, 5]


        try:
            
            # Read integer input for a variable called option. 
            # This will be used for comparision in a while loop and subsequent conditional blocks.
            m_option = int(input("Enter a number from 1 to 5: "))
            
            print()
            
            # Conditional block to capture invalid integer input.
            while m_option not in m_valid:
                print("ERROR: Menu option not recognised. Please try again.")
                m_option = int(input("Enter a number from 1 to 5: "))
                print()
        
            # Conditional block for valid input.
            else:        
                        
                # Conditional block for the menu.           
                if   m_option == m_valid[0]: add_new(); menu()
                elif m_option == m_valid[1]: update_book(); menu()
                elif m_option == m_valid[2]: delete_book(); menu()
                elif m_option == m_valid[3]: search(); menu()
                
                # Conditional block to exit the program.
                elif m_option == m_valid[4]: exit_program()
                
        
        # Capture invalid menu input and return to the menu.
        except ValueError: 
            print()
            print("ERROR: Menu option not recognised. Please try again.")
            menu()
    
        
    # Function call to open the menu.
    menu()  
            

# Function call that starts the program.
ebookstore()