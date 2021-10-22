"""
Questions:
- Will DBAccess be implemented as classes or just functions?
- Are we using snake_case or camelCase for functions?
- How do we want to handle missing data? Where do we want to handle it?
"""
import dbaccess


# Get a user's name from their netID
def get_users_name(netid):
    user = dbaccess.DBAccess().get_user(netid)
    if user is None:
        name = "Student"
    else:
        name = user.name

    return name
