In this directory you will add a .env settings file:

    .env

The contents should be structured like:

    VOL=<local path to the root of this repo -- will be mapped to /app in the docker web img>
    VOL_DB=<local path to the mysql files, e.g.: "local proj path/docker_mysql/8.0">
    VOL_DB_CONFIG=<local path to the db config file, e.g.: "local proj path/db_configuration">
    DB_PWD=<root db pwd>
    REL_DB_CONFIG=/opt/project/db_configuration
    STATIC_VOL=<path YSE_PZ app's static directory>
    DB_INIT=<path to "DatabaseInitialization" directory>


TO UPDATE PACKAGES AND/OR GENERATE A NEW WEB DOCKER IMAGE:
Add you requirements file to build a new web image at ./Requirements/. Naming conventions should be:

    ./Requirements/requirements_1.txt
    ./Requirements/requirements_2.txt
...

However, you should only need 1 file unless you have conflicting dependencies.


LOCAL DOCKER (recommended — prunes old images after each successful run):
From the repo root:

    ./docker/scripts/yse-docker.sh up       # start stack, light prune
    ./docker/scripts/yse-docker.sh pull     # pull latest web image, remove superseded layers
    ./docker/scripts/yse-docker.sh rebuild  # build local dev image from Dockerfile.web.dev
    ./docker/scripts/yse-docker.sh prune    # prune only

Or from docker/:

    ./scripts/yse-docker.sh up

Set YSE_DOCKER_PRUNE=0 to skip pruning for one command.

Pruning removes dangling layers, build cache, and old ghcr.io/davecoulter/yse_pz /
local/yse_pz_web images that are not used by ysepz_* containers. It does NOT delete
MySQL data (VOL_DB). To wipe the database intentionally:

    docker compose down -v

DISK SPACE (macOS Docker Desktop):
Each pull/build can leave 10–20 GB of old image layers in Docker.raw. The scripts
above reclaim most of that automatically. If the disk image still does not shrink,
use Docker Desktop → Troubleshoot → Clean / Purge data, or:

    docker system df
    ./docker/scripts/yse-docker.sh prune aggressive

Keep several GB free on the host disk; git push and Docker both fail when the
volume is full.