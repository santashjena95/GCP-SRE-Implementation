resource "google_cloud_run_v2_service" "run" {
  name     = var.run_name
  location = var.region
  launch_stage = "BETA"
  ingress = "INGRESS_TRAFFIC_ALL"
  template {
    containers {
      name = var.ingress_service_name
      ports {
        container_port = 8080
      }
      image = var.ingress_image
      env {
        name = "OTEL_EXPORTER_OTLP_ENDPOINT"
        value = "http://localhost:4317"
      }
      depends_on = [var.otel_sidecar_service_name]
    }
    containers {
      name = var.otel_sidecar_service_name
      image = var.otel_sidecar_image
      startup_probe {
        http_get {
          path = "/"
          port = 13133
        }
      }
      }
    }
    lifecycle {
        ignore_changes = [
        launch_stage, ingress,
        ]
    }
  }