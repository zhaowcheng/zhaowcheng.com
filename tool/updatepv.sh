#!/bin/bash -xe

TOOLDIR=$(dirname `realpath ${BASH_SOURCE[0]}`)
NGINXLOGDIR=/var/log/nginx
ARCHLOGNAME=access.log.`date +"%Y%m%d"`

cd $NGINXLOGDIR
mv access.log $ARCHLOGNAME
kill -USR1 `cat /var/run/nginx.pid`
sleep 1
python3 $TOOLDIR/nginxlog2csvpv.py $NGINXLOGDIR/$ARCHLOGNAME $TOOLDIR/../data/pageviews.csv
gzip -f $ARCHLOGNAME

cd $TOOLDIR/..
python3 ./tool/csvpv2jsonpv.py ./data/pageviews.csv ./data/pageviews.json
git config user.name zhaowcheng
git config user.email zhaowcheng@163.com
git add .
git commit -m "update `date +"%Y-%m-%d"` pageviews"
git push --set-upstream origin master
ln -sfv $TOOLDIR/../data/pageviews.json /var/www/blog.zhaowcheng.com/_site/pageviews.json
