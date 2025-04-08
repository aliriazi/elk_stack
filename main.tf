provider "aws" {
  region = "us-west-2"
}
resource "aws_key_pair" "elk_key" {
  key_name   = "elk-key"
  public_key = file("~/.ssh/elk-key.pub")
}

resource "aws_instance" "elk_server" {
  ami           = "ami-09dc20c616c152018" # Amazon Linux 2 (example)
  instance_type = "t3.small"
  key_name      = aws_key_pair.elk_key.key_name
  tags = {
    Name = "ELK-Server"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              docker run -d -p 5601:5601 -p 9200:9200 -p 5044:5044 --name elk sebp/elk
              EOF
}
