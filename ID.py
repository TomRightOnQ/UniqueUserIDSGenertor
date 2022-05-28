import mysql.connector

def generateID(cursor):
    # Open record to check the current range of IDS
    frc = open('RECORD.txt', 'r');
    r = frc.read()
    i = int(r)
    frc.close()

# Clear the record
    frc = open('RECORD.txt', 'w')
    frc.truncate(0)

# Insertion1
    limit = i + 10
    while i < limit:
        generate_id = ("INSERT INTO IDS (id, used) VALUES (%s, %s)")
        id_info = (str(i), "0")
        cursor.execute(generate_id, id_info)
        i += 1

# Rewrite the record file
    frc.write(str(limit))
    frc.close()
