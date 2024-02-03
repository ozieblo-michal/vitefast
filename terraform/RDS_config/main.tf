terraform {
  required_version = "1.6.6"  # Specifies the version of Terraform required for this configuration. Ensures consistency and compatibility.
  required_providers {
    aws = {
      source  = "hashicorp/aws"  # The source of the AWS provider, indicating where Terraform should fetch it from.
      version = ">= 3.0"  # Specifies the minimum version of the AWS provider required, ensuring features and syntax compatibility.
    }
  }
}

provider "aws" {
  region = "eu-west-1"  # Sets the AWS region for resources. This is where your resources will be created.
}

variable "region" {
  description = "The AWS region"  # A descriptive detail about the variable.
  default     = "eu-west-1"  # Default value for the region, used if no other value is provided.
  type = string  # Specifies the type of the variable, in this case, a string.
}


data "aws_caller_identity" "current" {}  # Retrieves information about the AWS account running the Terraform. Useful for dynamic referencing in policies or other resources.

resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"  # Defines the IP range for the VPC. This is a private network space for your AWS resources.
  tags = {
    Name = "my-vpc"  # Naming your VPC for easier identification and management.
  }
}

resource "aws_internet_gateway" "my_gateway" {
  vpc_id = aws_vpc.my_vpc.id  # Associates this internet gateway with the previously defined VPC, enabling access to the internet.

  tags = {
    Name = "my-gateway"  # Naming your internet gateway for easier identification.
  }
}

resource "aws_subnet" "my_public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"  # Specifies a subset of the VPC's IP range where resources can be placed.
  availability_zone       = "eu-west-1a"  # Specifies the AZ for high availability and redundancy.
  map_public_ip_on_launch = true  # Automatically assigns a public IP to instances launched in this subnet, making them accessible from the internet.

  tags = {
    Name = "my-public-subnet"  # Naming your subnet for easier identification and management.
  }
}


resource "aws_subnet" "my_secondary_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"  # Another subnet for organizational purposes, possibly for separating different types of resources.
  availability_zone       = "eu-west-1b"  # Placed in a different AZ for redundancy and failover capabilities.
  map_public_ip_on_launch = true  # Enables public IP assignment for resources in this subnet as well.

  tags = {
    Name = "my-secondary-subnet"  # Helps in distinguishing between subnets.
  }
}



resource "aws_route_table" "my_routing_table" {
  vpc_id = aws_vpc.my_vpc.id  # Associates this route table with your VPC, directing traffic based on the routes defined below.

  route {
    cidr_block = "0.0.0.0/0"  # Represents all IP addresses; this route directs internet-bound traffic to the internet gateway.
    gateway_id = aws_internet_gateway.my_gateway.id  # The gateway to route traffic through, enabling internet access.
  }

  tags = {
    Name = "my-routing-table"  # Naming the routing table for identification.
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.my_public_subnet.id  # Associates the routing table with a specific subnet, directing its traffic according to the table's rules.
  route_table_id = aws_route_table.my_routing_table.id  # The specific routing table to associate.
}

resource "aws_main_route_table_association" "main_route_table_association" {
  vpc_id         = aws_vpc.my_vpc.id  # Identifies the VPC for which this route table becomes the main (default) routing table.
  route_table_id = aws_route_table.my_routing_table.id  # Sets this routing table as the main one for the VPC.
}



resource "aws_security_group" "allow_ssh_http" {
  vpc_id = aws_vpc.my_vpc.id  # Associates the security group with your VPC, applying its rules to resources within the VPC.

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows inbound PostgreSQL traffic from any IP address, for database access.
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows SSH access from any IP address, for server management.
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows HTTP traffic from any IP address, for web server access.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allows all outbound traffic, ensuring that instances can initiate connections to the internet or other services.
  }

  tags = {
    Name = "allow_ssh_http"  # Helps in identifying the purpose of this security group.
  }
}


resource "aws_iam_policy" "s3_access_policy" {
  name        = "S3AccessPolicy"  # Defines a policy name for easier identification.
  description = "S3 access policy for EC2 instances"  # Provides a clear description of the policy's purpose.

  # The policy definition in JSON format, granting specific actions on S3 resources.
  # This enables EC2 instances with this policy to list buckets, and get, put, delete objects in the specified S3 bucket.
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Effect = "Allow",
        Resource = [
          "${aws_s3_bucket.my_bucket.arn}",
          "${aws_s3_bucket.my_bucket.arn}/*"
        ]
      },
      {
        Action   = "s3:ListAllMyBuckets",
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "ec2_s3_access_role" {
  name = "EC2S3AccessRole"  # Names the IAM role for EC2 instances to access S3.

  # The trust relationship policy that allows EC2 instances to assume this role.
  # It defines the principle service as EC2, enabling instances to adopt the permissions specified in attached policies.
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "ozieblomichal-fastapi-template-bucket"  # Specifies the name of the S3 bucket for storing application data or logs.

  tags = {
    Name = "MojBucket"  # Tags the bucket for organizational and billing purposes.
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.my_bucket.bucket  # Outputs the name of the S3 bucket for reference in other configurations or modules.
}

resource "aws_iam_role_policy_attachment" "s3_access_policy_attachment" {
  role       = aws_iam_role.ec2_s3_access_role.name  # Attaches the defined S3 access policy to the EC2 role.
  policy_arn = aws_iam_policy.s3_access_policy.arn  # Specifies the ARN of the policy to attach.
}

resource "aws_cloudwatch_log_group" "my_log_group" {
  name = "/aws/ec2/my-log-group"  # Names the CloudWatch Log Group for collecting logs.

  retention_in_days = 1  # Sets log retention policy to 1 day to minimize storage costs.

  tags = {
    Name = "MyLogGroup"  # Helps in identifying the log group within CloudWatch.
  }
}

resource "aws_iam_role" "ec2_cloudwatch_log_role" {
  name = "EC2CloudWatchLogRole"  # Defines a role for EC2 instances to interact with CloudWatch Logs.

  # Policy allowing EC2 instances to assume this role, specifically for logging purposes.
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "ec2_cloudwatch_log_policy" {
  name        = "EC2CloudWatchLogPolicy"
  description = "Policy allowing EC2 instances to send logs to CloudWatch"  # Describes the policy's intent.

  # The policy itself, in JSON format, granting permissions to create log streams and put log events into CloudWatch.
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams",
          "logs:CreateLogGroup"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/ec2/my-log-group:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_cloudwatch_log_policy_attachment" {
  role       = aws_iam_role.ec2_cloudwatch_log_role.name  # Attaches the CloudWatch logging policy to the role.
  policy_arn = aws_iam_policy.ec2_cloudwatch_log_policy.arn  # References the policy to attach.
}

resource "aws_iam_instance_profile" "ec2_s3_access_profile" {
  name = "EC2S3AccessProfile"  # Creates an instance profile for EC2 instances, enabling them to use the IAM role for S3 access.
  role = aws_iam_role.ec2_s3_access_role.name  # Associates the S3 access role with the instance profile.
}


resource "aws_iam_policy" "ec2_cloudwatch_logs_policy" {
  name        = "EC2CloudWatchLogsPolicy"
  description = "Policy allowing EC2 instances to send logs to CloudWatch Logs"
  # This policy enables EC2 instances to interact with CloudWatch Logs, allowing for the creation of log groups and streams, and the ability to put log events. This is essential for detailed monitoring and logging of application behavior and system performance.
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_cloudwatch_logs_policy_attachment" {
  role       = aws_iam_role.ec2_s3_access_role.name  # Attaches the CloudWatch Logs policy to the EC2 role, ensuring instances using this role can perform logging operations.
  policy_arn = aws_iam_policy.ec2_cloudwatch_logs_policy.arn
}

resource "aws_db_instance" "my_postgres_db" {
  allocated_storage   = 20  # Specifies the amount of storage allocated to the database instance, balancing cost with performance and storage requirements.
  storage_type        = "gp2"  # General Purpose SSD storage provides a balance of performance and cost.
  engine              = "postgres"  # Chooses PostgreSQL for its robust features and compatibility with various applications.
  engine_version      = "15.4"  # Specifies the version of PostgreSQL, ensuring compatibility with the application's requirements.
  instance_class      = "db.t3.micro"  # Selects a cost-effective instance class suitable for development or small production workloads.
  identifier          = "mydatabase"  # Provides a unique identifier for the database instance for easier management and reference.
  db_name             = "mydatabase"  # The name of the database created when the instance is launched, simplifying application configuration.
  username            = "postgres"  # Default administrative username, commonly used with PostgreSQL.
  password            = "mocnehaslo123"  # Sets a password for the database user, essential for securing database access.
  skip_final_snapshot = true  # Skips the creation of a final snapshot on deletion, suitable for development environments where persistence is not required.
  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]  # Associates the database with a security group, controlling access to the database instance.

  db_subnet_group_name = aws_db_subnet_group.my_db_subnet_group.name  # Associates the database instance with a subnet group, ensuring it is placed within the VPC for network isolation and security.

  tags = {
    Name = "MojaBazaDanychPostgres"  # Tags the database instance for organizational, billing, or management purposes.
  }
}

resource "aws_db_subnet_group" "my_db_subnet_group" {
  name       = "my-db-subnet-group"  # Names the DB subnet group for easier identification and management.
  subnet_ids = [aws_subnet.my_public_subnet.id, aws_subnet.my_secondary_subnet.id]  # Specifies the subnets in which the database should operate, ensuring high availability and network isolation.

  tags = {
    Name = "MyDBSubnetGroup"  # Tags the DB subnet group for organizational purposes.
  }
}

output "db_endpoint" {
  value = aws_db_instance.my_postgres_db.endpoint  # Outputs the database endpoint, providing a connection string that applications can use to connect to the database.
}


resource "aws_instance" "my_ec2_instance" {
  ami                         = "ami-0905a3c97561e0b69" # Specifies the AMI to be used, ensuring the instance is launched with the required OS and configurations.
  instance_type               = "t2.micro" # Chooses an instance type that balances cost and performance for the intended workload.
  subnet_id                   = aws_subnet.my_public_subnet.id # Ensures the instance is placed within a specific subnet for network isolation and control.
  associate_public_ip_address = true # Assigns a public IP address to enable direct access from the internet, necessary for web-facing applications.

  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id] # Associates the instance with a security group to control traffic flow, allowing for SSH, HTTP, and database access.

  iam_instance_profile = aws_iam_instance_profile.ec2_s3_access_profile.name # Attaches an IAM role to the instance, granting it permissions to interact with specified AWS services, like S3.

  # User data script for initial setup, such as installing necessary software, pulling a Docker image, and starting a container.
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              docker pull --pull always ozieblomichal/fastapi-template:latest
              mkdir /home/ubuntu/myapp-logs
              
              mkdir -p /var/awslogs/etc

              docker run -d -p 80:80 -e DATABASE_URL="postgresql://postgres:mocnehaslo123@${aws_db_instance.my_postgres_db.endpoint}/mydatabase" -e S3_BUCKET_NAME=${aws_s3_bucket.my_bucket.bucket} \
              -v /home/ubuntu/myapp-logs:/logs \
              -v /home/ubuntu/uploads:/uploads \
              ozieblomichal/fastapi-template:latest
              
              apt-get install -y awscli
              
              # Script to periodically upload logs to S3, illustrating automation and backup of application logs for auditing or analysis.
              cat <<'SCRIPT' >/home/ubuntu/upload_logs_to_s3.sh
              #!/bin/bash
              BUCKET_NAME="${aws_s3_bucket.my_bucket.bucket}"
              LOG_DIRECTORY="/home/ubuntu/myapp-logs"

              LOG_FILE="/home/ubuntu/myapp-logs/$(date -d "+1 hour" +'%Y-%m-%d %H'):00-$(date -d "$(date +'%Y-%m-%d %H') + 2 hours" +'%H'):00.log"

              S3_KEY="logs/$(date -d "+1 hour" +'%Y-%m-%d %H'):00-$(date -d "$(date +'%Y-%m-%d %H') + 2 hours" +'%H'):00.log"

              if [ -f "$LOG_FILE" ]; then
                  aws s3 cp "$LOG_FILE" "s3://$BUCKET_NAME/$S3_KEY"
              fi
              SCRIPT

              chmod +x /home/ubuntu/upload_logs_to_s3.sh

              # Configures the instance to install and run the AWS CloudWatch Logs agent, facilitating comprehensive logging and monitoring of the instance and applications running on it.
              add-apt-repository ppa:deadsnakes/ppa
              apt-get update -y
              apt-get install -y python2.7

              cd /home/ubuntu/ && curl https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py -O

              chmod +x ./awslogs-agent-setup.py
              
              # Configuration for the AWS CloudWatch Logs agent, specifying log files and destinations, enhancing operational insight through log aggregation and analysis.
              cat > /tmp/awslogs.conf <<- EOM

              [general]
              state_file = /var/awslogs/state/agent-state

              [myapp_logs]
              file = /home/ubuntu/myapp-logs/*.log
              log_group_name = myapp-log-group
              log_stream_name = {instance_id}-{file_name}
              datetime_format = %Y-%m-%d %H:%M:%S

              EOM

              python2.7 ./awslogs-agent-setup.py -n -r ${var.region} -c /tmp/awslogs.conf

              sleep 180 

              service cron start
              echo "*/1 * * * * /home/ubuntu/upload_logs_to_s3.sh" > /home/ubuntu/crontab_file
              crontab /home/ubuntu/crontab_file

              service awslogs start
              EOF

  # Tags the EC2 instance for easier identification and management within the AWS environment.
  tags = {
    Name = "my-ec2-instance"
  }
}
