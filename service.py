"""
Questions:
- Will DBAccess be implemented as classes or just functions?
- Are we using snake_case or camelCase for functions?
- How do we want to handle missing data? Where do we want to handle it?
"""

# Get a user's name from their netID
def getUserName(netId):
  # FIXME: Replace this with whatever fancy function Derek comes up with
  name = DBAccess.getUserName(netId)
  if name is None:
    name = "Student"

  return name
