
from app.models.db import init_db

users = []

class UsersData():
    def __init__(self):
        self.db = init_db()
        self.curr = self.db.cursor()

    def save(self, username, email, password, role):
        self.curr.execute("INSERT INTO users (username, email, password, role) VALUES(%s,  %s,  %s,  %s)", (username, email, password, role))
        return self.db.commit()

    def login(self, email, password):
        self.curr.execute("SELECT role FROM users WHERE email=(%s) AND password=(%s)",(email, password,))
        role = self.curr.fetchone()
        return role
    
    def get_user(self, email):
        self.curr.execute("SELECT * FROM users WHERE email=%s", (email,))
        user_data = self.curr.fetchone()
        if not user_data:
            return {"message":"User not found"}

        for user in user_data:
            user = dict(
                email = user_data[2],
                employee_no = user_data[0],
                role = user_data[4],
                password = user_data[1]
            )
            users.append(user)
        return user
    
    def get_all_users(self):
        self.curr.execute("SELECT * FROM users")
        data = self.curr.fetchall()
        users = []
        for i,items in enumerate(data):
            employee_no, username, email, password, role = items
            fetched_data = dict(
                employee_no = employee_no,
                username = username,
                email = email,
                password = password,
                role = role
            )
            user = [user for user in users if email == user["email"]]
            if user:
                response = users
            else:
                users.append(fetched_data)
        response = users
        return response   
         