### Useful Commands

**How to Build Image, Run Container, and Remove All After the Job** :whale:

- `docker-compose up`: Starts containers as defined in `docker-compose.yml`. Useful for running the application in a local development environment.

- `docker-compose up --build`: Rebuilds the image and starts the containers. Use this when you've made changes to the Dockerfile or other components of the image.

- `docker build -t [NAME:TAG] . --no-cache`: Builds the Docker image with the tag, ignoring any cached layers. This ensures a fresh build.

- `docker run -p 80:8000 [ID OR NAME]`: Runs the container, mapping port 80 of the host to port 8000 of the container.

- `docker ps`: Lists running containers.

- `docker logs [ID OR NAME]`: Fetches logs of a specific container. Useful for debugging.

- `docker run -it --entrypoint /bin/sh [ID OR NAME]`: Runs the container in interactive mode with a shell entrypoint. Good for exploring inside the container.

- `docker stop [ID OR NAME]`: Stops a running container.

- `docker rm [ID OR NAME]`: Removes a stopped container.

- `docker images`: Lists all Docker images.

- `docker rmi [ID OR NAME]`: Removes the specified image.

- `docker rmi -f $(docker images -q)`: Force removes all images.

- `sudo docker stop $(sudo docker ps -aq)`: Stops all running containers.

- `sudo docker rm $(sudo docker ps -aq)`: Removes all containers.

- `sudo docker system prune -a`: Removes all stopped containers, networks, images (both dangling and unreferenced), and optionally, volumes.

**Potential local Postgres client issues:** :elephant:

- `netstat -an | grep 5432`: Checks if the PostgreSQL port is already in use.

- `brew services stop postgresql`: Stops the PostgreSQL service if it's running locally, freeing up the port.

- Or stop the process via Activity Monitor.

**After Executing the Terraform Script** :mag:

- `sudo aws s3 ls s3://ozieblomichal-fastapi-template-bucket`: Lists objects in the specified S3 bucket.

- `sudo docker logs container_name`: Fetches logs from a specific container.

- `sudo docker exec -it container_name bin/sh`: Executes an interactive shell inside the container.

- `LATEST_LOG=$(sudo aws s3 ls s3://ozieblomichal-fastapi-template-bucket/logs/ --recursive | sort | tail -n 1 | awk '{print substr($0, index($0, $4))}')`: Fetches the latest log file name from the S3 bucket.

- `echo $LATEST_LOG`: Displays the latest log file name.

- `sudo aws s3 cp "s3://ozieblomichal-fastapi-template-bucket/${LATEST_LOG}" - | cat`: Copies the latest log file from S3 and displays its content.

- `/var/log/syslog`, `/var/log/awslogs.log`: View system logs and AWS logs, respectively.

- `sudo find / -type f -name "awslogs-agent-setup.py"`: Finds the location of the AWS logs agent setup script.

- `sudo systemctl status awslogsd`: Checks the status of the AWS logs daemon.

- `crontab -l`: Lists all cron jobs.

- `cat /var/log/cloud-init-output.log`: Views the output log of cloud initialization.

- `grep "crontab" /var/log/cloud-init-output.log`, `grep "log_group_name" /var/log/awslogs.log`: Searches for specific terms in logs for troubleshooting.
