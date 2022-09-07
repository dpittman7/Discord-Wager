import pandas as pd
import matplotlib.pyplot as plt


#READ THE DOCS: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

def addUser(dataframe, userID, username, addy, filename, total = 0, streak = 0, rank = 1000, win = 0, loses = 0, inchallenge = 0):
        #appends user
        
        newUser = pd.DataFrame.from_dict({userID: [username,win,loses,total,streak,rank,addy,inchallenge]},orient='index', columns = ['USERNAME','WINS','LOSES','TOTAL','STREAK','RANK','ETH_ADDY','IN_CHALLENGE'])
        _dataframe = dataframe.append(newUser)
        saveTable(_dataframe, filename)
        
        
def locateUser(dataframe,userID):
        
        try:
                indexList = dataframe.index # returns Int64Index[] https://www.dataforeverybody.com/convert-pandas-index-list-array/
                stdlist = list(indexList)
                userIndex = stdlist.index(userID)
                return userIndex
        except:
                return -1


def retreiveUserDataObject(dataframe, userID, header = ''):

        
        try:
                userIndex = locateUser(dataframe,userID)
        except: 
                return -1

        userdataobject = dataframe.iloc[userIndex]

        if header != '':
                value = userdataobject[header]
                return value
        else:
                return userdataobject
        
        #to do, access data by index following lookup


def loadTable(filename):
        dataframe = pd.read_csv(filename, index_col=0)
        print(dataframe)
        return dataframe

def updateUserValue(dataframe,userID,header, value = 0, reset = 0):
        if header == 'WINS' or header == 'TOTAL' or header == 'LOSES':
                dataframe.at[userID,header] += 1
        if header == 'STREAK':
                if reset != 0:
                        dataframe.at[userID,header] = 0
                else:
                        dataframe.at[userID,header] += 1
        if header == 'RANK' or header == 'ETH_ADDY' or header == 'IN_CHALLENGE':
                dataframe.at[userID,header] = value
        

        
        saveTable(dataframe, 'database/ultimate.csv' ) #need to change literal filename passed

#TIP: The headers for each column in the dataframe is TOTAL, STREAK, and ACTIVEFLAG 
def getUserValue(dataframe,userID,header):
        userIndex = locateUser(dataframe,userID)
        row = dataframe.iloc[userIndex]
        value = row[header]
        return value

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

        client_id = 'd478e014ceab2f5'
        client_secret = '1a195891c34e64b794ee561bbf615cf4c07f6465'
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
        image = client.upload_from_path(filename)
        print("Done")
        print()

        return image['link']



