# This repo deploys cloud run using terraform with opentelemetry as sidecar container

## 1. Go to GCP artifact registry and create repository.

## 2. Then run the github action pipeline for building and pushing the docker image to Google Artifact Registry.

## 3. Then it will automatically trigger the cloud run terraform module for the deploying cloud run with the image pushed to google artifact registry

## 4. Then it will automatically trigger the monitoring terraform module for the deploying custom log based metrics and associated monitoring alert

## NOTE: Permissions needed for service account of terraform for monitoring: Logs Configuration Writer, Monitoring AlertPolicy Editor, Monitoring NotificationChannel Editor

## Important Docs:

### i. https://github.com/actions/download-artifact?tab=readme-ov-file#download-artifacts-from-other-workflow-runs-or-repositories

### ii. https://stackoverflow.com/questions/64868918/how-to-download-artifact-release-asset-in-another-workflow

### iii. https://github.com/actions/download-artifact#inputs

### iv. https://cloud.google.com/run/docs/tutorials/custom-metrics-opentelemetry-sidecar

### v. https://cloud.google.com/run/docs/deploying#terraform_2

### vi. https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_alert_policy#severity

### vii. https://github.com/hashicorp/terraform-provider-google/blob/main/website/docs/r/monitoring_alert_policy.html.markdown

### viii. https://cloud.google.com/monitoring/alerts/notification-terraform

### ix. https://github.com/hashicorp/terraform-provider-google-beta/blob/main/website/docs/r/logging_metric.html.markdown