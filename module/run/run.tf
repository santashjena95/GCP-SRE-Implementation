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

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_v2_service_iam_policy" "noauth" {
  count       = var.public_cloud_run ? 1 : 0
  location    = google_cloud_run_v2_service.run.location
  project     = google_cloud_run_v2_service.run.project
  service     = google_cloud_run_v2_service.run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}