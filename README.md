# GitLab Community Edition Backup

> A high customizable utility script to backup a GitLab Community Edition server.

## How it works

## How to use it


## Scheduling
Here is a simple scheduling crontab's entry. The backup will be triggered every Sunday at 2:00 AM.
```
2 0 * * 0 cd MY_BACKUP_DIR; python GitLabBackup.py https://<MY_IP_SERVER> <MY_GITLAB_PRIVATE_TOKEN> --ssh_port <CLONE_SSH_PORT> > ./log 2>&1
```

## License

© Pierre PIRONIN, 2015. Licensed under an [MIT](https://github.com/PierrePIRONIN/GitLabBackup/blob/master/LICENSE.md) license.
