import flask
from time import sleep
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

# Set up the page
app = flask.Flask(__name__)
limiter = Limiter(
app,
key_func=get_remote_address,
default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
@limiter.limit("1/second")
def index():
    return flask.render_template('Index.html')

# Page for new ID
@app.route('/NewID')
@limiter.limit("1/second")
def NewID():
    try:
        # Unlock database
        cursor.execute('UNLOCK TABLES')

        # Select first unused
        cursor.execute('SELECT id FROM IDS WHERE IDS.used = 0')
        # Make sure the IDS are sufficient
        idR = cursor.fetchone()
        while idR is None:
            pass
        idR = str(idR[0])
        # Set current id as used
        cursor.execute('UPDATE IDS SET used = 1 WHERE id = %s', (idR,))
        cnx.commit()
        # Enlarge id pool
        cursor.execute('SELECT COUNT(id) FROM IDS WHERE used = 0')
        idC = cursor.fetchone()
        while idC is None:
            pass
        idC = int(idC[0])
        # Check remaining ids
        if idC <= 10:
            # generate another 10 ids
            ID.generateID(cursor)
        
        ret = '<h1>Congratulations! Your ID Number is: ' + idR + ' ' + str(idC) + '</h1>'
        # Lock database
        cursor.execute('LOCK TABLE IDS READ')
        cursor.execute('LOCK TABLE IDS WRITE')
        return ret
    except Exception as e:
        cursor.execute('LOCK TABLE IDS READ')
        cursor.execute('LOCK TABLE IDS WRITE')
        ret = 'An error has occur: '
        ret += str(e)
        return ret
        
# Run the Webserver
if __name__ == '__main__':
    # Lock table
    cursor.execute('LOCK TABLE IDS READ')
    cursor.execute('LOCK TABLE IDS WRITE')
    # Running
    app.run(debug = False, host = '0.0.0.0', port = 8000, threaded = True)

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()