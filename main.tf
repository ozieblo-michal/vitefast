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

resource "aws_instance" "my_ec2_instance" {
  ami           = "ami-0905a3c97561e0b69"  
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.my_public_subnet.id
  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              docker pull ozieblomichal/fastapi-template:amd
              docker run -d -p 80:80 ozieblomichal/fastapi-template:amd
              EOF

  tags = {
    Name = "my-ec2-instance"
  }
}
