#!/bin/sh
set -e

dockerd &

sleep 3

exec "$@"