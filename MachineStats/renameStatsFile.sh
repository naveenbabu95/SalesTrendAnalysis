cd AnalyticsService
./input_instances.sh
cd ..
cd DatabaseService
./input_instances.sh
cd ..
cd InputService
./input_instances.sh
cd ..

rm -rf AnalyticsService/logs/gunicorn-access.csv
mv AnalyticsService/logs/gunicorn-access.log AnalyticsService/logs/gunicorn-access.csv

rm -rf DatabaseService/logs/gunicorn-access.csv
mv DatabaseService/logs/gunicorn-access.log DatabaseService/logs/gunicorn-access.csv

rm -rf InputService/logs/gunicorn-access.csv
mv InputService/logs/gunicorn-access.log InputService/logs/gunicorn-access.csv

python3 machineStats.py
