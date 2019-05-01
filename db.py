import pymysql.cursors
import genpass

class Database(object):
    def __init__(self):
        self.host = "localhost"
        self.usrnme = "root"
        self.pswrd = ""  
        self.dbnme = "polls"
        self.connection = pymysql.connect(host=self.host,
                             user=self.usrnme,
                             password=self.pswrd,
                             db=self.dbnme,
                             cursorclass=pymysql.cursors.DictCursor)

    def con_auth(self, userid, user_pass):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM users WHERE userid='"+userid+"'"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
        try:
            userpass = check["user_pass"]
            if genpass.check_password_hash(userpass, user_pass):
                return check
        except:
            return None

    def register_user(self, username, user_pass):
        with self.connection.cursor() as cursor:
            hash_pass = genpass.User(username, user_pass)
            hash_pass = hash_pass.pw_hash
            com = "INSERT INTO users VALUES ('"+username+"', '"+hash_pass+"')"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()

    def addpoll(self, question, option1, option2, username, typePoll):
        with self.connection.cursor() as cursor:
            com = "INSERT INTO polling (question, op1, op2, op1count, op2count, userid, type) VALUES ('"+question+"', '"+option1+"', '"+option2+"', 0, 0, '"+username+"', '"+typePoll+"')"
            cursor.execute(com)
        self.connection.commit()

    def checkUser(self, userid):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM users WHERE userid='"+userid+"'"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
        return check

    def getPublicPolls(self, dummyData):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM polling WHERE type='public'"
            cursor.execute(com)
            check = cursor.fetchall()
        self.connection.commit()
        return check

    def getPrivatePolls(self, dummyData):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM polling WHERE type='private'"
            cursor.execute(com)
            check = cursor.fetchall()
        self.connection.commit()
        return check

    def getPollbyID(self, pollid):
        with self.connection.cursor() as cursor:
            com = "SELECT * from polling WHERE un_id="+pollid
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
        return check

    def giveVote(self, pollid, option, count):
        with self.connection.cursor() as cursor:
            com = "UPDATE polling SET "+option+"count="+count+" WHERE un_id="+pollid
            cursor.execute(com)
            self.connection.commit()