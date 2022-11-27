#!/bin/bash -xe

TOOLDIR=$(dirname `realpath ${BASH_SOURCE[0]}`)

cd $TOOLDIR/..
python3 ./tool/nginxlog2csvpv.py /var/log/nginx/access.log.1 ./data/pageviews.csv
python3 ./tool/csvpv2jsonpv.py ./data/pageviews.csv ./data/pageviews.json
git add .
git commit -m "update `date --date="yesterday" +"%Y-%m-%d"` pageviews"
git push
ln -sfv $TOOLDIR/../data/pageviews.json /var/www/blog.zhaowcheng.com/_site/pageviews.json
