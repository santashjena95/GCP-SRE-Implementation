resource "google_monitoring_notification_channel" "email" {
    display_name = "Notification Email"
    type = "email"
    labels = {
        email_address = var.email_address_notify
    }
}

resource "google_logging_metric" "cloud_run_error" {
  name   = var.custom_metric_name
  description = "Captures Cloud Run Error"
  project = var.project_id
  filter = "resource.type=\"cloud_run_revision\" AND severity >= ERROR"
  
  label_extractors = {
    "run_name" = "EXTRACT(resource.labels.service_name)"
    "reason" = "EXTRACT(protoPayload.response.status.conditions.reason)"
    "msg" = "EXTRACT(protoPayload.response.status.conditions.message)"
  }
  metric_descriptor {
    value_type  = "INT64"
    metric_kind = "DELTA"
    labels {
      key = "run_name"
      value_type = "STRING"
    }
    labels {
      key = "reason"
      value_type = "STRING"
    }
    labels {
      key = "msg"
      value_type = "STRING"
    }
  }
}

resource "null_resource" "delay" {
  provisioner "local-exec" {
    command = "sleep 60"
  }
}

resource "google_monitoring_alert_policy" "cloud_run_error_alert_policy" {
  project = var.project_id
  display_name = var.monitoring_display_name
  documentation {
    content = "The $${metric.display_name} of the $${resource.type} $${log.extracted_label.run_name} in $${resource.project} has $${log.extracted_label.msg} Error because of $${log.extracted_label.reason} reason."
    subject = var.notify_subject_line
  }
  combiner     = "OR"
  conditions {
    display_name = var.monitoring_display_name
    condition_threshold {
        comparison = "COMPARISON_GT"
        duration = "0s"
        filter = <<-EOT
         metric.type="logging.googleapis.com/user/${google_logging_metric.cloud_run_error.id}"
         resource.type = "cloud_run_revision"
        EOT
        trigger {
          count = "1"
        }
        aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_COUNT"
      }
    }
  }

  alert_strategy {
    auto_close = "1800s"
  }
  severity = "ERROR"

  notification_channels = flatten([google_monitoring_notification_channel.email.name])
  enabled = true
  depends_on = [null_resource.delay]
}