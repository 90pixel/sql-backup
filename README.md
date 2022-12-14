# SQL BACKUP

You can backup your mysql, mssql, postgresql databases and upload them to digital ocean spaces.

Supports linux and windows.
Feel free to fork and develop!

## Get Started

First create directory and get in it.

```bash
mkdir -p /home/90px-backup/ && mkdir -p /home/90px-backup/backups/ && chmod -R 777 /home/90px-backup/backups/ && cd /home/90px-backup/
```

Then install necessary python libraries for the project to work correctly.
If **pip** is not working, you can try the **pip3** command.

```bash
wget -N https://raw.githubusercontent.com/90pixel/sql-backup/main/requirements.txt
chmod +x requirements.txt
sudo -H pip install --ignore-installed PyYAML
pip install -r requirements.txt
```

Let's download and start our backup script. If **python3** not exist, you can try **python** command.

```bash
wget -N https://raw.githubusercontent.com/90pixel/sql-backup/main/backup-script.py
chmod +x backup-script.py
python3 backup-script.py
```

## Screenshots

For the first run, if the config file is not found, you must enter the digital ocean spaces information
![Config Settings](https://raw.githubusercontent.com/90pixel/sql-backup/main/imgs/1.jpg)

You can choose option 1 to enter new sql information to be backed up
![Option Settings](https://raw.githubusercontent.com/90pixel/sql-backup/main/imgs/2.jpg)

![Option Settings](https://raw.githubusercontent.com/90pixel/sql-backup/main/imgs/3.jpg)

If the database informations is correct the config will be added successfully

![Add Database Config](https://raw.githubusercontent.com/90pixel/sql-backup/main/imgs/4.jpg)

## Auto Backup

If you want use sqlcmd and not linked to /usr/local/bin/sqlcmd, you can use this command to create a symbolic link.

```bash
sudo ln -s /opt/mssql-tools/bin/sqlcmd /usr/local/bin/sqlcmd
```

You can start via -backup arguments. To auto backup and add to cronjob. You should add path for cronjob.

```bash
cd /home/90px-backup/ && python3 backup-script.py -backup
```

Crontab ready to use. Every day at 3:05 AM (If the server time is in utc, it will be 06:05 in Turkey time)

```bash
# Backup db and upload
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
5 3 * * * cd /home/90px-backup/ && python3 backup-script.py -backup >> backup.log 2>&1
```

## TODO LIST

### Todo

- [ ] Extra backup options can be added (google drive, local, ftp)
- [ ] The cronjob task can be set from within the script for ubuntu(linux)
- [ ] Can be automatically added to the task scheduler for windows
- [ ] Log system can be improved
- [ ] In case of error, you can send an e-mail or a notification can be sent from discord.
- [ ] Add port option other than default port
- [ ] Ssh tunnel connection to database

### In Progress

- [ ] None

### Done ✓

- [x] Delete old backups older than 3 months
- [x] Create init commit  