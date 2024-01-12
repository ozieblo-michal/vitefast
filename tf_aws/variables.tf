variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "image" {
  description = "Docker image"
  type        = string
  default = "ozieblomichal/fastapi-template:dev"
}
