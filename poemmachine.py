# PoemMachine by Chloé Matthews
# Generates random three-line poems from a database of content
# Allows users to write new content to database
# Currently runs in shell, connects to SQLite3 database

import random, sqlite3

def connect(db_file):
    """ creates connection to SQLite database: notebook.db """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def clean_input(a, b, c):
    """ takes user input and makes it passable for db """
    if a.isalpha() and b.isalpha() and c.isalpha():
        if len(a)==1 and len(b)==1 and len(c)==1:
            a.lower()
            b.lower()
            c.lower()

            return a, b, c
        else:
            print('please enter only one letter at a time')
    else:
        print('please enter only letters')

def display_all(conn):
    """ query and return all valus in table: lines """
    cursor = conn.cursor()
    cursor.execute("select * from lines order by firstLetter")

    data = cursor.fetchall()
    all_content = []
    for item in data:
        all_content.append(item)

    return all_content

def select_by_first(conn, fl):
    """ query table, filter by column: firstLetter """
    """ return random entry """
    try:
        cursor = conn.cursor()
        cursor.execute("select content from lines where firstLetter=?", 
                (fl))

        data = cursor.fetchall()
        count = 0
        for item in data:
            count += 1
        try:
            random_line = data[random.randrange(count)]
            return random_line
        except ValueError as e:
            return 'an error occurred: ', e.args[0]
    except sqlite3.Error as e:
        return 'an error occurred: ', e.args[0]


def get_poem (conn, a, b, c):
    """ takes cleaned user input and returns lines """
    collection = []
    collection.append(select_by_first(conn, a))
    collection.append(select_by_first(conn, b))
    collection.append(select_by_first(conn, c))

    return collection

def add_line (conn, content, author):
    """ adds user-written line to database """
    print('content: ' + content)

    if content[0].isalpha() is True:
        fl = content[0].lower()
    else:
        return 'unsuccessful: line must begin with a letter'
    
    try:
        cursor = conn.cursor()
        cursor.execute("insert into lines values(?, ?, ?)", 
                (content, fl, author))
        conn.commit()
        return cursor.lastrowid, 'line successfully added to notebook'
    except sqlite3.Error as e:
        return 'an error occurred: ', e.args[0]

def menu():
    """ allow users to choose an action """
    q = 'what would you like to do? (1) generate a poem (2) write a line'
    print(q)
    choice = input('type 1 or 2: ')
    
    try:
        if int(choice)==1 or int(choice)==2:
            return int(choice)
        else:
            print('make a selection by entering numbers 1 or 2')
    except ValueError as e:
        return 'an error occurred ', e.args[0]

def run():
    """ runs program """
    option = menu()
    db = "notebook.db"

    if option==1:
        l1 = input('enter first letter: ')
        l2 = input('enter second letter: ')
        l3 = input('enter third letter: ')

        cleaned = clean_input(l1, l2, l3)
    
        conn = connect(db)
        with conn:
            try:
                print("poem using letters: {0}, {1}, {2}".format(
                    cleaned[0], cleaned[1], cleaned[2]))
                poem = get_poem(conn, cleaned[0], cleaned[1], cleaned[2])
                if poem:
                    for item in poem:
                        print(item)
            except TypeError as e:
                return 'an error occurred: ', e.args[0]
    elif option==2:
        content = input('write line here, press ENTER when done: ')
        author = input('write your pen name, press ENTER when done: ')
       
        print(content, author)
        conn = connect(db)
        with conn:
            try:
                print('adding your lines to the notebook...')
                published = add_line(conn, content, author)
               
                if published is not None:
                    print(published)
            except TypeError as e:
                return 'an error occurred: ', e.args[0]
    else:
        if option:
            print(option)

if __name__== '__main__':
    run()
