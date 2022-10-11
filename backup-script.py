import json
import os
import sys
import time

from spaces import Client

# CONSTANTS
backup_dir = "/home/90px-backup/backups/"
# IF OS IS WINDOWS BACKUP DIR IS DIFFERENT
if os.name == 'nt':
    backup_dir = "C:\\90px-backup\\"
config_file = "config.json"
do_config_file = "do_config.json"

# DigitalOcean Spaces Config
do_region_name = ""
do_spaces_name = ""
do_spaces_access_key = ""
do_spaces_secret_key = ""


# CHECK do_spaces Config FILE
def check_do_config_file():
    global do_region_name
    global do_spaces_name
    global do_spaces_access_key
    global do_spaces_secret_key

    if not os.path.isfile(do_config_file):
        do_region_name = input("Enter DigitalOcean region name: ")
        do_spaces_name = input("Enter DigitalOcean Spaces name: ")
        do_spaces_access_key = input("Enter DigitalOcean Spaces access key: ")
        do_spaces_secret_key = input("Enter DigitalOcean Spaces secret key: ")

        # Create config file
        with open(do_config_file, 'w') as outfile:
            json.dump({
                "do_region_name": do_region_name,
                "do_spaces_name": do_spaces_name,
                "do_spaces_access_key": do_spaces_access_key,
                "do_spaces_secret_key": do_spaces_secret_key
            }, outfile)
    else:
        read_do_config_file()


# read digitalocean config file and set variables
def read_do_config_file():
    global do_region_name
    global do_spaces_name
    global do_spaces_access_key
    global do_spaces_secret_key

    with open(do_config_file) as json_file:
        data = json.load(json_file)
        do_region_name = data['do_region_name']
        do_spaces_name = data['do_spaces_name']
        do_spaces_access_key = data['do_spaces_access_key']
        do_spaces_secret_key = data['do_spaces_secret_key']


# UPLOAD TO DIGITALOCEAN SPACES
def upload_to_digitalocean_spaces():
    try:
        client = Client(do_region_name, do_spaces_name, do_spaces_access_key, do_spaces_secret_key)
        print("Uploading to DigitalOcean Spaces...")
        for file in os.listdir(backup_dir):
            if file.endswith(".gz"):
                print("Uploading " + file)
                # split by dot and get first value
                file_name = file.split(".")[0]
                client.upload_file(backup_dir + file, 'backups/', rename=file_name)
                print("Uploaded " + file)
                # remove file
                os.remove(backup_dir + file)
    except Exception as e:
        print("Error uploading to DigitalOcean Spaces")
        print(e)


# BACKUP MYSQL

def backup_mysql(_host="", _user="", _password="", _database=""):
    try:
        # Create backup directory
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Create backup file
        backup_file = backup_dir + _database + time.strftime("%Y%m%d-%H%M%S") + ".sql"

        # if _host is not set
        if _host == "":
            _host = "localhost"

        # Dump database into SQL file
        dumpcmd = "mysqldump -h" + _host + " -u " + _user + " -p" + _password + " " + _database + " > " + backup_file
        # If password is not set
        if _password == "":
            dumpcmd = "mysqldump -h" + _host + "  -u " + _user + " " + _database + " > " + backup_file
        os.system(dumpcmd)

        # Compress SQL file
        compresscmd = "gzip " + backup_file
        os.system(compresscmd)

    except Exception as e:
        print(e)


# BACKUP MSSQL

def backup_mssql(_host="", _user="", _password="", _database=""):
    try:
        # Create backup directory
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Create backup file
        backup_file = backup_dir + _database + time.strftime("%Y%m%d-%H%M%S") + ".bak"

        print("Backing up " + backup_file + " database...")
        # if _host is not set
        if _host == "":
            _host = "localhost"

        # Dump database into SQL file
        dumpcmd = "sqlcmd -S " + _host + " -U " + _user + " -P " + _password + " -Q \"BACKUP DATABASE " + _database + " TO DISK = '" + backup_file + "'\""

        if _user == "":
            dumpcmd = "sqlcmd -S " + _host + " -Q \"BACKUP DATABASE " + _database + " TO DISK = '" + backup_file + "'\""
        os.system(dumpcmd)

        print("Backup done")
        # Compress SQL file
        compresscmd = "gzip " + backup_file
        os.system(compresscmd)

        print("Compress done")

    except Exception as e:
        print(e)


# BACKUP POSTGRESQL

def backup_postgresql(_host="", _user="", _password="", _database=""):
    try:
        # Create backup directory
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Create backup file
        backup_file = backup_dir + _database + time.strftime("%Y%m%d-%H%M%S") + ".sql"

        # if _host is not set
        if _host == "":
            _host = "localhost"

        # Dump database into SQL file
        dumpcmd = "pg_dump --host=" + _host + " --username=" + _user + " --port=5432 " + _database + " > " + backup_file
        os.system(dumpcmd)

        # Compress SQL file
        compresscmd = "gzip " + backup_file
        os.system(compresscmd)

    except Exception as e:
        print(e)


# TEST MYSQL CONNECTION
def test_mysql_connection(_host="", _user="", _password="", _database=""):
    # Check dependencies
    check_dependencies_mysql()

    # if _host is not set
    if _host == "":
        _host = "localhost"

    # Test connection
    testcmd = "mysql -h" + _host + " -u " + _user + " -p" + _password + " -e \"use " + _database + "\""
    # If password is not set
    if _password == "":
        testcmd = "mysql -h" + _host + "  -u " + _user + " -e \"use " + _database + "\""
    if os.system(testcmd) != 0:
        print("Test connection failed")
        exit()
    print("Test connection success")


# TEST MSSQL CONNECTION
def test_mssql_connection(_host="", _user="", _password="", _database=""):
    # Check dependencies
    check_dependencies_mssql()

    # if _host is not set
    if _host == "":
        _host = "localhost"

    # Test connection
    testcmd = "sqlcmd -S " + _host + " -U " + _user + " -P " + _password + " -Q \"use " + _database + "\""
    if _user == "":
        testcmd = "sqlcmd -S " + _host + " -Q \"use " + _database + "\""
    if os.system(testcmd) != 0:
        print("Test connection failed")
        exit()
    print("Test connection success")


# TEST POSTGRESQL CONNECTION
def test_postgresql_connection(_host="", _user="", _password="", _database=""):
    # Check dependencies
    check_dependencies_postgresql()

    # if _host is not set
    if _host == "":
        _host = "localhost"

    # Test connection
    testcmd = "psql -h " + _host + " -U " + _user + " -p 5432 -d " + _database + " -c \"select 1\""
    if os.system(testcmd) != 0:
        print("Test connection failed")
        exit()
    print("Test connection success")


# REMOVE OLD FILES
def remove_old_files():
    # If OS is Windows delete last 3 days
    if os.name == 'nt':
        os.system("forfiles /P " + backup_dir + " /M *.* /D -3 /C \"cmd /c del @path\"")
        # remove sql files
        os.system("forfiles /P " + backup_dir + " /M *.sql /C \"cmd /c del @path\"")
    else:
        os.system("find " + backup_dir + " -type f -mtime +3 -exec rm {} \;")
        # remove sql files
        os.system("find " + backup_dir + " -type f -name '*.sql' -exec rm {} \;")


# CHECK DEPENDENCIES postgreSQL
def check_dependencies_postgresql():
    # Check if pg_dump is installed
    if os.system("which pg_dump") != 0:
        print("pg_dump is not installed")
        exit()

    # Check if psql is installed
    if os.system("which psql") != 0:
        print("psql is not installed")
        exit()

    # Check if gzip is installed
    if os.system("which gzip") != 0:
        print("gzip is not installed")
        exit()


# CHECK DEPENDENCIES
def check_dependencies_mysql():
    # Check if mysqldump is installed
    if os.system("which mysqldump") != 0:
        print("mysqldump is not installed")
        exit()

    # Check if gzip is installed
    if os.system("which gzip") != 0:
        print("gzip is not installed")
        exit()


# CHECK DEPENDENCIES
def check_dependencies_mssql():
    # Check if gzip is installed
    if os.system("which gzip") != 0:
        print("gzip is not installed")
        exit()

    # Check if sqlcmd is installed
    if os.system("which sqlcmd") != 0:
        print("sqlcmd is not installed")
        exit()


# ADD BACKUP ARGUMENTS TO CONFIG FILE AS JSON
def add_backup_arguments_to_config_file(_host, _user, _password, _database, _type):
    # if host is not set
    if _host == "":
        _host = "localhost"

    # if type is mysql
    if _type == "mysql":
        # test mysql connection
        test_mysql_connection(_host, _user, _password, _database)
    # if type is mssql
    elif _type == "mssql":
        # test mssql connection
        test_mssql_connection(_host, _user, _password, _database)
    elif _type == "postgresql":
        # test postgresql connection
        test_postgresql_connection(_host, _user, _password, _database)
    else:
        print("Type is not valid")
        exit()

    # Check if config file exists
    if not os.path.exists(config_file):
        # Add backup arguments to config file as list
        with open(config_file, 'w') as outfile:
            json.dump([{"host": _host, "user": _user, "password": _password, "database": _database, "type": _type}],
                      outfile, indent=4)
    else:
        # Read config file
        with open(config_file) as json_file:
            data = json.load(json_file)

            # Add backup arguments to config file as list
            data.append({"host": _host, "user": _user, "password": _password, "database": _database, "type": _type})
            # if duplicate found remove it
            data = [i for n, i in enumerate(data) if i not in data[n + 1:]]
            # Write config file
            with open(config_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
    print("Backup arguments added to config file")


# READ ALL BACKUP ARGUMENTS FROM CONFIG FILE
def take_all_backups():
    try:
        # Check if config file exists
        if not os.path.exists(config_file):
            print("Config file not found")
            exit()
        else:
            # Read config file
            with open(config_file) as json_file:
                data = json.load(json_file)
                # Loop through all backup arguments
                for p in data:
                    # If type is mysql
                    if p['type'] == "mysql":
                        # Backup mysql
                        print(p['database'] + " backup started")
                        backup_mysql(p['host'], p['user'], p['password'], p['database'])
                        print(p['database'] + " backup finished")
                    # If type is mssql
                    elif p['type'] == "mssql":
                        # Backup mssql
                        print(p['database'] + " backup started")
                        backup_mssql(p['host'], p['user'], p['password'], p['database'])
                        print(p['database'] + " backup finished")
                    elif p['type'] == "postgresql":
                        # Backup postgresql
                        print(p['database'] + " backup started")
                        backup_postgresql(p['host'], p['user'], p['password'], p['database'])
                        print(p['database'] + " backup finished")
                    else:
                        print("Unknown type: " + p['type'])
                        continue
        print("All backups completed")
        # remove old not compressed files
        remove_old_files()
        print("Start to upload backups")
        upload_to_digitalocean_spaces()
    except Exception as e:
        print(e)
        print("Error: Something went wrong")
        exit()


# Print all configs with order number in config file
def print_all_configs():
    # Check if config file exists
    if not os.path.exists(config_file):
        print("Config file not found")
        exit()
    else:
        # Read config file
        with open(config_file) as json_file:
            data = json.load(json_file)
            # is empty print error
            if len(data) == 0:
                print("Config file is empty")
                exit()
            # Loop through all backup arguments
            for p in data:
                print(str(data.index(p) + 1) + ". " + p['host'] + " " + p['user'] + " " + p['password'] + " " + p[
                    'database'] + " " + p['type'])


# remove from config file with order number
def remove_from_config_file(_order_number):
    # Check if config file exists
    if not os.path.exists(config_file):
        print("Config file not found")
        exit()
    else:
        # Read config file
        with open(config_file) as json_file:
            data = json.load(json_file)
            # Loop through all backup arguments
            for p in data:
                if str(data.index(p) + 1) == _order_number:
                    data.remove(p)
                    # Write config file
                    with open(config_file, 'w') as outfile:
                        json.dump(data, outfile, indent=4)
                    print("Removed from config file")
                    break


# select menu
def select_menu():
    print("Select an option:")
    print("1. Add Sql Backup Task")
    print("2. Remove Sql Backup Task")
    print("3. Start Backup Now")
    print("4. List All Backup Tasks")
    print("5. Exit")
    option = input("Option: ")
    if option == "1":
        # get host, user, password, database, type
        _host = input("Host: (default: localhost) ")
        _user = input("User: ")
        _password = input("Password: ")
        _database = input("Database: ")
        _type = input("Type (mysql/mssql/postgresql): ")
        # add backup arguments to config file
        add_backup_arguments_to_config_file(_host, _user, _password, _database, _type)
        select_menu()
    elif option == "2":
        print_all_configs()
        order_number = input("Remove by line number: ")
        remove_from_config_file(order_number)
        select_menu()
    elif option == "3":
        take_all_backups()
        select_menu()
    elif option == "4":
        print_all_configs()
    elif option == "5":
        exit()


# STARTUP
if len(sys.argv) > 1 and sys.argv[1] == "-backup":
    check_do_config_file()
    take_all_backups()
else:
    check_do_config_file()
    select_menu()
