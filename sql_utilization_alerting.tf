project_id                = "sre-project-poc"
email_address_notify      = "jenasantosh95@gmail.com"
monitoring_display_name   = "SQL CPU Utilization > 80%"
notify_subject_line       = "Cloud SQL CPU Utilization Is More Than 80%"
-----------------------------------------------------------------------------------
resource "google_monitoring_notification_channel" "email" {
    display_name = "Santash's Non Official Email"
    type = "email"
    labels = {
        email_address = var.email_address_notify
    }
}

resource "google_monitoring_alert_policy" "sql_cpu_utilize" {
  display_name = var.monitoring_display_name
  documentation {
    content = "The $${metric.display_name} of the $${resource.type} $${resource.label.database_id} in $${resource.project} has exceeded 80% for over 1 minute."
    subject = var.notify_subject_line
  }
  combiner     = "OR"
  conditions {
    display_name = var.monitoring_display_name
    condition_threshold {
        comparison = "COMPARISON_GT"
        duration = "60s"
        filter = "resource.type = \"cloudsql_database\" AND metric.type = \"cloudsql.googleapis.com/database/cpu/utilization\""
        threshold_value = "0.04"
        trigger {
          count = "1"
        }
    }
  }

  alert_strategy {
    auto_close = "1800s"
  }

  notification_channels = flatten([google_monitoring_notification_channel.email.name])

  severity = "WARNING"
  enabled = true
  lifecycle {
    create_before_destroy = true
  }
}
-------------------------------------------------------------------------------
variable "project_id" {
  type        = string
  description = "The project ID of the cloud run service"
}

variable "email_address_notify" {
  type        = string
  description = "Email Id of the error message recipient"
}

variable "monitoring_display_name" {
  type        = string
  description = "Display name of monitoring alert"
}

variable "notify_subject_line" {
  type        = string
  description = "The subject line of the Alert email"
}
-------------------------------------------------------------------------------------------
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
      prefix = "teststatefile"
    }
}

provider "google" {
    project = var.project_id
}
