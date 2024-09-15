terraform {
    required_version = ">=1.3"
    
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 5.40.0, < 6"
      }
    }
    backend "gcs" {
      bucket = "sre-terraform-state-file"
      prefix = "cloudrunstatefile"
    }
}

provider "google" {
    project = var.project_id
}