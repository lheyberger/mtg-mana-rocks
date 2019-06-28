#!/bin/sh

VIRTUAL_ENV=.env

FILENAME=$(basename "$0")
SHORTNAME="${FILENAME%.*}"
SCRIPT="${SHORTNAME}.py"

cd "$( dirname "${BASH_SOURCE[0]}" )"

# install virtual env if needed
if [ ! -d ${VIRTUAL_ENV} ] ; then
  virtualenv ${VIRTUAL_ENV} 2>&1 >/dev/null
fi

# install requirements if needed
if [ -f requirements.txt ] ; then
  ${VIRTUAL_ENV}/bin/pip install -q -r requirements.txt 2>&1 >/dev/null
fi

# invoke script, forwarding args if needed
if [ $# -eq 0 ] ; then
  ${VIRTUAL_ENV}/bin/python $SCRIPT
else
  ${VIRTUAL_ENV}/bin/python $SCRIPT "$@"
fi
