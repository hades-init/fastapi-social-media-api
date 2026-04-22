import psycopg
from psycopg.rows import dict_row

# DATABASE CONNECTION STRING/URI
# [dialect]://[user]:[password]@[host]:[port]/[dbname]

# Database connection string
POSTGRES_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/sampledb"

# Connect to an existing database
with psycopg.connect(conninfo=POSTGRES_DATABASE_URL) as conn:

    # Open a `Cursor` instance to perform database operations
    # You can pass `row_factory=dict_row` argument to represent rows as dictionaries (with the column names as keys)
    with conn.cursor() as cursor:

        # Execute a database query using `cursor.execute()`
        # For example, this creates a table
        cursor.execute("""
                       CREATE TABLE heroes (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        hero_name VARCHAR(100),
                        class CHAR(1) CHECK (class IN ('S', 'A', 'B', 'C')) NOT NULL,
                        rank INTEGER NOT NULL,
                        ability TEXT,
                        is_active BOOLEAN DEFAULT true
                       );
                       """)
        
        # And this inserts data into the table
        cursor.execute("""
                       INSERT INTO heroes (name, hero_name, class, rank, ability) 
                       VALUES
                        ('Saitama', 'Caped Baldy', 'B', 7, 'Overwhelming strength, defeats enemies in one punch'),
                        ('Genos', 'Demon Cyborg', 'S', 14, 'Advanced cybernetic enhancements and firepower'),
                        ('Bang', 'Silver Fang', 'S', 3, 'Master of Water Stream Rock Smashing Fist'),
                       ('Tatsumaki', 'Tornado of Terror', 'S', 2, 'Powerful esper with psychic powers');
                       """)
        

        # Query the database and obtain data as Python objects
        cursor.execute("SELECT * FROM heroes")
        # Iterate over the cursor object
        for row in cursor:
            print(row)
        
        # use `fetchall()` to return list of records
        cursor.execute("SELECT * FROM heroes WHERE class = %s AND rank <= ", ('S', 10))
        heroes = cursor.fetchall()  # Returns rows as a list of tuples
        print(heroes)