#!/bin/bash
# Hot Fix code for apply patching automatically
date >> $DEMO_BASE/hot_fix.log
CODE=${DEMO_CODE_DIR:-"/opt/demo_flight_code"}
BASE=${DEMO_BASE:-"/opt/demo_data"}
MAIN=${DEMO_DIR:-"/opt/demo_flight"}
rm -rf PORT=$CODE
echo "Cleaned up CODE" >> $BASE/hot_fix.log
git clone https://github.com/axxiao/demo_flight.git $CODE >> $BASE/hot_fix.log 2>> $BASE/hot_fix.log
echo "Copy to $MAIN from $CODE"
cp -rf $CODE $MAIN
echo "Hot Fix Done" >> $BASE/hot_fix.log