# Setting up monitoring for Timeliness Check for Data Quality
resource "google_logging_metric" "timeliness_dq_file_missing_1" {
  name        = "timeliness-dq-file-missing-1"
  description = "Captures the timeliness Check Logs for Data Quality"
  project     = var.project_id
  filter      = <<-EOT
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
      key        = "msg"
      value_type = "STRING"
    }
  }
}


resource "google_monitoring_alert_policy" "timeliness_dq_log_alert" {
  project      = var.project_id
  display_name = "Alert for Timeliness Check Logs for Data Quality"
  documentation {
    content = "The Alert for Timeliness Check Logs for Data Quality of the $${resource.type} in $${resource.project}."
    subject = "Alert for Timeliness Check Logs for Data Quality"
  }
  combiner = "OR"
  conditions {
    display_name = "timeliness-dq-log-1"
    condition_threshold {
      comparison = "COMPARISON_LT"
      duration   = "0s"
      threshold_value = "1"
      filter     = <<-EOT
         metric.type="logging.googleapis.com/user/${google_logging_metric.timeliness_dq_file_missing_1.id}"
         resource.type = "cloud_function"
        EOT
      trigger {
        count = "1"
      }
      aggregations {
        alignment_period     = "86700s"
        per_series_aligner   = "ALIGN_SUM"
        cross_series_reducer = "REDUCE_SUM"
        group_by_fields      = ["metric.label.msg"]
      }
    }
  }

  alert_strategy {
    auto_close = "1800s"
  }
  severity = "ERROR"

  notification_channels = ["projects/turnkey-cove-443706-t1/notificationChannels/18424733301046705249"]
  enabled               = true
}
