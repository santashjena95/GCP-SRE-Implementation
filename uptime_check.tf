project_id                = "sre-project-poc"
--------------------------------------------------------------------------
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
-------------------------------------------------------------------------
resource "google_monitoring_notification_channel" "email" {
    display_name = "Santash Non-Official Email"
    type = "email"
    labels = {
        email_address = "jenasantosh95@gmail.com"
    }
}

resource "google_monitoring_uptime_check_config" "https" {
  display_name = "https-uptime-check"
  timeout = "10s"
  period  = "60s"

  http_check {
    path = "/"
    port = "443"
    use_ssl = true
    accepted_response_status_codes {
      status_class = "STATUS_CLASS_2XX"
    }
    accepted_response_status_codes {
      status_class = "STATUS_CLASS_3XX"
    }
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      host       = "otel-run-1058717846530.us-central1.run.app"
      project_id = var.project_id
    }
  }
}

resource "google_monitoring_alert_policy" "alert_policy_uptime_check" {
  project = var.project_id
  enabled = true
  display_name = "UptimeCheckAlert"
  combiner     = "OR"
  severity = "CRITICAL"
  documentation {
    content = "Uptime Check Failed"
    subject = "Uptime Check Failed"
  }
  notification_channels = flatten([google_monitoring_notification_channel.email.name])
  conditions {
   display_name = "UptimeCheckAlert"
   condition_threshold {
      filter     = format("metric.type=\"monitoring.googleapis.com/uptime_check/check_passed\" AND metric.labels.\"check_id\"=\"%s\" AND resource.type=\"uptime_url\"",google_monitoring_uptime_check_config.https.uptime_check_id)
      duration   = "60s"
      comparison = "COMPARISON_GT"
      threshold_value = "1"
      aggregations {
        alignment_period   = "1200s"
        per_series_aligner = "ALIGN_NEXT_OLDER"
        cross_series_reducer = "REDUCE_COUNT_FALSE"
        group_by_fields = [
          "resource.label.project_id",
          "resource.label.host"
        ]
      }
      trigger {
          count = 1
      }
   }
  }
  lifecycle {
    create_before_destroy = true
  }
}
-------------------------------------------------------------------------------
variable "project_id" {
  type        = string
  description = "The project ID of the cloud run service"
}
