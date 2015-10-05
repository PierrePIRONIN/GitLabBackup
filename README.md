# GitLab Community Edition Backup

> A highly customizable python script to backup your GitLab Community Edition server.

## Requirements
GitLabBackup requires Python 2.7 or higher and is only tested on Linux-like systems ;)

## How it works
GitLabBackup uses the [GitLab API](http://doc.gitlab.com/ee/api/projects.html) to retrieve your projects on your GitLab Community Edition server and make a backup of them with Git !

## How to use it
Clone the repo using Git:
``` bash
git clone https://github.com/PierrePIRONIN/GitLabBackup
```
Then just launch GitLabBackup.py with, at least, the mandatory arguments:
``` bash
python GitLabBackup.py <MY_GITLAB_SERVER_URL> <MY_GITLAB_PRIVATE_TOKEN>
```
### Arguments
| Argument                | Position | Optional | Default             | Description |
| ----------------------- | :------: | :------: | :-----------------: | ----------- |
| MY_GITLAB_SERVER_URL    | 1        | No       |                     | Your GitLab-CE server url |
| MY_GITLAB_PRIVATE_TOKEN | 2        | No       |                     | Your GitLab-CE [private token](https://www.safaribooksonline.com/library/view/gitlab-cookbook/9781783986842/ch06s05.html) |
| --ssh_port              | 3+       | Yes      | 22                  | The ssh port used to clone your GitLab projects |
| --backup_dir            | 3+       | Yes      | <CURRENT_DIR>/repos_backup      | The parent directory where your GitLab projects will be cloned |
| --config_email          | 3+       | Yes      | <CURRENT_DIR>/config_email.json | The JSON file containing configuration of email notifications |

Here is an example with all the arguments and a redirection of log:
> python GitLabBackup.py <MY_GITLAB_SERVER_URL> <MY_GITLAB_PRIVATE_TOKEN> --ssh_port 2222 --backup_dir /data/gitlab/backups --config_email /data/gitlab/config/email_notifications.json > ./log 2>&1

## Email notifications
GitLabBackup could be configured to send an email after the backup processed sucessfully. 

This feature is enabled if the option --config_email is set correctly (or if a file named config_email.json is present aside GitLabBackup.py i.e. the default value for --config_email option).

### Structure
The config_email.json must respect the following schema:
``` json
{
  "from": "backup@my.domain.com",
  "to": "me@gmail.com",
  "smtp_url": "my_provider_smtp_url",
  "smtp_login": "backup@my.domain.com",
  "smtp_password": "MY_SECRET_SMTP_PASSWORD"
}
```
In addition of this mandatory fields, you could customize the following ones (the given values are the default ones):
``` javascript
{
  ...
  "subject": "Backup GitLab", # email subject
  "message": "Your GitLab projects were backup sucessfully.", # email body
  "enable_ssl": True, # send email through ssl or not
  "port": 465, # or 587 if enable_ssl is false or everyone you want
}
```

## Scheduling
Here is a simple scheduling crontab's entry. The backup will be triggered every Sunday at 2:00 AM.
``` crontab
0 2 * * 0 cd MY_BACKUP_DIR; python GitLabBackup.py <MY_GITLAB_SERVER_URL> <MY_GITLAB_PRIVATE_TOKEN> > ./log 2>&1
```

Enjoy ! ;)

## License
© Pierre PIRONIN, 2015. Licensed under an [MIT](https://github.com/PierrePIRONIN/GitLabBackup/blob/master/LICENSE.md) license.
