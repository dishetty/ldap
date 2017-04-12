import grp
import pwd
import os
import ldap
import subprocess
import getpass

DEFAULT_SHELL = "/bin/bash"
ldap_ad = "ldap://localhost"

# LDAP admin password
def input_ldap_pass():
     return getpass.getpass("Enter LDAP manager password: ")    #Enter the admin password set at the time of configuration


def input_data():                                                  
    user = {}
    # name
    user['firstname'] = raw_input("Firstname: ")
    user['lastname'] = raw_input("Lastname: ")

    # user's name
    user['username'] = raw_input("Username: ")
   
   
   # UID
    uid = raw_input("UID : ")
    uid = int(uid)
    user['uid'] = uid

    # group's name
    user['group'] = raw_input("Group name: ")
    if (user['group'] == ""):
        user['group'] = "openldap"

    # login shell
    shell = raw_input("Login shell [default is /bin/bash]: ")
    if (shell == ""): 
        user['shell'] = DEFAULT_SHELL
    else:
        user['shell'] = shell
    #password      
    user['password'] = raw_input("Password: ")

    return user

# this is going to try to bind to LDAP with admin DN and give password and exit
def try_ldap_bind(admin_pass):
    
    try:
        ldap_conn = ldap.initialize(ldap_ad)
    except Exception as e:
        print e
        print("Can't contact LDAP server")
        exit()

    try:
        ldap_conn.set_option(ldap.OPT_REFERRALS, 0)
        ldap_conn.simple_bind_s("cn=admin,dc=rhel,dc=com", admin_pass)	#User is 'admin', Domain name was set as "rhel.com"
    except Exception as e:
        print("This password is incorrect!")
        exit()

    print("Authorization successful")
    print("")


# to create new entry in LDAP for given user
def create_user(user, admin_pass):

    dn = "cn=" + user['username'] + "," + "dc=rhel,dc=com"
    fullname = user['firstname'] + "_" + user['lastname']
    entry = []
    entry.extend([
        ('objectClass', ["person", "organizationalPerson", "inetOrgPerson", "posixAccount"]),
        ('cn', fullname),
        ('givenname', user['firstname']),
        ('sn', user['lastname']),
        ('uid', str(user['uid'])),
        ('loginShell', user['shell'])
        ('userPassword', user['password'])

    ])

    ldap_conn = ldap.initialize(ldap_ad)
    ldap_conn.simple_bind_s("cn=admin,dc=rhel,dc=com",admin_pass)

    try:
        ldap_conn.add_s(dn, entry)
    finally:
        ldap_conn.unbind_s()

#main
admin_pass = input_ldap_pass()

try_ldap_bind(admin_pass)

user = input_data()
print("Creating LDAP entry")
create_user(user,admin_pass)
       

print("")
print(" user " + user['username'] + " (" + str(user['uid']) + ") successfully created")
