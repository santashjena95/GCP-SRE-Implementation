# This repo deploys cloud run using terraform with opentelemetry as sidecar container

## 1. Go to GCP artifact registry and create repository.

## 2. Then run the github action pipeline for building and pushing the docker image to Google Artifact Registry.

## 3. Then it will automatically trigger the cloud run terraform module for the deploying cloud run with the image pushed to google artifact registry