provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "my-vpc"
  }
}

resource "aws_internet_gateway" "my_gateway" {
  vpc_id = aws_vpc.my_vpc.id

  tags = {
    Name = "my-gateway"
  }
}

resource "aws_subnet" "my_public_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true  
  
  tags = {
    Name = "my-public-subnet"
  }
}

resource "aws_route_table" "my_routing_table" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_gateway.id
  }

  tags = {
    Name = "my-routing-table"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.my_public_subnet.id
  route_table_id = aws_route_table.my_routing_table.id
}

resource "aws_main_route_table_association" "main_route_table_association" {
  vpc_id         = aws_vpc.my_vpc.id
  route_table_id = aws_route_table.my_routing_table.id
}



resource "aws_security_group" "allow_ssh_http" {
  vpc_id = aws_vpc.my_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh_http"
  }
}










resource "aws_iam_policy" "s3_access_policy" {
  name        = "S3AccessPolicy"
  description = "S3 access policy for EC2 instances"

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
        Effect   = "Allow",
        Resource = [
          "${aws_s3_bucket.my_bucket.arn}",
          "${aws_s3_bucket.my_bucket.arn}/*"
        ]
      },
    ]
  })
}


resource "aws_iam_role" "ec2_s3_access_role" {
  name = "EC2S3AccessRole"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}



resource "aws_s3_bucket" "my_bucket" {
  bucket = "ozieblomichal-fastapi-template-bucket" 
  acl    = "private"

  tags = {
    Name = "MojBucket"
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.my_bucket.bucket
}


resource "aws_iam_role_policy_attachment" "s3_access_policy_attachment" {
  role       = aws_iam_role.ec2_s3_access_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}


resource "aws_instance" "my_ec2_instance" {
  ami           = "ami-0905a3c97561e0b69"  
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.my_public_subnet.id
  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]

  iam_instance_profile = aws_iam_instance_profile.ec2_s3_access_profile.name

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              docker pull ozieblomichal/fastapi-template:amd
              docker run -d -p 80:80 -e S3_BUCKET_NAME=${aws_s3_bucket.my_bucket.bucket} ozieblomichal/fastapi-template:amd
              EOF

  tags = {
    Name = "my-ec2-instance"
  }
}