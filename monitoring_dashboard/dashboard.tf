resource "google_logging_metric" "custom_uptime_log" {
  count       = var.environment == "dev" ? 1 : 0
  name        = "custom-uptime-log"
  description = "Captures Custom Uptime Check Logs"
  project     = var.project_id
  filter      = "resource.type=\"cloud_function\" AND resource.labels.function_name=\"synthetic\" AND (textPayload=~\"Failed\" OR textPayload=~\"Success Call\")"

  label_extractors = {
    "msg" = "EXTRACT(textPayload)"
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

resource "google_monitoring_custom_service" "custom_slo_service" {
  count        = var.environment == "dev" ? 1 : 0
  service_id   = "uptime-check-srv"
  display_name = "Uptime Check Service"
  project      = google_logging_metric.custom_uptime_log[0].project
}

resource "google_monitoring_slo" "custom_uptime_slo" {
  count        = var.environment == "dev" ? 1 : 0
  service      = google_monitoring_custom_service.custom_slo_service[0].service_id
  slo_id       = "uptime-slo"
  display_name = "Uptime Check Percentage"

  goal                = 0.9
  rolling_period_days = 7

  request_based_sli {
    good_total_ratio {
      good_service_filter = join(" AND ", [
        "metric.type=\"logging.googleapis.com/user/custom-uptime-check\"",
        "resource.type=\"cloud_function\"",
        "metric.labels.msg=monitoring.regex.full_match(\"Success.*\")",
      ])
      total_service_filter = join(" AND ", [
        "metric.type=\"logging.googleapis.com/user/custom-uptime-check\"",
        "resource.type=\"cloud_function\"",
      ])
    }
  }
}

resource "google_monitoring_dashboard" "custom_uptime_dashboard" {
  project  = var.project_id
  for_each = var.environment == "dev" ? local.uptime_dashboard_json : []
  dashboard_json = templatefile(each.key, {
    PROJECT_ID = var.project_id
    SERVICE_ID = google_monitoring_slo.custom_uptime_slo[0].service
    SLO_ID     = google_monitoring_slo.custom_uptime_slo[0].slo_id
  })
}
