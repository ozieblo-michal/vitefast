![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)
![Alpine Version](https://img.shields.io/badge/Alpine-3.14-green.svg)
![Postgres](https://img.shields.io/badge/Postgres-16.1--alpine3.19-red.svg)

# FastAPI application installer :rocket:

### Introduction :wave:

This repository embodies a unique package that serves several critical objectives with a focus on educational value, ease of deployment, customization, and adherence to best coding and architectural practices as of January 2024. The primary goal is to provide a comprehensive learning experience, guiding users through the rationale behind each implementation, understanding the 'why' and 'how', rather than just the 'what'.

### Educational Value :school:

**Thorough Documentation:** It is committed to meticulously document every aspect of the package. The documentation emphasizes the purpose and reasoning behind each feature and implementation. This approach aims to enhance the learning experience for users, providing them with a deeper understanding of the underlying concepts and choices made during development.

### Streamlined AWS Integration :cloud:

**One-Line Deployment:** The package is designed for seamless integration with AWS services, enabling users to launch a basic application with just a single line of command in the terminal, assuming pre-configured AWS host connection settings. This feature significantly simplifies the process of deploying and managing applications on the cloud.

### Customization and Flexibility :wrench:

**Rapid Adaptation:** Acknowledging the diverse needs of different projects, the package is engineered to allow quick and straightforward adjustments. Users can easily tailor the package to meet specific requirements within a basic scope, providing both flexibility and efficiency in development.

### Technology and Best Practices :star:

**Current Package Versions:** Reflecting the latest advancements as of January 2024, ensuring that all package versions used are up-to-date, offering users the benefits of the latest features, security patches, and optimizations.

**Best Coding and Architectural Practices:** The package is built with a strong emphasis on best practices in coding and architecture. This includes the use of Alpine-based images, known for their lightweight and security-focused design. These practices not only enhance the performance and security of applications but also provide a reference point for users to learn and incorporate these practices into their own development workflows.

### Conclusion :bulb:

This package is more than just a tool for development; it's a learning journey for modern software practices, cloud integration, and effective application deployment. Whether you are a beginner looking to understand the intricacies of AWS services and application deployment, or an experienced developer seeking a quick and reliable solution for your AWS-based projects, this package is crafted to meet your needs. Join in exploring the potential of cloud computing with a solid foundation in best practices and cutting-edge technology.

I welcome contributions, feedback, and inquiries to continually improve and update this repository. Let's build and learn together!

## About FastAPI
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. The key features are:

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%. 
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.


## Package structure
```
src/
├── model/
    ├──models.py [Defines SQLAlchemy ORM models representing database tables.]
    └── __init__.py [Initializes the model package, allowing for its modules to be imported elsewhere.]
├── db/
    ├── database.py [Sets up and configures the database connection and session handling.]
    ├── fake_db.py [Provides a mock database for testing or development purposes.]
    └── __init__.py [Initializes the db package to enable database configurations.]
├── service/
    ├── services.py [Contains business logic or services related to 'Dummy' entities.]
    └── __init__.py [Initializes the service package for organizing business logic.]
├── schema/
    ├── schemas.py [Defines Pydantic models for data validation and serialization.]
    └── __init__.py [Initializes the schema package to encapsulate Pydantic models.]
├── route/
    ├── crud.py [Defines CRUD routes/endpoints for the application.]
    └── __init__.py [Initializes the route package, grouping the route modules.]
├── tests/
    ├── __init__.py [Initializes the tests package, aggregating test modules.]
    └── unit/
        ├── __init__.py [Initializes the unit testing subpackage within tests.]
        └── route/
            ├── __init__.py [Initializes the route testing module for unit tests.]
            └── test_route.py [Unit tests for route functionalities.]
└── main.py [The main entry point for the FastAPI application, defining API routes.]

```







## How to run the app on the localhost

```zsh
poetry shell
cd src
poetry run python main.py
```

in web browser, open `http://localhost:8000/docs`

## How to run the app via Docker
#### How to build image, run container and remove all after the job

```zsh
docker-compose up
```

issues:
```zsh

netstat -an | grep 5432
brew services stop postgresql

or stop process via Activity Monitor

docker-compose up --build
```

single container (currently invalid, note)
```zsh
docker build -t fastapi-template:dev . --no-cache
docker run -p 80:8000 fastapi-template:dev
docker ps
docker logs [ID OR NAME]
docker run -it --entrypoint /bin/sh fastapi-template:dev
```

in the web browser, run `localhost`

```zsh
docker stop [ID OR NAME]
docker rm [ID OR NAME]
docker images
docker rmi fastapi-template:dev
docker rmi -f $(docker images -q)

sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker system prune -a
```

## How to run tests
```zsh
cd src
poetry run python -m pytest .
```

## Cloud infrastructure diagram (x86_64 EC2)
![Cloud infrastructure diagram](cloudschema.drawio.png "Cloud infrastructure diagram")

After executing the terraform script, validate via EC2 console using (for example):
```zsh
sudo aws s3 ls s3://ozieblomichal-fastapi-template-bucket
sudo docker logs container_name
sudo docker exec -it container_name bin/sh
LATEST_LOG=$(sudo aws s3 ls s3://ozieblomichal-fastapi-template-bucket/logs/ --recursive | sort | tail -n 1 | awk '{print substr($0, index($0, $4))}')
echo $LATEST_LOG
sudo aws s3 cp "s3://ozieblomichal-fastapi-template-bucket/${LATEST_LOG}" - | cat
/var/log/syslog
/var/log/awslogs.log
sudo find / -type f -name "awslogs-agent-setup.py"
sudo systemctl status awslogsd
crontab -l
cat /var/log/cloud-init-output.log
grep "crontab" /var/log/cloud-init-output.log
grep "log_group_name" /var/log/awslogs.log
```
