provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "main" {
  // VPC configuration
}

resource "aws_subnet" "main" {
  // subnet configuration
}

resource "aws_security_group" "fastapi_sg" {
  name        = "fastapi_sg"
  description = "Security group for FastAPI app"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
