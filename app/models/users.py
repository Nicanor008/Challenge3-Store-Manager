from app.models.db import init_db

class UsersData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()
    
        select_user = """SELECT * FROM users"""
        self.curr.execute(select_user)
        self.result = self.curr.rowcount > 1

    def save(self, employeeno, username, email, password, role):

        payload = {
            'employeeno':employeeno,
            'username':username,
            'email':email,
            'password':password,
            'role': role
        }

        if self.result:
            return {"user already exist"}

        # if employeeno is in payload:
        #     return {"message":"user already exists"}

        query = """INSERT INTO users(employeeno, username, email, password, role) 
        VALUES(%(employeeno)s, %(username)s,  %(email)s,  %(password)s,  %(role)s)"""

        # curr = self.db.cursor()
        self.curr.execute(query, payload)
        return self.db.commit()

    def login(self, email, password):
        self.curr.execute('SELECT * FROM users WHERE email=%s AND password=%s',(email, password))
        users_data = self.curr.fetchall()
        return self.db.commit()

        
         