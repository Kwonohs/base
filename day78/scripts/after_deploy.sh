REPOSITORY=/home/ubuntu/base/day78

cd $REPOSITORY/do_it_django

echo "> Stop & Remove docker servies."
sudo docker-compose down

echo "> Run new docker servies."
sudo docker-composer up -d --build >> /var/log/deploy.log 2>&1