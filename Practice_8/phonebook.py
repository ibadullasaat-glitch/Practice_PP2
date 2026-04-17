import psycopg2
import csv
from config import host, port, user, password, database

def get_connection():
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    conn.autocommit = True
    return conn

def setup_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
    CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
    RETURNS TABLE (id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR, created_at TIMESTAMP)
    AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM contacts
        WHERE first_name ILIKE '%' || pattern || '%'
           OR last_name ILIKE '%' || pattern || '%'
           OR phone ILIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_or_update_user(p_first_name VARCHAR, p_last_name VARCHAR, p_phone VARCHAR)
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM contacts WHERE phone = p_phone) THEN
            UPDATE contacts SET first_name = p_first_name, last_name = p_last_name WHERE phone = p_phone;
        ELSE
            INSERT INTO contacts(first_name, last_name, phone) VALUES (p_first_name, p_last_name, p_phone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
    CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
    RETURNS TABLE (id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR, created_at TIMESTAMP)
    AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM contacts ORDER BY id LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
    AS $$
    BEGIN
        DELETE FROM contacts
        WHERE first_name ILIKE '%' || p_value || '%'
           OR last_name ILIKE '%' || p_value || '%'
           OR phone = p_value;
    END;
    $$ LANGUAGE plpgsql;
    """)

    cur.close()
    conn.close()

def add_or_update():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s,%s,%s)", (first_name, last_name, phone))
    cur.close()
    conn.close()

def search():
    pattern = input("Search: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s,%s)", (limit, offset))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def delete():
    value = input("Name or phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s)", (value,))
    cur.close()
    conn.close()

def menu():
    setup_db()
    while True:
        print("1 Add/Update")
        print("2 Search")
        print("3 Pagination")
        print("4 Delete")
        print("5 Exit")
        c = input()
        if c == "1":
            add_or_update()
        elif c == "2":
            search()
        elif c == "3":
            paginate()
        elif c == "4":
            delete()
        elif c == "5":
            break

if __name__ == "__main__":
    menu()
