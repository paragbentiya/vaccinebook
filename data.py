import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(user='root',
                              password='1234',
                              host='1234',
                              database='vaccinebook')

# Create a cursor
cursor = cnx.cursor()

# Define the CREATE TABLE statement
create_table_stmt = """
CREATE TABLE IF NOT EXISTS accounts (
    id int(11) NOT NULL AUTO_INCREMENT,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
"""

# Execute the CREATE TABLE statement
cursor.execute(create_table_stmt)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
