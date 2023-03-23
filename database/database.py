import sqlite3
from passlib.hash import sha256_crypt

database = (r"database/ClearMapDB.db")

def createConnection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def createTable(conn, tableSQL):
    try:
        cur = conn.cursor()
        cur.execute(tableSQL)
    except sqlite3.Error as e:
        print(e)


def main():
    userTable = """CREATE TABLE IF NOT EXISTS "users" (
                            "UserId"	INTEGER,
                            "Username"	TEXT NOT NULL,
                            "Password"	TEXT NOT NULL,
                            "Email"	TEXT NOT NULL,
                            "Name"	TEXT NOT NULL,
                            PRIMARY KEY("UserId" AUTOINCREMENT)
                        ); """

    addressTable = """CREATE TABLE IF NOT EXISTS "address" (
                            "AddressId"	INTEGER,
                            "Address"	TEXT NOT NULL,
                            "Postcode"	TEXT NOT NULL,
                            "AddressTitle"	TEXT NOT NULL,
                            "Lat"	REAL,
                            "Long"	REAL,
                            "Favourite"	INTEGER,
                            "UserId"	INTEGER NOT NULL,
                            FOREIGN KEY("UserId") REFERENCES "users"("UserId"),
                            PRIMARY KEY("AddressId" AUTOINCREMENT)
                        );"""# bool values 1 = true, 0 = false stored as int
        
    journeyTable = """CREATE TABLE IF NOT EXISTS "journey" (
                            "JourneyId"	INTEGER,
                            "StartAddressId"	INTEGER NOT NULL,
                            "EndAddressId"	INTEGER NOT NULL,
                            "JourneyName"	TEXT NOT NULL,
                            "Distance"	REAL,
                            "JourneyTime"	REAL,
                            "UserId"	INTEGER NOT NULL,
                            FOREIGN KEY("UserId") REFERENCES "users"("UserId"),
                            FOREIGN KEY("StartAddressId") REFERENCES "address"("AddressId"),
                            FOREIGN KEY("EndAddressId") REFERENCES "address"("AddressId"),
                            PRIMARY KEY("JourneyId" AUTOINCREMENT)
                        );"""

    conn = createConnection(database)

    createTable(conn, userTable)
    createTable(conn, addressTable)
    createTable(conn, journeyTable)
    
    conn.close()

def addUser(data):
    conn = createConnection(database)
    sql = ''' INSERT INTO users(Username,Password,Email,Name)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    conn.close()

def authenticate(username, password):
    sql = ''' SELECT * FROM users WHERE username = ? '''
    conn = createConnection(database)
    cur = conn.cursor()
    username = username,
    checkExists = ''' SELECT EXISTS({0}) '''.format(sql)
    if (cur.execute(checkExists, username)).fetchone() == (1,):
        cur.execute(sql, username)
        if sha256_crypt.verify(password, cur.fetchone()[2]):
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        conn.close()
        return False

def noUsernameExists(username):
    sql = ''' SELECT EXISTS(SELECT * FROM users WHERE username = ?) '''
    conn = createConnection(database)
    cur = conn.cursor()
    username = username,
    if(cur.execute(sql, username)).fetchone() == (1,):
        conn.close()
        return False
    conn.close()
    return True
    
def updateUsername(newUsername, oldusername):
    conn = createConnection(database)
    sql = ''' UPDATE users SET username =? WHERE username = ?'''
    cur = conn.cursor()
    data = (newUsername, oldusername)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return True

def updatePassword(newpassword, username):
    conn = createConnection(database)
    newpassword = sha256_crypt.encrypt(newpassword)
    sql = ''' UPDATE users SET password =? WHERE username = ?'''
    cur = conn.cursor()
    data = (newpassword, username)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return True

def getUserId(username):
    sql = ''' SELECT * FROM users WHERE username = ? '''
    conn = createConnection(database)
    cur = conn.cursor()
    username = username,
    cur.execute(sql, username)
    userId = cur.fetchone()[0]
    conn.close()
    return userId

def getUsername(email):
    sql = ''' SELECT * FROM users WHERE email = ? '''
    conn = createConnection(database)
    cur = conn.cursor()
    email = email,
    cur.execute(sql, email)
    username = cur.fetchone()[1]
    conn.close()
    return username

def emailExists(email):
    sql = ''' SELECT EXISTS(SELECT * FROM users WHERE Email = ?) '''
    conn = createConnection(database)
    cur = conn.cursor()
    email = email,
    if(cur.execute(sql, email)).fetchone() == (1,):
        conn.close()
        return True
    conn.close()
    return False

def newAddress(address, userId):
    sql = ''' SELECT EXISTS(SELECT * FROM address WHERE UserId = ? AND Address = ?)'''
    conn = createConnection(database)
    cur = conn.cursor()
    data = (userId, address)
    if(cur.execute(sql, data)).fetchone() == (1,):
        conn.close()
        return False
    conn.close()
    return True

def addAddress(data):
    conn = createConnection(database)
    sql = ''' INSERT INTO address(Address,Postcode,AddressTitle,Lat,Long,Favourite,UserId)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    conn.close()

def getAddressId(address, username):
    sql = ''' SELECT AddressId FROM address WHERE address = ? AND UserId = ?'''
    conn = createConnection(database)
    cur = conn.cursor()
    userId = getUserId(username)
    data = (address, userId)
    cur.execute(sql, data)
    AddressId = cur.fetchone()[0]
    conn.close()
    return AddressId

def getAddresses(username):
    userId = getUserId(username),
    sql = ''' SELECT AddressTitle, Address, Postcode FROM address WHERE UserId = ? AND Favourite = 1'''
    conn = createConnection(database)
    cur = conn.cursor()
    cur.execute(sql, userId)
    records = cur.fetchall()
    addresses = []
    for row in records:
        addresses.append(row)
    conn.close()
    return addresses

def addJourney(data):
    conn = createConnection(database)
    sql = ''' INSERT INTO journey(StartAddressId,EndAddressId,JourneyName,Distance,JourneyTime,UserId)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    conn.close()

def newJourney(name):
    sql = ''' SELECT EXISTS(SELECT * FROM journey WHERE JourneyName = ?)'''
    conn = createConnection(database)
    cur = conn.cursor()
    name = name,
    if(cur.execute(sql, name)).fetchone() == (1,):
        conn.close()
        return False
    conn.close()
    return True

def getJourneyNames(userId):
    sql = ''' SELECT j.*, 
a1.Address, 
a1.Postcode, 
a2.Address, 
a2.Postcode, 
(a1.Long||','||a1.Lat) AS startCoord, 
(a2.Long||','||a2.Lat) AS endCoord 
FROM journey AS j
JOIN address AS a1 ON j.StartAddressId = a1.AddressId
JOIN address AS a2 ON j.EndAddressId = a2.AddressId
WHERE j.UserId = ? '''
    conn = createConnection(database)
    cur = conn.cursor()
    userId = userId,
    cur.execute(sql , userId)
    journeyNames = cur.fetchall()
    conn.close()
    return journeyNames

def deleteJourney(journeyId):
    sql = ''' DELETE FROM journey WHERE JourneyId = ?'''
    journeyId = journeyId,
    conn = createConnection(database)
    cur = conn.cursor()
    cur.execute(sql, journeyId)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()