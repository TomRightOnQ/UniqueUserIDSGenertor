import mysql.connector
import ID # for id generation

# Set up mysql config
config = {
'user': 'root',
'password': '123456',
'host': 'localhost',
'database': 'user_id_ge',
'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered = True)
ID.generateID(cursor)
cnx.commit()
cursor.close()
cnx.close()
         