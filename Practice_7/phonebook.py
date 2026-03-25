import psycopg2
import csv
import sys
from config import host, port, user, password, database

def get_connection():
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    conn.autocommit = True
    return conn

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id          SERIAL PRIMARY KEY,
            first_name  VARCHAR(100) NOT NULL,
            last_name   VARCHAR(100),
            phone       VARCHAR(20) UNIQUE NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.close()
    conn.close()

def import_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 3:
                    continue
                first_name = row[0].strip()
                last_name = row[1].strip() if len(row) > 1 else None
                phone = row[2].strip()
                
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, phone)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING;
                """, (first_name, last_name, phone))
        print("Data from CSV file imported successfully.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print("Error importing CSV:", e)
    finally:
        cur.close()
        conn.close()

def add_contact():
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name (can be empty): ").strip()
    phone = input("Enter phone number: ").strip()
    
    if not first_name or not phone:
        print("First name and phone are required.")
        return
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO contacts (first_name, last_name, phone)
            VALUES (%s, %s, %s)
            ON CONFLICT (phone) DO NOTHING;
        """, (first_name, last_name or None, phone))
        
        if cur.rowcount > 0:
            print("Contact added successfully.")
        else:
            print("Phone number already exists.")
    except Exception as e:
        print("Error adding contact:", e)
    finally:
        cur.close()
        conn.close()

def update_contact():
    phone = input("Enter phone number to update: ").strip()
    
    print("What do you want to update?")
    print("1. First name")
    print("2. Last name")
    print("3. Phone number")
    choice = input("Choose (1-3): ")
    
    conn = get_connection()
    cur = conn.cursor()
    
    if choice == "1":
        new_value = input("New first name: ").strip()
        cur.execute("UPDATE contacts SET first_name = %s WHERE phone = %s", (new_value, phone))
    elif choice == "2":
        new_value = input("New last name: ").strip()
        cur.execute("UPDATE contacts SET last_name = %s WHERE phone = %s", (new_value, phone))
    elif choice == "3":
        new_value = input("New phone number: ").strip()
        cur.execute("UPDATE contacts SET phone = %s WHERE phone = %s", (new_value, phone))
    else:
        print("Invalid choice.")
        return
    
    if cur.rowcount > 0:
        print("Contact updated successfully.")
    else:
        print("Contact not found.")
    
    cur.close()
    conn.close()

def search_contacts():
    print("Search by:")
    print("1. Name")
    print("2. Phone prefix")
    choice = input("Choose (1-2): ")
    
    conn = get_connection()
    cur = conn.cursor()
    
    if choice == "1":
        name = input("Enter name (or part of name): ").strip()
        cur.execute("""
            SELECT id, first_name, last_name, phone, created_at 
            FROM contacts 
            WHERE first_name ILIKE %s OR last_name ILIKE %s
            ORDER BY first_name;
        """, (f"%{name}%", f"%{name}%"))
    elif choice == "2":
        prefix = input("Enter phone prefix: ").strip()
        cur.execute("""
            SELECT id, first_name, last_name, phone, created_at 
            FROM contacts 
            WHERE phone LIKE %s
            ORDER BY phone;
        """, (prefix + "%",))
    else:
        print("Invalid choice.")
        return
    
    rows = cur.fetchall()
    if not rows:
        print("No contacts found.")
    else:
        print(f"\nFound {len(rows)} contact(s):")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} {row[2] or ''} | Phone: {row[3]} | Added: {row[4].strftime('%Y-%m-%d %H:%M')}")
    
    cur.close()
    conn.close()

def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, phone, created_at FROM contacts ORDER BY first_name;")
    rows = cur.fetchall()
    
    if not rows:
        print("No contacts in the phonebook.")
    else:
        print(f"\nAll contacts ({len(rows)}):")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} {row[2] or ''} | Phone: {row[3]} | Added: {row[4].strftime('%Y-%m-%d %H:%M')}")
    
    cur.close()
    conn.close()

def delete_contact():
    print("Delete by:")
    print("1. Phone number")
    print("2. Name")
    choice = input("Choose (1-2): ")
    
    conn = get_connection()
    cur = conn.cursor()
    
    if choice == "1":
        phone = input("Enter phone number to delete: ").strip()
        cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    elif choice == "2":
        name = input("Enter name (or part of name): ").strip()
        cur.execute("DELETE FROM contacts WHERE first_name ILIKE %s OR last_name ILIKE %s", (f"%{name}%", f"%{name}%"))
    else:
        print("Invalid choice.")
        return
    
    if cur.rowcount > 0:
        print(f"Successfully deleted {cur.rowcount} contact(s).")
    else:
        print("No contacts found to delete.")
    
    cur.close()
    conn.close()

def menu():
    create_table()
    
    while True:
        print("\n" + "="*40)
        print("          PHONEBOOK")
        print("="*40)
        print("1. Add new contact")
        print("2. Import from CSV")
        print("3. Search contacts")
        print("4. Update contact")
        print("5. Show all contacts")
        print("6. Delete contact")
        print("7. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            filename = input("Enter CSV filename (default: contacts.csv): ") or "contacts.csv"
            import_from_csv(filename)
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            show_all_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()