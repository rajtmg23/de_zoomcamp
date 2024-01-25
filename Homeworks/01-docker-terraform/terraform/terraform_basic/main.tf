terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = "../keys/my-creds.json"
  project = "dezoomcamp-412213"
  region  = "us-central1"
}

resource "google_storage_bucket" "data-lake-bucket" {
  name     = "dezoomcamp-412213-data-lake-bucket"
  location = "US"

  # Optional, but recommended settings:
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "my_bigquery_dataset" {
  dataset_id = "dezoomcamp-412213-my_bigquery_dataset"
  project    = "dezoomcamp-412213"
  location   = "US"
}