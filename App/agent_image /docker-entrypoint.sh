#!/bin/sh
# שימי לב שהשתמשתי ב-sh במקום bash
set -e

# Start the docker daemon
dockerd &

# Wait for daemon to start
sleep 3

# Execute the command
exec "$@"