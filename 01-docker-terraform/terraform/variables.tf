variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project Name"
  default     = "US"
}

variable "location" {
  description = "Project Location"
  default     = "bionic-baton-411711"
}

variable "region" {
  description = "Region name"
  default     = "us-central1"
}

variable "zone" {
  description = "Zone name"
  default     = "us-central1-c"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_bucket_class" {
  description = "bionic-baton-411711-auto-expiring-bucket"
  default     = "STANDARD"
}