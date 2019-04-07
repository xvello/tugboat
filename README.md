# tugboat: Integrate containers in your backup workflow

[![Build Status](https://travis-ci.org/xvello/tugboat-backups.svg?branch=master)](https://travis-ci.org/xvello/tugboat-backups) [![PyPI version](https://badge.fury.io/py/tugboat-backups.svg)](https://badge.fury.io/py/tugboat-backups)

When running a docker mono-node, it is non-trivial to reliably backup the datastores runing in containers:

- there is no `cron` running in the containers to create regular snapshots
- if container names are non-deterministic, running `docker exec` from a cronjob is error-prone
- backup scripts must be maintained alongside the container specs

`tugboat` resolves this by allowing you to define backup commands in your container labels. `tugboat` will execute these commands inside your containers, and capture their standard output to files in a given backup folder.

## Obligatory cute tugboat picture

[![](https://www.publicdomainpictures.net/pictures/240000/velka/tugboat-two.jpg)](https://www.publicdomainpictures.net/en/view-image.php?image=234452&picture=tugboat-two)

## Setup

Create the following labels on your containers:

- `tugboat.bkp_command`: the command to run to get a backup
- `tugboat.filename`: the file name to store the backup in (relative to the backup folder)
- `tugboat.pre_command`: (optional) command to run before bkp
- `tugboat.post_command`: (optional) command to run after bkp

Then run `tugboat` with the destination folder as an argument:

```
$ tugboat /var/backups/tugboat/
Found 3 containers to backup
  Running backup for postgres-bc5c7cd5-1543-829b-7090-92c21c55ea62... OK
  Running backup for redis-f6aec815-ea31-1f8a-a5ec-715cb5bdf48e... OK
  Running backup for consul-1cebf3d3-47f1-999a-605f-c1f079f930a3... OK
```

For safety reasons, file path will not be allowed to escape the specified folder. Use of `../` and symlinks will be detected and blocked.

## Label examples

### PostgreSQL

```
"tugboat.pre_command" = "vacuumdb --all --analyze"
"tugboat.bkp_command" = "sh -c 'pg_dumpall | gzip'"
"tugboat.filename"    = "psql.dump.gz"
```

### Consul

```
"tugboat.bkp_command" = "sh -c 'consul kv export | gzip'"
"tugboat.filename"    = "consul.dump.gz"
```

### Redis

```
"tugboat.pre_command"  = "redis-cli save"
"tugboat.bkp_command"  = "gzip -c dump.rdb"
"tugboat.post_command" = "rm --force dump.rdb"
"tugboat.filename"     = "redis-rspamd.dump.gz"
```

On a very low traffic redis server (rspamd persistence), the synchronous `save` can be used. For production databases, the asynchronous `bgsave` command should be used instead.
