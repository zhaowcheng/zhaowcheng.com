#!/bin/bash -xe

TOOLDIR=$(dirname `realpath ${BASH_SOURCE[0]}`)

cd $TOOLDIR/..
python3 ./tool/nginxlog2csvpv.py /var/log/nginx/access.log ./data/pageviews.csv
python3 ./tool/csvpv2jsonpv.py ./data/pageviews.csv ./data/pageviews.json
git config user.name zhaowcheng
git config user.email zhaowcheng@163.com
git add .
git commit -m "update `date --date="yesterday" +"%Y-%m-%d"` pageviews"
git push --set-upstream origin master
ln -sfv $TOOLDIR/../data/pageviews.json /var/www/blog.zhaowcheng.com/_site/pageviews.json
