import grp
import pwd
import os
import ldap
import subprocess
 



# LDAP admin password
def input_ldap_pass():
     return getpass.getpass("Enter LDAP manager password: ")


def input_data():                                                  
    user = {}
    # name
    user['firstname'] = raw_input("Firstname: ")
    user['lastname'] = raw_input("Lastname: ")

    # user's name
    user['username'] = raw_input("Username: ")
    if (check_username(user["username"])):
        print("This username is already used!")
        exit()
   
   # UID
    uid = raw_input("UID (or empty for generate): ")
    if (uid == ""): 
        user['uid'] = generate_uid()
    else: 
        uid = int(uid)
        if (check_uid(uid)):
            print("This UID is already used!")
            exit()
        else:
            user['uid'] = uid

    # group's name
    user['group'] = raw_input("Group name: ")
    if (not(check_group(user['group']))):
        print("No such group found!")
        exit()

    # login shell
    shell = raw_input("Login shell [default is /bin/false]: ")
    if (shell == ""): 
        user['shell'] = DEFAULT_SHELL
    else:
        user['shell'] = shell;

# to return path of users home directory on this filesystem 
def home_path(username):
     dir="/mnt/home"
     return dir + '/' + username

# this is going to try to bind to LDAP with admin DN and give password and exit
def try_ldap_bind(admin_pass):
    ldap_ad = "ldap://localhost"
    try:
        ldap_conn = ldap.initialize(ldap_ad)
    except ldap.SERVER_DOWN:
        print("Can't contact LDAP server")
        exit()
        
    try:
        ldap_conn.simple_bind_s(cn=classroom,dc=example,dc=com,admin_pass)
    except ldap.INVALID_CREDENTIALS:
        print("This password is incorrect!")
        exit()
    print("Authorization successful")
    print("")

# to create new entry in LDAP for given user
def create_user(user, admin_pass):
    home="/home"
    dn = 'uid=' + user['username'] + ',' + dc=example,dc=com
    fullname = user['firstname'] + ' ' + user['lastname']
    home_dir = home + '/' + user['username']
    gid = find_gid(user['group'])

    entry = []
    entry.extend([
        ('objectClass', ["person", "organizationalPerson", "inetOrgPerson", "posixAccount", "top", "hostObject"])
        ('cn', fullname),
        ('givenname', user['firstname']),
        ('sn', user['lastname']),
        ('uidNumber', str(user['uid'])),
        ('gidNumber', str(gid)),
        ('loginShell', user['shell']),
        ('homeDirectory', home_dir),
        ('userPassword', user['password'])
    ])
    ldap_conn = ldap.initialize(ldap_ad)
    ldap_conn.simple_bind_s(cn=classroom,dc=example,dc=com)

    try:
        ldap_conn.add_s(dn, entry)
    finally:
        ldap_conn.unbind_s()





#main
admin_pass = input_ldap_pass()
try_ldap_bind(admin_pass)

user = input_data()
user['password'] = generate_password()
print("Creating LDAP entry")
create_user(user,admin_pass)
       

print("")
print(" user " + user['username'] + " (" + str(user['uid']) + ") successfuly created")
print("initial password is:" + user['password'])

