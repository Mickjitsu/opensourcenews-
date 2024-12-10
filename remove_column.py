import psycopg2
from django.conf import settings

# Database connection settings (use your settings.py from Django)
db_settings = settings.DATABASES['default']

try:
    # Establish the connection to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT']
    )
    
    cursor = connection.cursor()

    # SQL query to remove the 'is_headline' column if it exists
    cursor.execute("ALTER TABLE articles_article DROP COLUMN IF EXISTS is_headline;")
    
    # Commit the changes to the database
    connection.commit()

    print("Column 'is_headline' removed successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()