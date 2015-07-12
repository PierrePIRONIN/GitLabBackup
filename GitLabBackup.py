import argparse
import sys
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import requests

# Start timestamp
print("Backup starts at : " + str(datetime.now()))

# Extract url from arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the GitLab server's url")
parser.add_argument("token", help="the private token of your GitLab profile")
parser.add_argument("--ssh_port", help="the ssh port of GitLab projects clone operation (default 22)")
parser.add_argument("--backup_dir", help="the directory where repositories will be backup (default ./repos_backup")
parser.add_argument("--config_email", help="the configuration file (.json) for email notification (default ./config_email.json)")
args = parser.parse_args()

# Request GitLab API to retrieve projects
gitlab_url = args.url + "/api/v3/projects?private_token=" + args.token
r = requests.get(gitlab_url, verify=False)
if r.status_code != 200:
    r.raise_for_status()

# Make the backup repositories directory
backup_directory = "./repos_backup"
if args.backup_dir:
    backup_directory = args.backup_dir
try:
    os.mkdir(backup_directory)
except OSError as e:
    if e.errno == 17:
        print("Backup directory already exists. Skip creation...")
    else:
        raise

# Iterate on projects and clone them in mirror mode or update them if already exist
projects = r.json()
for project in projects:
    url = project["ssh_url_to_repo"]
    if args.ssh_port:
        url = "ssh://" + url.replace(":", ":" + args.ssh_port + "/")
    localPath = backup_directory + "/" + project["path"] + ".git"
    if not os.path.exists(localPath):
        print("Create backup for " + localPath)
        os.system("git clone --mirror " + url + " " + localPath)
    else:
        print("Update backup for " + localPath)
        os.system("cd " + localPath + "; git remote update")

# Send mail if enabled
configEmailFilename = args.config_email
if not configEmailFilename:
    configEmailFilename = "./config_email.json"
if not os.path.exists(configEmailFilename):
    print("No configuration file found for email notification. Skip...")
else:
    config = None
    with open(configEmailFilename) as configEmail:
        config = json.loads(configEmail.read())

    # Mandatory fields
    if config is None:
        print("An error occured when reading email notifications configuration file. Skip email notification...")
        sys.exit(-1)
    if "from" not in config:
        print("Field 'from' not found in email notifications configuration file. Skip email notification...")
        sys.exit(-1)
    if "to" not in config:
        print("Field 'to' not found in email notifications configuration file. Skip email notification...")
        sys.exit(-1)
    if "smtp_url" not in config:
        print("Field 'smtp_url' not found in email notifications configuration file. Skip email notification...")
        sys.exit(-1)
    if "smtp_login" not in config:
        print("Field 'smtp_login' not found in email notifications configuration file. Skip email notification...")
        sys.exit(-1)
    if "smtp_password" not in config:
        print("Field 'smtp_password' not found in email notifications configuration file. Skip email notification...")
        sys.exit(-1)

    # Optional fields
    subject = "Backup GitLab"
    if "subject" not in config:
        print(
            "Field 'subject' not found in email notifications configuration file. Default will be used ('" + subject + "')")
    else:
        subject = config["subject"]
    message = "Your GitLab projects were backup sucessfully."
    if "message" not in config:
        print(
            "Field 'message' not found in email notifications configuration file. Default will be used ('" + message + "')")
    else:
        subject = config["subject"]
    enable_ssl = True
    if "enable_ssl" not in config:
        print("Field 'enable_ssl' not found in email notifications configuration file. Default will be used (" + str(
            enable_ssl) + ")")
    else:
        if type(config["enable_ssl"]) != bool:
            print("Field 'enable_ssl' isn't a boolean. Default will be used (" + str(enable_ssl) + ")")
        else:
            enable_ssl = config["enable_ssl"]
    port = 465
    if not enable_ssl:
        port = 587
    if "port" not in config:
        print(
            "Field 'port' not found in email notifications configuration file. Default will be used (" + str(
                port) + ")")
    else:
        if type(config["port"]) != int:
            print("Field 'port' isn't an integer. Default will be used (" + str(port) + ")")
        else:
            port = config["port"]

    # Send mail
    msg = MIMEMultipart()
    msg["From"] = config["from"]
    msg["To"] = config["to"]
    msg["Subject"] = subject
    msg.attach(MIMEText(message))
    mailserver = None
    if enable_ssl:
        mailserver = smtplib.SMTP_SSL(config["smtp_url"], port)
    else:
        mailserver = smtplib.SMTP(config["smtp_url"], port)
    mailserver.ehlo()
    mailserver.login(config["smtp_login"], config["smtp_password"])
    mailserver.sendmail(config["from"], config["to"], msg.as_string())
    mailserver.quit()
    print("Mail sent succesfully")

# End timestamp
print("Backup ends at : " + str(datetime.now()))
