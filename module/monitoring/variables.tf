variable "project_id" {
  type        = string
  description = "The project ID of the cloud run service"
}

variable "email_address_notify" {
  type        = string
  description = "Email Id of the error message recipient"
}

variable "custom_metric_name" {
  type        = string
  description = "Name for the custom log based metrics"
}

variable "monitoring_display_name" {
  type        = string
  description = "Display name of monitoring alert"
}

variable "notify_subject_line" {
  type        = string
  description = "The subject line of the Alert email"
}