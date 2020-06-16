#!/bin/sh

flask db upgrade heads

exec "$@"