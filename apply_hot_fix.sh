#!/bin/bash
# Hot Fix code for apply patching automatically
# __author__="Alex Xiao"
# __date__="2019-10-10"
# __version__="0.1"
date >> $DEMO_BASE/hot_fix.log
CODE=${DEMO_CODE_DIR:-"/opt/demo_flight_code"}
BASE=${DEMO_BASE:-"/opt/demo_data"}
MAIN=${DEMO_DIR:-"/opt/demo_flight"}
rm -rf $CODE
echo "Cleaned up $CODE" >> $BASE/hot_fix.log
git clone https://github.com/axxiao/demo_flight.git $CODE >> $BASE/hot_fix.log 2>> $BASE/hot_fix.log
echo "Copy to $MAIN from $CODE"  >> $BASE/hot_fix.log
cp -rf $CODE/* $MAIN
echo "Restarting"  >> $BASE/hot_fix.log
sudo kill $(ps -ef | grep start_monitor | awk '{print $2}')
sudo kill $(ps -ef | grep chromium-browser | awk '{print $2}')
python $MAIN/start_monitor.py &
echo "Restarted"  >> $BASE/hot_fix.log
echo "Hot Fix Done" >> $BASE/hot_fix.log
