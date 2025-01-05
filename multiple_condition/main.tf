resource "google_monitoring_notification_channel" "email" {
    display_name = "Notification Email"
    type = "email"
    labels = {
        email_address = var.email_address_notify
    }
}

# Setting up monitoring for Timeliness Check for Data Quality
resource "google_logging_metric" "timeliness_dq_log_1" {
  name   = "timeliness-dq-log-1"
  description = "Captures the timeliness Check Logs for Data Quality"
  project = var.project_id
  filter = <<-EOT
    resource.type="cloud_function" AND
    textPayload =~ "Total records retrieved from PR2: 0" AND
    logName = "projects/${var.project_id}/logs/cloudfunctions.googleapis.com%2Fcloud-functions"
    EOT
  label_extractors = {
    "msg" = "EXTRACT(protoPayload.status.message)"
  }
  metric_descriptor {
    value_type  = "INT64"
    metric_kind = "DELTA"
    labels {
      key = "msg"
      value_type = "STRING"
    }
  }
}

# Setting up monitoring for Timeliness Check for Data Quality
resource "google_logging_metric" "timeliness_dq_log_2" {
  name   = "timeliness-dq-log-2"
  description = "Captures the timeliness Check Logs for Data Quality"
  project = var.project_id
  filter = <<-EOT
    resource.type="cloud_function" AND
    textPayload =~ "source: gs://${var.project_id}/speech_to_text_monitored_user_BAU*" AND
    logName = "projects/${var.project_id}/logs/cloudfunctions.googleapis.com%2Fcloud-functions"
    EOT
  label_extractors = {
    "msg" = "EXTRACT(protoPayload.status.message)"
  }
  metric_descriptor {
    value_type  = "INT64"
    metric_kind = "DELTA"
    labels {
      key = "msg"
      value_type = "STRING"
    }
  }
}

resource "google_monitoring_alert_policy" "timeliness_dq_log_alert" {
  project = var.project_id
  display_name = "Alert for Timeliness Check Logs for Data Quality"
  documentation {
    content = "The Alert for Timeliness Check Logs for Data Quality of the $${resource.type} in $${resource.project}."
    subject = "Alert for Timeliness Check Logs for Data Quality"
  }
  combiner     = "AND"
  conditions {
    display_name = "timeliness-dq-log-1"
    condition_threshold {
        comparison = "COMPARISON_GT"
        duration = "0s"
        filter = <<-EOT
         metric.type="logging.googleapis.com/user/${google_logging_metric.timeliness_dq_log_1.id}"
         resource.type = "cloud_function"
        EOT
        trigger {
          count = "1"
        }
        aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_COUNT"
        cross_series_reducer = "REDUCE_COUNT"
        group_by_fields = ["metric.label.msg"]
      }
    }
  }

  conditions {
    display_name = "timeliness-dq-log-2"
    condition_threshold {
        comparison = "COMPARISON_GT"
        duration = "0s"
        filter = <<-EOT
         metric.type="logging.googleapis.com/user/${google_logging_metric.timeliness_dq_log_2.id}"
         resource.type = "cloud_function"
        EOT
        trigger {
          count = "1"
        }
        aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_COUNT"
        cross_series_reducer = "REDUCE_COUNT"
        group_by_fields = ["metric.label.msg"]
      }
    }
  }

  alert_strategy {
    auto_close = "1800s"
  }
  severity = "ERROR"

  notification_channels = flatten([google_monitoring_notification_channel.email.name])
  enabled = true
}
