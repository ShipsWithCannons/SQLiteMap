import sqlite3
import json
import codecs


def main():
    OUTPUT_FILE = 'locations.js'

    conn = sqlite3.connect('geodata.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Locations')
    filehandle = codecs.open(OUTPUT_FILE, 'w', "utf-8")
    filehandle.write("locations = [\n")
    count = 0
    for row in cur:
        '''
        row[0]: target
        row[1]: address
        row[2]: lat & long
        '''
        target = str(row[0]).split(',')[0]
        data = str(row[2])
        try:
            js = json.loads(str(data))
        except:
            continue

        if not('status' in js and js['status'] == 'OK'):
            continue

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0:
            continue
        loc = js['results'][0]['formatted_address'].replace("'", "")
        try:
            print target, loc, lat, lng

            count = count + 1
            if count > 1:
                filehandle.write(",\n")
            output = "['"+target+"',"+str(lat)+","+str(lng)+"]"
            filehandle.write(output)
        except:
            continue

    filehandle.write("\n];\n")
    cur.close()
    filehandle.close()
    print count, "records written to", OUTPUT_FILE

if __name__ == '__main__':
    main()
