## AI Coder
- https://chat.deepseek.com/coder
- https://claude.ai/chat/


## TODO

- test `app-v5.py`

## Dev

### v5 - add user admin

After merging codes by you and me, I have tested the added features of user registration and login. After some refactoring and changes, it works!
Great job, Claude!

Can you add a new feature to administrate users for a super-user?
1) The super-user should be the very first user who registers and logins into this task manager app, where is_admin flag is set to 1, any other subsequent  users will be normal user with is_admin flag set to 0;
2) For an admin user, please add additional menu items such as
(a) add user
(b) edit user , these two flag fields (is_admin, is_active) should be editable
(c) we don't hard-delete record in habits7_user table, 
but when the user has is_active = 0, that user is soft-deleted and login is denied
3) A normal user should have access to "edit user" menu item, 
but these two flag fields (is_admin, is_active) should be hidden 

the app-v4-claude.py is pasted here: <pasted>



### v4 - add user

app-v4-claude.py prompt
```
I have a basic streamlit app to manage tasks, 
can you add 2 new features: 
1) user registration; 
2) login, 

a table called "habits7_user" is used to store user information such as : 
""" 
email TEXT NOT NULL,
password TEXT,
username text,
is_admin  in  default 0 in (0,1),
is_active int default 1 in (0,1),
profile text,
note TEXT,
created_by TEXT,
created_at TEXT,
updated_by TEXT,
updated_at TEXT
"""

the app-v3.py is pasted here: <pasted>
```


## Misc
```
- h7admin@gmail.com
- h7admin@gmail.com

```
