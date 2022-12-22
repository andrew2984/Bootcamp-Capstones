import sqlite3

def add_book():
        # checks if id is already taken
        while True:
            try:
                new_id = int(input("Enter id"))
                if new_id in get_id_list():
                    print("This id is already taken")
                else:
                    break
            except ValueError:
                print("Please enter a number")

        # user enters data and data is inserted
        new_title = input("Enter the title")
        new_author = input("Enter the author")
        new_qty = int(input("Enter how many we have in stock"))
        # makes list and inserts into table
        new_book_data = [new_id, new_title, new_author, new_qty]
        cursor.execute('''
            INSERT INTO bookstore(id, Title, Author, Qty) VALUES(?,?,?,?)''', new_book_data)


def update_info():
    # checks if id is valid
    while True:
        try:
            update_id = int(input("Enter the id of the book you would like to update"))
            if update_id in get_id_list():
                break
            else:
                print("No book has this id")
        except ValueError:
            print("Please enter a number")

    # checks if id is already taken
    while True:
        try:
            new_id = int(input("Enter new id"))
            if new_id in get_id_list() and new_id != update_id:  # allows same id to be entered again
                print("This id is already taken")
            else:
                break
        except ValueError:
            print("Please enter a number")

    # user enters data and data is set
    # data stays the same if user enters /stay/
    new_title = input("Enter the new title or '/stay/' if you want it to stay")
    if new_title == "/stay/":
        for elements in all_data:
            if elements[0] == update_id:  # [0] is id
                new_title = elements[1]  # [1] is title
    new_author = input("Enter the author or '/stay/' if you want it to stay")
    if new_author == "/stay/":
        for elements in all_data:
            if elements[0] == update_id:  # [0] is id
                new_author = elements[1]  # [2] is author
    new_qty = int(input("Enter how many we have in stock"))
    update = (new_id, new_title, new_author, new_qty, update_id)
    update_data(update)
    

# updates row according to given list
def update_data(update):
    cursor.execute('''
        UPDATE bookstore SET id = ?, Title = ?, Author = ?, Qty = ? WHERE id = ?''', update)


def delete_book():
    # checks if id is valid
    while True:
        try:
            delete_id = int(input("Enter the id of the book you would like to delete"))
            if delete_id in get_id_list():
                break
            else:
                print("No book has this id")
        except ValueError:
            print("Please enter a number")
    # delete id's row
    cursor.execute('''
        DELETE FROM bookstore WHERE id = ?''', (delete_id,))


def search_book_id():
    # checks if id is valid
    while True:
        try:
            search_id = int(input("Enter the id of the book you would like to search"))
            if search_id in get_id_list():
                break
            else:
                print("No book has this id")
        except ValueError:
            print("Please enter a number")

    # returns book with given id
    cursor.execute('''
    SELECT * FROM bookstore WHERE id = ?''', (search_id,))
    search = cursor.fetchall()
    print(search)
    return_menu = input("Enter anything to return to menu")


def search_book_author():
    # checks if author is valid
    while True:            
        search_author = input("Enter the author you would like to search for")
        if search_author in get_author_list():
            break
        else:
            print("We don't have books from this author")

    # returns books by given author
    cursor.execute('''
    SELECT * FROM bookstore WHERE Author = ?''', (search_author,))
    search = cursor.fetchall()
    # prints books line by line
    for elements in search:
        print(elements)
    return_menu = input("Enter anything to return to menu")


def create_table():
    # create table
    cursor.execute('''
        CREATE TABLE bookstore(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')


def insert_data(data):
    # insert data into table
    cursor.executemany('''
        INSERT INTO bookstore(id, Title, Author, Qty) VALUES(?,?,?,?)''', data)


# delete entire table
def drop_table():
    try:
        cursor.execute('''
        DROP TABLE bookstore''')
    except sqlite3.OperationalError:
        pass


# restore database to default
def restore(data):
    drop_table()
    create_table()
    insert_data(data)


# gathers list of ids from all_data
def get_id_list():
    id_list = []
    for books in all_data:
        id_list.append(books[0])  # [2] is index of id
    return id_list


# gathers list of authors from all_data
def get_author_list():
    author_list = []
    for books in all_data:
        author_list.append(books[2])  # [0] is index of author
    return author_list


# gathers data from database and prints
def gather_data():
    cursor.execute('''
        SELECT * FROM bookstore''')
    return cursor.fetchall()


def print_data(data):
    for books in data:
        print(books)


try:
    db = sqlite3.connect('bookstore.db')
    cursor = db.cursor()
    # initial table
    book_data = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40), (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25), (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37), (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

    while True:
        # gather and print all books
        all_data = gather_data()
        print_data(all_data)
        # menu selection
        try:
            menu = int(input("Please enter one of the following.\n1. Enter book\n2. Update book\n3. Delete book\n4. Search books\n5. Restore to default\n0. Exit"))
        except ValueError:
            print("Please enter a number")
            continue
        
        if menu == 1:
            add_book()
        elif menu == 2:
            update_info()
        elif menu == 3:
            delete_book()
        elif menu == 4:
            select_search = input("Would you like to search by id or by author?").lower()
            # select search by id or author
            if select_search == "id":
                search_book_id()
            elif select_search == "author":
                search_book_author()
            else:
                print("Invalid input")
        elif menu == 5:
            # restores to default layout
            restore(book_data)
        elif menu == 0:
            break
        else:
            print("Please enter a valid number")
except Exception:
    db.rollback()
finally:
    db.commit()
    db.close()