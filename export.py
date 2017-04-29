#export tracking data to TrackMeViewer (https://github.com/espinosaluis/TrackMeViewer).
import MySQLdb
import datetime

def cuttext( str ):
        out = str.split(":", 1)[-1]
        return out;

now = datetime.datetime.now()
nowdate = str(now.year) + '.' + str(now.month) + '.' + str(now.day) + '_' + str(now.hour) + ':' + str(now.minute)
connection = MySQLdb.connect(host='127.0.0.1', user='trackme', passwd='xxxx', db='trackme')
cursor = connection.cursor()
cursor.execute('insert into trips values (null, 3, "track_' + nowdate + '", NULL, 0);')
connection.insert_id()
id = cursor.lastrowid

file = open('final')
for line in file:
        y = line.strip().split(";")
        long = cuttext(y[3])
        lat = cuttext(y[4])
        speed = float(cuttext(y[5])) / 3.6
        date = cuttext(y[6])
        time = cuttext(y[7])
        d = date[4] + date[5]
        m = date[2] + date[3]
        yr = date[0] + date[1]
        h = time[0] + time[1]
        min = time[2] + time[3]
        s = time[4] + time[5]
        timestamp = '20' + yr + '-' + m + '-' + d + ' ' + h + ':' + min + ':' + s
        sql='insert into positions values (NULL, 3, ' + str(id) + ', NULL, ' + str(long) + ', ' + str(lat) + ', 0, ' + str(speed) + ', 0, NULL, "' + str(timestamp) + '", NULL, NULL, NULL, NULL, NULL, NULL)'
        #print values
        cursor.execute(sql)
        # Close the cursor
cursor.close()

# Commit the transaction
#database.commit()

# Close the database connection
#database.close()
