In [1]: def make_dory_forget(dory):
   ...:     if dory.transactions:
   ...:         for item in dory.transactions:
   ...:             db.session.delete(item)
   ...:             db.session.commit()
   ...:     db.session.delete(dory)
   ...:     db.session.commit()    
   ...:     return User.query.filter(User.fname == "Dory").first()
