Developed a platform as a Service(PaaS) application, enabling pipelined execution in the sales trend analysis domain. The platform offered
services like a storage service, analytical service and graphical visualization service.
The application reviewed historical revenue results to obtain patterns and predict the demand for an unreleased commodity. The user was
also provided with a dashboard to select the services he desired and rearrange them according to his need.
The system was distributed on 4 physical machines forming a cluster and each machine running a set of micro services deployed on
containers in docker. The requests to the server was distributed using rabbitmq message broker

The services are hosted on 

	"inputservice_url" : "http://0.0.0.0:8000",
	"database_url" : "http://172.20.128.6:8004",
	"analytics_url" : "http://172.20.128.2:8002",
	"output_url" : "http://172.20.128.5:8003"

This can be changed by the end user based on his/her requirements and can be be found in the container_port.json file.