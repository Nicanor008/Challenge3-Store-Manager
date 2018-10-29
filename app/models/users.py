from app.models.db import init_db

class UsersData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()
    
        select_user = """SELECT * FROM users"""
        self.curr.execute(select_user)
        self.result = self.curr.rowcount > 1

    def save(self, employeeno, username, email, password, role):
        if self.result:
            return {"user already exist"}

        # if employeeno is in payload:
        #     return {"message":"user already exists"}

        # curr = self.db.cursor()
        self.curr.execute("INSERT INTO users(employeeno, username, email, password, role) VALUES(%s, %s,  %s,  %s,  %s)", (employeeno, username, email, password, role))
        return self.db.commit()

    def login(self, email, password):
        if not email:
            response = "failed"
        query = self.curr.execute('SELECT email,password FROM users WHERE email=%s AND password=%s',(email, password))
        if not query:
            response = 'failed'
        else:
            self.curr.fetchone()
            response = self.db.commit()
    
    def get_user(self, email):
        self.curr.execute("SELECT * FROM users WHERE email=%s", (email,))
        data = self.curr.fetchone()
        
        # role = data['role']

        return data

        
         