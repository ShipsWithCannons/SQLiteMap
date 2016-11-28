import urllib
import sqlite3
import json


def main():
    SERVICE_URL = "http://maps.googleapis.com/maps/api/geocode/json?"

    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Locations (target TEXT,
            address TEXT, geodata TEXT)''')

    filehandle = open("locations.data")
    count = 0
    for line in filehandle:
        target, _, address = line.partition(', ')
        address = address.strip()
        cur.execute(
                "SELECT geodata FROM Locations WHERE target= ?",
                (buffer(target), ))

        try:
            data = cur.fetchone()[0]
            print "Found in database ", address
            continue
        except:
            pass

        print 'Resolving', address
        url = SERVICE_URL + urllib.urlencode(
            {"sensor": "false", "address": address})
        print 'Retrieving', url
        urlhandle = urllib.urlopen(url)
        data = urlhandle.read()
        print 'Retrieved', len(data), \
              'characters', data[:20].replace('\n', ' ')
        count = count + 1
        try:
            js = json.loads(str(data))
        except:
            continue

        if 'status' not in js or (
                js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
            print '==== Failure To Retrieve ====', \
                  data
            break

        cur.execute('''INSERT INTO Locations (target, address, geodata)
                VALUES ( ?, ?, ? )''', (
                buffer(target), buffer(address), buffer(data)))
        conn.commit()

if __name__ == '__main__':
    main()
