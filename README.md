# This repo deploys cloud run using terraform with opentelemetry as sidecar container

## 1. Go to GCP artifact registry and create repository

## 2. Then run the github action pipeline for building and pushing the docker image to Google Artifact Registry.

## 3. Then it will automatically trigger the cloud run terraform module for the deploying cloud run with the image pushed to google artifact registry

## 4. Then it will automatically trigger the monitoring terraform module for the deploying custom log based metrics and associated monitoring alert

## NOTE: We have two ways of deploying cloud run sidecar containers -

## a. Running "gcloud run services replace service.yaml" command in run_service/ folder that will create cloud run with the otel sidecar container

## b. Running "cloudrunterraform.yaml" github actions workflow (This will be automatically triggered if new code is pushed to app_code/ or collector/ code, which will trigger pushtoartifact.yaml workflow and this will trigger cloudrunterraform.yaml workflow) (Make sure if we are running "cloudrunterraform.yaml" workflow manually, atleast one run for "pushtoartifact.yaml" has already happened as we are utilizing the sha from it for image push and that image is used in cloud run)

## NOTE: Permissions needed for service account of terraform for monitoring: Logs Configuration Writer, Monitoring AlertPolicy Editor, Monitoring NotificationChannel Editor

## NOTE: group_by_fields is important for defining log based metrics labels in documentation of monitoring alert policy

## NOTE: Before trigerring the image build and push workflow pipeline make sure to create the repos in Google Artifact registry

## NOTE: Added delay of 2 minutes after creating log based metrics as it takes time to register for monitoring alert policy to use it

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

### x. https://cloud.google.com/logging/docs/alerting/log-based-alerts#lba-by-api

### xi. https://cloud.google.com/monitoring/alerts/doc-variables

### xii. https://stackoverflow.com/questions/59963102/stackdriver-custom-label-usage-in-email-alerts-for-metric-conditions