from app.models.db import init_db

users = []

class UsersData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()

    def save(self, employee_no, username, email, password, role):
        self.curr.execute("INSERT INTO users(employee_no, username, email, password, role) VALUES(%s, %s,  %s,  %s,  %s)", (employee_no, username, email, password, role))
        return self.db.commit()

    def login(self, email, password):
        self.curr.execute("SELECT * FROM users WHERE email=(%s) AND password=(%s)",(email, password,))
        return self.curr.fetchone()
    
    def get_user(self, email):
        self.curr.execute("SELECT * FROM users WHERE email=%s", (email,))
        data = self.curr.fetchone()
        
        # role = data['role']

        return data

        
         