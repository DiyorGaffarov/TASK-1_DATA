import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_books_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id NUMERIC PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                genre VARCHAR(100),
                publisher VARCHAR(255),
                year INT,
                price NUMERIC(10, 2)
            );
        """)
    conn.commit()
    print("Books table is ready")


def parse_price(price_str):
    price_str = str(price_str).strip()
    if "€" in price_str:
        return round(float(price_str.replace("€", "").strip()) * 1.2, 2)
    return float(price_str.replace("$", "").strip())


def insert_books(conn, books):
    inserted = 0
    skipped = 0

    for book in books:
        try:
            price = parse_price(book.get("price", "0"))

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO books (id, title, author, genre, publisher, year, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    book.get("id"),
                    book.get("title"),
                    book.get("author"),
                    book.get("genre"),
                    book.get("publisher"),
                    book.get("year"),
                    price
                ))

            conn.commit()
            inserted += 1

        except Exception as e:
            conn.rollback()
            print(f"Could not insert book '{book.get('title')}': {e}")
            skipped += 1

    print(f"Inserted {inserted} books, skipped {skipped}")
    
    json_count = len(books)
    print("JSON count:", json_count)


