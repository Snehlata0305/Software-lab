#!/bin/sh
path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$path"

cd "$1"

ls -l | grep -c ^d
