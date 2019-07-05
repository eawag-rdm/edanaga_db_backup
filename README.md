# edanaga DB backup

Script to backup periodically the edanaga - SwitchElicit database.


Can be run as a Docker container (execute via `cron`)

In the top-level directory:

1. `make install` (Installs the necessary dependencies in a virtualenv
called "v3" (not necessary when using Docker)
2. `make build_image` (Build a Docker image)
3. `make test` (Runs unit-tests)
4. `make help` (Shows command to run the container)


