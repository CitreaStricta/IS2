users = []
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None