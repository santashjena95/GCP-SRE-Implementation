project_id                = "sre-project-poc"
run_name                  = "otel-run"
region                    = "us-central1"
public_cloud_run          = true
ingress_service_name      = "app"
# ingress_image             = "us-central1-docker.pkg.dev/sre-project-poc/otel-run/mainapp:latest"
otel_sidecar_service_name = "collector"
# otel_sidecar_image        = "us-central1-docker.pkg.dev/sre-project-poc/otel-run/otelsidecar:latest"