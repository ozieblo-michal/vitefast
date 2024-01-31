![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)
![Alpine Version](https://img.shields.io/badge/Alpine-3.14-green.svg)
![Postgres](https://img.shields.io/badge/Postgres-16.1--alpine3.19-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.108.0-009688.svg)
[![Docker and Pytest Workflow](https://github.com/ozieblo-michal/fastAPI-templates/actions/workflows/docker_and_pytest.yml/badge.svg)](https://github.com/ozieblo-michal/fastAPI-templates/actions/workflows/docker_and_pytest.yml)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Pylint](https://img.shields.io/badge/linter-pylint-blue.svg)


# FastAPI engine :rocket:

### Introduction :wave:

This repository is a **ready-to-use web applications backend template, designed for  effortless deployment**. It was crafted to ease rapid and easy customization, catering to diverse needs and preferences. **Documentation focuses on 'why' and 'how', not 'what'**. The package follows the best coding and architectural practices as of January 2024.

### Prerequisites for Working with the Package :school:

Before diving into the package, it's important to familiarize yourself with a few foundational tools and concepts:

- **FastAPI Documentation**: A thorough understanding of FastAPI, a modern, fast web framework for building APIs with Python, is crucial. Familiarize yourself with its key features and functionalities by reviewing [FastAPI Documentation](https://fastapi.tiangolo.com/).
- **Basic Docker Commands**: Knowledge of Docker, a tool designed to make it easier to create, deploy, and run applications using containers, is essential. Brush up on the [Docker Documentation](https://docs.docker.com/get-started/overview/).
- **Basic Terraform Commands**: Terraform, used for building, changing, and versioning infrastructure safely and efficiently, is another key tool. Review the [Terraform Documentation](https://www.terraform.io/docs/index.html) to understand its core principles and commands.

### Running the package :runner:

To run the package, you have two options depending on your preference:

#### 1. Cloud infrastructure diagram - variant with RDS (x86_64 EC2)
![Cloud infrastructure diagram](/img/RDSschema.png "Cloud infrastructure diagram - variant with RDS")

#### 2. Cloud infrastructure diagram - variant with Postgres as a microservice (x86_64 EC2)
![Cloud infrastructure diagram](img/dbmicroserviceschema.png "Cloud infrastructure diagram - variant with Postgres as a microservice")

1. **AWS Deployment:** 
   - First, log in to your AWS account using the AWS Command Line Interface (CLI).
   - Install Terraform on your machine.
   - Navigate to the `terraform` directory containing the `main.tf` Terraform configuration file. Choose a version using a Postgres database on AWS RDS or available as a microservice in EC2 with the application.
   - Execute `terraform plan` to review the planned infrastructure changes.
   - Apply these changes by running `terraform apply`.
   - After you're done, and if you wish to tear down the infrastructure, use `terraform destroy`.

2. **Local Deployment:**
   - Ensure you have Docker and Docker Compose installed on your local machine.
   - Run `docker compose up` from the main directory containing your `docker-compose.yml` file. 
   - This will start the application locally using Docker.

### Streamlined AWS Integration :cloud:

**One-Line Deployment:** The package was designed for seamless integration with AWS services. It enables to launch a basic application with a single line in the terminal. This feature simplifies the process of deploying and managing applications on the cloud.

### Educational Value :school:

**Thorough Documentation:** It was committed to document every aspect of the package. The documentation emphasizes the purpose and reasoning behind each feature and implementation.

### Customization and Flexibility :wrench:

**Quick Adaptation:** The package was engineered to allow quick and straightforward adjustments. Users may tailor the package to specific requirements, providing development flexibility and efficiency.

### Technology and Best Practices :star:

**Current Package Versions:** As of January 2024, all packages are up-to-date, offering latest features, security patches, and optimizations.

**Best Coding and Architectural Practices:** The package was built with a strong emphasis on best practices in coding and architecture. This includes the use of Alpine-based images, known for their lightweight and security-focused design. These practices enhance the performance and security of applications.

### Why FastAPI, not Flask :muscle:
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. The key features are:

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%. 
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.

### Advantages of Using Alpine Images for Ubuntu and Postgres :mount_fuji:
Alpine was renowned for its minimalistic size, which results in lighter and faster containers. It reduces the download and deployment time, but also lessens the resource consumption. It makes it ideal for environments with limited resources. Alpine's minimalistic nature means also fewer components susceptible to vulnerabilities, enhancing the security of the containers. This makes Alpine an excellent choice for streamlined, secure, and efficient containerized applications.

### AWS RDS Postgres vs. Containerized Postgres :grey_question:

**AWS RDS Postgres**
- Advantages: Managed service (simplifies administration), high availability, scalable, secure, integrated monitoring.
- Disadvantages: May lack the latest Postgres version, higher cost, less control, potential vendor lock-in.

**Containerized Postgres**
- Advantages: Access to the latest Postgres versions, more control over configuration, cost-effective, portable across environments.
- Disadvantages: Increased management overhead, complex high availability setup, additional security responsibilities, resource-intensive management.

The choice between AWS RDS and a containerized Postgres hinges on needs for the latest Postgres features, budget, control level, and scalability.

### How to Run Tests :white_check_mark:

- `cd src`: Change directory to the source code.

- `poetry run python -m pytest .` : Runs tests using pytest within the poetry environment.

### Conclusion :bulb:

This package is more than an engine. Whether you are a beginner looking to understand the intricacies of AWS services and application deployment, or an experienced developer seeking a quick and reliable solution for your AWS-based projects, this package was crafted to meet your needs.

I welcome contributions, feedback, and inquiries to continually improve and update this repository. Let's build and learn together!