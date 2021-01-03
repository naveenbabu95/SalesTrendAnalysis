docker stop postgres
docker stop dbscript


docker rm postgres
docker rm dbscript

docker rmi $(docker images postgres)
docker rmi $(docker images temp_databasescript)