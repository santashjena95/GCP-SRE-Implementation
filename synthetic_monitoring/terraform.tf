data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/synthetic/"
  output_path = "${path.module}/synthetic/synthetic.zip"
}
 
resource "google_storage_bucket_object" "function_code" {
  name   = "function-code-${filemd5(data.archive_file.function_zip.output_path)}.zip"
  bucket = "synthetic_mocha"
  source = data.archive_file.function_zip.output_path
}

resource "google_cloudfunctions_function" "function" {
  name        = "synthetic"
  project     = var.project_id
  description = "Function To Run Synthetic Monitoring"
  runtime     = "nodejs20"
  region      = "us-central1"

  available_memory_mb   = 2048
  max_instances         = 2
  source_archive_bucket = google_storage_bucket_object.function_code.bucket
  source_archive_object = google_storage_bucket_object.function_code.name
  trigger_http          = true
  ingress_settings      = "ALLOW_INTERNAL_ONLY"
  timeout               = 540
  entry_point           = "SyntheticMochaSuite"
  service_account_email = "synthetic-test@sre-project-poc.iam.gserviceaccount.com"
}

resource "google_cloud_scheduler_job" "job" {
  name        = "synthetic-scheduler-job"
  description = "Scheduler to trigger Cloud Function job"
  region      = "us-central1"
  project     = var.project_id
  schedule    = "*/5 * * * *"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.function.https_trigger_url

    oidc_token {
      service_account_email = google_cloudfunctions_function.function.service_account_email
    }
  }
}
