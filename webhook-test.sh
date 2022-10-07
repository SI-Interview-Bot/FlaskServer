#!/bin/sh
if [ "$1" = "-k" ]; then
    shift
    curl --http1.1 "http://${1:-localhost}:${2:-8088}/end"
else
    curl --http1.1 -d @webhook-test.json "http://${1:-localhost}:${2:-8088}/issue-update?user_id=some.employee%40coolCompany.com&user_key=some.employee%40coolCompany.com"
fi
