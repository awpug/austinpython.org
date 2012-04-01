#!/bin/sh

PINAX=`python -c "import pinax_theme_bootstrap as px;import os.path as p;print(p.dirname(px.__file__));"`
ATXPY_LESS="static/less/base.less"
COMMAND="lessc -x --include-path=$PINAX $ATXPY_LESS static/css/master.css"
${COMMAND}
