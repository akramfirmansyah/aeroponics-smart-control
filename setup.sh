mkdir -p mosquitto/data
mkdir -p mosquitto/log

mkdir -p influxdb/data
mkdir -p influxdb/config

cd node-red && npm install && cd ..

docker compose --project-name sgh up -d