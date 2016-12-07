mkdir services/$1
cp template_service/* services/$1/

sed -i 's/port: 8001/port: $2/g' ./services/$1/_config.yml
sed -i 's/template/$1/g' ./services/$1/_supervisord.conf
