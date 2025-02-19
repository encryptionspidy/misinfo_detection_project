provider "aws" {
  region = "us-east-1"
}

# S3 Bucket for Data Storage
resource "aws_s3_bucket" "misinfo_data_bucket" {
  bucket = "misinfo-detection-data-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "MisinfoDetectionData"
    Environment = "Production"
  }
}

# EC2 Instance for Model Training
resource "aws_instance" "training_instance" {
  ami           = "ami-0c55b159cbfafe1f0" # Replace with your preferred AMI
  instance_type = "t3.large"
  key_name      = "your-key-pair" # Replace with your SSH key pair

  tags = {
    Name = "MisinfoTrainingInstance"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker"
    ]
  }
}

# EKS Cluster for Model Deployment
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "misinfo-eks-cluster"
  cluster_version = "1.21"
  subnets         = ["subnet-abc123", "subnet-def456"] # Replace with your subnet IDs

  node_groups = {
    misinfo_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_type    = "t3.medium"
    }
  }

  tags = {
    Environment = "Production"
  }
}

# IAM Role for S3 Access
resource "aws_iam_role" "s3_access_role" {
  name = "misinfo-s3-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_read_write" {
  role       = aws_iam_role.s3_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.misinfo_data_bucket.bucket
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
