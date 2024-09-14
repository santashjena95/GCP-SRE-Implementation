module "cloud_run" {
    source                    ="../module/run"
    run_name                  = var.run_name
    region                    = var.region
    ingress_service_name      = var.ingress_service_name
    ingress_image             = var.ingress_image
    otel_sidecar_service_name = var.otel_sidecar_service_name
    otel_sidecar_image        = var.otel_sidecar_image
}