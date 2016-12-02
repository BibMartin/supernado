
source activate supervisor


rm -rf services/test
cp -R template_service services/test

sed -i 's/port: 8001/port: 8000/g' ./services/test/_config.yml
sed -i 's/template/test/g' ./services/test/_supervisord.conf

supervisord
supervisorctl start all
supervisorctl restart all

curl http://localhost:8001/foo/bar
curl http://localhost:8000/foo/bar

supervisorctl shutdown

find . -type f -name "*.py" ! -name 'conf.py' | xargs flake8 --max-line-length=100
