import os
import shutil
import re
import time 
import sqlite3
import sys
from urllib.request import pathname2url
from os import system, name
from time import sleep 
    
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Adding comment here
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    pass

else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

user_id=None
choice=None
inputagain=None 
count=0 
u1=None
u2=None
contactnumber_id=None
class ContactBook:
    conn=None 
    c=None 
    username=None
    loginname=None  
    def __init__(self):
        self.conn=None
        self.c=None 
    def connect2(self):
        pass

    def connect(self,username):
        username=username+'.db'
        self.conn=sqlite3.connect(username)
        self.c=self.conn.cursor()
        self.loginname=username

    def checkdatabasefileexitornot(self,username):
        databasename=username+'.db'
        try:
            dburi = 'file:{}?mode=rw'.format(pathname2url(databasename))
            self.conn = sqlite3.connect(dburi, uri=True)
            self.c=self.conn.cursor()
           
            #print("You are a already user of ContactBOOK")
            loginname2=username.split('@')
            #print(f'Hi User "{loginname2[0]}" \n')
            #print(f'Hi User {loginname2[0]}' ',' 'you have successfully SignedIN now ')
            
            return 1
        except sqlite3.OperationalError:
            
            #print("In Exception ")
            return 0

    def createdatabase(self,username):
        returnvalue=d1.checkdatabasefileexitornot(username)
        if returnvalue==1:
            return 1
        if returnvalue==0:
            
            d1.connect(username)

            self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Users' ''')

            if self.c.fetchone()[0]==1 : {
                #print('Table exists.')
            
            }
            else:
                #print("Table is not exit")

                self.c.execute("""CREATE TABLE Users
                (
                user_id INTEGER NOT NULL PRIMARY KEY,
                username TEXT NOT NULL,
                userregisterednumber INTEGER
                )
                """)



                self.c.execute("""CREATE TABLE ContactNumber
                (
                contactnumber_id INTEGER NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                phonenumber INTEGER,
                address TEXT,
                email TEXT,
                contactcreationdate TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (user_id)
                )
                """)

                #print("Database and tables are created")
           
    def insertnumber(self,user_id):

        name=input(" Enter name ")
        phonenumber=input(" Enter number ")
        address=input(" Enter Address ")
        email=input(" Enter email ")
        contactcreationdate=time.asctime(time.localtime(time.time()))
        user_id=user_id

        self.c.execute("INSERT INTO ContactNumber (name,phonenumber,address,email,contactcreationdate,user_id) VALUES(?,?,?,?,?,?)", 
                                                    (name,phonenumber,address,email,contactcreationdate,user_id)) 

        self.conn.commit()    

        print(f'Conatct {name} has been inserted successfully')

        
    
    def findcontact(self,user_id):

        name=input("Input a name to find the Contact Details")

        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where name=? and user_id=?"""

        data=(name,user_id)
        self.c.execute(sql_select_query,data)
        
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list")
            print("You can add contact add new contacts by option 1")
        else:

            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

    def deletenumber(self,user_id):
        print("Current Contact List: ")

        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where user_id=?"""
        self.c.execute(sql_select_query,(user_id, ))
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list")
            print("You can add contact add new contacts by option 1")
        else:

            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

            name=input("Inpute a name to Delete ")

            sql_delete_query="""delete from ContactNumber where name =? and user_id=?"""
            data=(name,user_id)
            self.c.execute(sql_delete_query,data)
            self.conn.commit()
            print(f' {name} has been deleted sucussfully')

    def updatethecontact(self,user_id):

        name=input("Input a name to Update the Details ")

        print("User ID:",user_id)
        print("name: ",name)
        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where name=? and user_id=?"""
        data=(name,user_id)
        self.c.execute(sql_select_query,data)
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list ")
            print("You can add contact add new contacts by option 1 ")
        else:
            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))
            
            updatednumber=input(f'Enter a number you want to upadte for {name} ')

            sql_update_query="""Update ContactNumber set phonenumber = ? where name = ?"""
            data=(updatednumber,name)
            self.c.execute(sql_update_query,data)
            self.conn.commit()
            print("Contact Number has been Updated ")
            sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where name=?"""
            self.c.execute(sql_select_query,(name, ))
            records=self.c.fetchall()
            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

    def listinalphabeticalorder(self,user_id):

        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where user_id=? order by name ASC"""
        self.c.execute(sql_select_query,(user_id, ))
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list")
            print("You can add contact add new contacts by option 1")
        else:
            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

    def listcontactsbycreationdate(self,user_id):
        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where user_id=? order by contactcreationdate"""
        self.c.execute(sql_select_query,(user_id, ))
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list")
            print("You can add contact add new contacts by option 1")
        else:
            formatted_row='{:<15} {:<12} {:<10} {:<25} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

    def saveContacts(self,user_id):

        user_id=user_id

        sql_select_query="""select username from Users where user_id=?"""

        self.c.execute(sql_select_query,(user_id, ))

        row=self.c.fetchone()
        username=row[0]
        d1.connect(username)   
        f= drive.CreateFile()

        username=username+'.db'
        f.SetContentFile(username)
        f.Upload()
        #print('title: %s, mimeType: %s' % (f['title'], f['mimeType']),'ID: ',f['id'])
        #print("Your contacts have been stored on Google Drive succesfully")

    def registeredusers(self):
        for i in self.c.execute("select * from Users"):
            print(i)
    def signup(self):
        print("\nEnter below details for Signup\n")
               
        while True:
            username=input("Enter your email id as your usernname \n")    
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            if(re.search(regex,username)):  
                break
            else:  
                print("Invalid Email format, please try again")
                continue  

        while True:
            doublecheck=input("Please reenter your email id as your usernname \n")
            if not username==doublecheck:
                print("Your email ID's didn't matched, please try again ")
                continue
            else:
                break

        while True:
            userregisterednumber=input("Enter your mobile number for registration \n")

            if not userregisterednumber.isdigit():
                print("Enter a valid mobile number")
            
                continue
            else:
                break

        cdreturn=d1.createdatabase(username)
        if cdreturn==1:
            return 1

        self.c.execute("INSERT INTO Users (username,userregisterednumber) VALUES(?,?)", 
                                                    (username,userregisterednumber))

        self.conn.commit()

        try:

            sql_select_query="""select user_id from Users where username=? and userregisterednumber=?"""
            data=(username,userregisterednumber)
            self.c.execute(sql_select_query,data)

            row=self.c.fetchone()
            number=(row[0])
            #print(type(number))
            return number
        except TypeError:
                print("username or mobile number is not valid\n")

    def backupfromgoogledrive(self,username,number):
        usernametogetregisternumber=username
        count=0
        databasename=username+'.db'
        path=os.getcwd()
        dirName='googledrivebackup'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            #print("Directory " , dirName ,  " Created ")
        else:    
            #print("Directory " , dirName ,  " already exists")
            pass

        src=path+'\\'+dirName+'\\'+databasename
        dst=path
        username_2=username+'.db'
        tablename=username_2
        file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
        for file1 in file_list:
            if (file1['title'])==tablename:
                #print("Table found",file1['title'],"ID : ",file1['id'])
                getthefile=drive.CreateFile({'id':file1['id']})
                newpath='googledrivebackup/'+username_2
                getthefile.GetContentFile(newpath)
                newconn=sqlite3.connect(newpath)
                cnew=newconn.cursor()
                try:
                    sql_select_query="""select user_id from Users where username=? and userregisterednumber=?"""
                    data=(username,number)
                    try:
                        cnew.execute(sql_select_query,data)
                        rows=cnew.fetchall()
                        #print("rows ",rows)
                        if len(rows)==0:
                            #print("It looks you dont have backup on google drive")

                            #print("You have to stored the data on Google Drive first")
                            return 0
                            break
                        else:
                            shutil.copy2(src,dst)
                            #print("Your data has been restored")
                            return 1

                    except sqlite3.Error as e:
                        #print("It looks you dont have backup on google drive")

                        #print("You have to stored the data on Google Drive first")
                        return 0
                        break

                except sqlite3.Error as e:
                    print("From Exception username or mobile number is not valid\n",e.args[0])  
                    return 0
                count=count+1
                break    

        if count==0:
            
            #print("It looks you dont have backup on google drive")
            #print("You have to stored the data on Google Drive first")
            return 0
        


    def getthecontactList(self,user_id):
        print("Contact Details")
        sql_select_query="""select name,phonenumber,address,email,contactcreationdate from ContactNumber where user_id=?"""
        self.c.execute(sql_select_query,(user_id, ))
        records=self.c.fetchall()
        if len(records)==0:
            print("It looks you are a new user, you dont have contacts in your list")
            print("You can add contact add new contacts by option 1")
        else:
            formatted_row='{:<20} {:<12} {:<10} {:<30} {:<15}'
            print(formatted_row.format("name","phonenumber","address","email","contactcreationdate"))
            for rows in records:
                print(formatted_row.format(*rows))

    def gettheusername(self,user_id):
        sql_select_query="""select username from Users where user_id=?"""

        self.c.execute(sql_select_query,(user_id, ))

        row=self.c.fetchone()
        username=row[0]

        sql_select_query="""select userregisterednumber from Users where user_id=?"""

        self.c.execute(sql_select_query,(user_id, ))

        row=self.c.fetchone()
        userregisterednumber=row[0]
        
        return username,userregisterednumber

    def gettheUser(self):
        yesorno2=None
        user_id=None  
        count=0
        global row
        useridnumber=None
        
        print()
        print("=======WELCOME TO CONTACT BOOK=======")
        
        while True:

            yesorno=input("\nFor SIGNIN type 'yes' \n\nNew to ORDER BOOK? for SIGN UP type 'no' ")
            if not re.match("yes|no",yesorno):
                print("Enter valid input")
            else:
                break
        if yesorno=="no":
            user_id=d1.signup()
            return user_id
        if yesorno =="yes":
            while True:
                if count>3:
                    print("You have reched to the maximum login attempt, please try again")
                    break
                if count>0:
                    print("You have entered the wrong login details, please try again \n")
                    #print("Type 'yes' to try again 'no' to SIGNUP ")
                    while True:
                        yesorno2=input("Type 'yes' to try again 'no' to SIGNUP ")
                        if not re.match("yes|no",yesorno2):
                            print("Enter valid input")
                        else:
                            break

                if yesorno2=="no":
                            
                    user_id=d1.signup()
                    return user_id

                if yesorno2=="yes":
                    print("You have typed yes ")
                        
                if yesorno=="yes":
                    print("Enter your email/username and registered number for login\n")

                    while True:
                        name=input("Enter your email ID ")
                        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                        if(re.search(regex,name)):  
                            break
                        else:  
                            print("Invalid Email format, please try again")
                            continue 
                
                    while True:
                        number=input("Enter your registered mobile number")
                        if not number.isdigit():
                            print("Enter a valid mobile number")
                            continue
                        else:
                            break                   
                    
                    count=count+1
                    returnvalue=d1.checkdatabasefileexitornot(name)
                    if returnvalue==0:
                        #print("Your data is not on your local ")
                        valuefromgoogledrivebackup=d1.backupfromgoogledrive(name,number)
                        if valuefromgoogledrivebackup==1:
                            d1.connect(name)
                            return valuefromgoogledrivebackup
                        if valuefromgoogledrivebackup==0:
                            continue  
                    sql_select_query="""select user_id from Users where username=? and userregisterednumber=?"""
                    data=(name,number)
                    try:                      
                        self.c.execute(sql_select_query,data)
                    except:
                        #print("Exception handling 'no such table:Users'")
                        valuefromgoogledrivebackup=d1.backupfromgoogledrive(name,number)
                        if valuefromgoogledrivebackup==1:
                            return valuefromgoogledrivebackup
                        if valuefromgoogledrivebackup==0:
                            continue                   
                    row=self.c.fetchone()            
                    try:
                        useridnumber=row[0]
                        
                        return useridnumber
                    except:
                        if useridnumber==None:
                            valuefromgoogledrivebackup=d1.backupfromgoogledrive(name,number)
                            if valuefromgoogledrivebackup==1:
                                return valuefromgoogledrivebackup
                            if valuefromgoogledrivebackup==0:
                                continue
    def clear(self): 
        if name == 'nt': 
            _ = system('cls') 
        else: 
            _ = system('clear') 

    def getthechoice(self):

            sleep(1)
            #d1.clear()
            while True:
                
                #loginname2=self.loginname.split('@')
                #print(f'Hi User "{loginname2[0]}" \n')
                print("1 to Add new Number ")
                print("2 to find the contact ")
                print("3 to Delete a number ")
                print("4 to update the contact list")
                print("5 to get the Contact List ")
                print("6 to get the Contact List in Alphabetical Order ")
                print("7 to get the contacts using contact creation date. ")
                #print("8 Save the Contacts on your Google Drive ")
                #print("9 Get the Contacts from your Google Drive ")
                print("0 to Exit")

                choice= input("Enter the choice from above ")
                if choice.isdigit():
                    if int(choice)>7:
                        print("Please enter the valid option ")
                    else:
                        return int(choice)
                else:
                    print("Please enter the valid option ")


d1=ContactBook()
user_id=d1.gettheUser()
#print("USER ID: ",user_id)

if user_id==None:
    pass
    #print("Its None returned")
else:
    username1=d1.gettheusername(user_id)
    username2=username1[0].split('@')
    #print(username2[0])
    #print("User ",username1[0].split('@').[0])
    print(f'User "{username2[0]}" has been succussfully logged in ')
    while True:
            if user_id==0:
                break
            if count>2:
                break
            if choice==1:
                d1.insertnumber(user_id)
                d1.saveContacts(user_id)
            if choice==2:
                d1.findcontact(user_id)
            if choice==3:
                d1.deletenumber(user_id)
                d1.saveContacts(user_id)
            if choice==4:
                d1.updatethecontact(user_id)
                d1.saveContacts(user_id)
            if choice==5:
                d1.getthecontactList(user_id)
            if choice==6:
                d1.listinalphabeticalorder(user_id)
            if choice==7:
                d1.listcontactsbycreationdate(user_id)
            #if choice==8:
            #    d1.saveContacts(user_id)
            if choice==8:
                username1,number=d1.gettheusername(user_id)
                d1.backupfromgoogledrive(username1,number)
            if choice==10:
                d1.registeredusers()        
            if choice==0:
                break
            while True:
                
                togetthechoice=input(f'\nType yes to continue or no to exit ' )
                if not re.match("yes|no",togetthechoice):
                    print("Enter valid input")
                else:
                    break
            if togetthechoice=='yes':
                choice=d1.getthechoice()
            if togetthechoice=='no':
                break

