variable "credentials" {
  description = "My Credentials"
  default     = "../keys/my-creds.json"
}


variable "project" {
  description = "First project on de_zoomcamp"
  default     = "dezoomcamp-412213"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "first_demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "dezoomcamp-412213-data-lake-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}