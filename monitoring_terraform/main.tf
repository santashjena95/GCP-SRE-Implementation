module "cloud_run_monitoring" {
    source                    = "../module/monitoring"
    project_id                = var.project_id
    email_address_notify      = var.email_address_notify
    custom_metric_name        = var.custom_metric_name
    monitoring_display_name   = var.monitoring_display_name
    notify_subject_line       = var.notify_subject_line
}