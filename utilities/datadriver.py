import pandas as pd
import matplotlib.pyplot as plt
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
#READ THE DOCS (PANDAS): https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
#READ THE DOCS (MySQL): https://dev.mysql.com/doc/refman/8.0/en/entering-queries.html

DATABASE_USER= os.getenv('DATABASE_USER')
DATABASE_PASS = os.getenv('DATABASE_PASS')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

config = {
        'user': DATABASE_USER,
        'password': DATABASE_PASS,
        'host': DATABASE_HOST,
        'database': DATABASE_NAME,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def addUser(userID, username, addy, filename, total = 0, streak = 0, ranking = 1000, win = 0, loses = 0, inchallenge = 0):
        #PANDAS VERSION
        #newUser = pd.DataFrame.from_dict({userID: [username,win,loses,total,streak,ranking,addy,inchallenge]},orient='index', columns = ['USERNAME','WINS','LOSES','TOTAL','STREAK','RANK','ETH_ADDY','IN_CHALLENGE'])
        #_dataframe = dataframe.append(newUser)
        #saveTable(_dataframe, filename)

        #SQL VERSION
        profileurl = uploadImage(filename)
        query = ("INSERT INTO leaderboard_user(id,wins,loses,total,streak,ranking,eth_addy,in_challenge,username,profileurl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        data = (userID,win,loses,total,streak,ranking,addy,inchallenge,username,profileurl)
        cursor.execute(query,data)
        cnx.commit()
        print(cursor)

        
#Not needed with SQL rewrite       
def locateUser(dataframe,userID):
        
        try:
                indexList = dataframe.index # returns Int64Index[] https://www.dataforeverybody.com/convert-pandas-index-list-array/
                stdlist = list(indexList)
                userIndex = stdlist.index(userID)
                return userIndex
        except:
                return -1


def getUserRow(userID):

        query = ("SELECT * FROM leaderboard_user WHERE id = %s")
        data = (userID,)
        try:
                cursor.execute(query,data)
                result = cursor.fetchone()
                return list(result)
        except: 
                return -1


        #userdataobject = dataframe.iloc[userIndex]

        #if header != '':
        #        value = userdataobject[header]
        #        return value
        #else:
        #        return userdataobject
       # 
        #to do, access data by index following lookup


def loadTable(filename):
        dataframe = pd.read_csv(filename, index_col=0)
        print(dataframe)
        return dataframe

def updateUserValue(userID,header,value = 0, reset = 0):
        if header == 'WINS' or header == 'TOTAL' or header == 'LOSES':
                query = ("UPDATE leaderboard_user SET {0} = {0} + 1 WHERE id = {1}".format(header,userID))
                #dataframe.at[userID,header] += 1
        if header == 'STREAK':
                if reset != 0:
                        #dataframe.at[userID,header] = 0
                        query = ("UPDATE leaderboard_user SET {0} = 0 WHERE id = {1}".format(header,userID))
                else:
                        #dataframe.at[userID,header] += 1
                        query = ("UPDATE leaderboard_user SET {0} = {0} + 1 WHERE id = {1}".format(header,userID))
        if header == 'RANK' or header == 'ETH_ADDY' or header == 'IN_CHALLENGE':
                #dataframe.at[userID,header] = value
                query = ("UPDATE leaderboard_user SET {0} = {2} WHERE id = {1}".format(header,userID,value))
        
        #saveTable(dataframe, 'database/ultimate.csv' ) #need to change literal filename passed
        
        try:
                cursor.execute(query)
                cnx.commit()
                return 1
        except: 
                return -1


#TIP: The headers for each column in the dataframe is TOTAL, STREAK, and ACTIVEFLAG 
def getUserValue(userID,header):
        #userIndex = locateUser(dataframe,userID)
        #row = dataframe.iloc[userIndex]
        #value = row[header]
        #print(header)
        query = ("SELECT {0} FROM leaderboard_user WHERE id = %s".format(header))
        #print(query)
        data = (userID,)
        cursor.execute(query,data)
        try:
                result = list(cursor.fetchone()) #All rows need to be fetched in order for connection to do new query. userID is PK -> should return only one.
        except:
                return -1
        
        return result[0]

def saveTable(dataframe,filename):
        dataframe.to_csv(filename)
        print('File Updated!')

#pass guild parameter in rewrite
def generateLeaderBoard(dataframe):
        #frame = loadTable()
        plt.figure()
        dataframe.plot.barh(y = 'TOTAL')
        plt.savefig("output.png")
        filename = "output.png"
        return filename

#https://github.com/Imgur/imgurpython
from imgurpython import ImgurClient
def uploadImage(filename):

        client_id = os.getenv('IMGUR_ID')
        client_secret = os.getenv('IMGUR_SECRET')
        client = ImgurClient(client_id, client_secret)

        #Here's the metadata for the upload. All of these are optional, including
        #this config dict itself.
        #config = {
        #	'album': album,
        #	'name':  'Catastrophe!',
        #	'title': 'Catastrophe!',
        #	'description': 'Cute kitten being cute on {0}'.format(datetime.now())
        #}

        print("Uploading image... ")
        picturepath = "profilepics/{}.png".format(filename)
        image = client.upload_from_path(picturepath)
        print("Done")
        print(image['link'])
        return image['link']


#Used for testing local functions
if __name__ == "__main__":
    #addUser(898989,"addUserTest","testAddy")
    print(getUserValue('355178090231758850','total'))
    print(getUserRow(355178090231758850))
    result = getUserRow(355178090231758850)