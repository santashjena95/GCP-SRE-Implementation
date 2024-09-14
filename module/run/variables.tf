variable "run_name" {
  type        = string
  description = "The name of the cloud run service"
}

variable "region" {
  type        = string
  description = "The region of the cloud run service"
  default     = "us-central1"
}

variable "ingress_service_name" {
  type        = string
  description = "Name of the main app container service"
  default     = "mainapp"
}

variable "ingress_image" {
  type        = string
  description = "Image for the main app container service"
}

variable "otel_sidecar_service_name" {
  type        = string
  description = "Name of the otel sidecar container service"
  default     = "collector"
}

variable "otel_sidecar_image" {
  type        = string
  description = "Image for the otel sidecar container service"
}

variable "public_cloud_run" {
  type        = bool
  description = "Whether the cloud run will be publcily available or not"
  default     = true
}