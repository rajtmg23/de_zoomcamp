## TERRAFORM

### Installing terraform on linux
https://developer.hashicorp.com/terraform/install

[More details](https://phoenixnap.com/kb/how-to-install-terraform#:~:text=How%20to%20Install%20Terraform%20on%20Windows%201%20Download,check%20the%20Terraform%20global%20path%20configuration%3A%201.%20)

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

```
To use terraform in a cloud firstly we need to create a service account from the `IAM & Admin` menu. Define the role needed for the account.

If any roles needs to be added after creating account then go to the `IAM` menu select the menu account and click on `Edit principal`.

### On this `de_zoomcamp` we are dealing with Bigquery, Storage & Compute Enginer(VM)

So we are gonna create a service account with roles as `BigQuery Admin`, `Compute Admin` & `Storage Admin`.

Now we are gonna need a key for a service account. 
* Click on `Service Accounts` menu. 
* Select the account. From the `Actions` option and click on `Manage Keys`.
* Click on `Add KEY` button.
* Click on `Create new key`.
* Choose the `JSON` option and click on `CREATE`.

_You are given the credentials needed for working with cloud. Save it in a safe place._

**Install `terraform` extension in the vs code editor. This is very helpful working with `tf` files.**

Here we can find the 
[Terraform Google Provider Docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

**Example Usage**
* A typical provider configuration will look something like:
```terraform
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options
}
```
Use the following command to correctly format the codes inside the `tf` files.
```terraform
terraform fmt
```
Get the project id from the google cloud and provide in the `main.tf` file.

Now we gonna give the credentials to connect to the cloud. This can be done in several ways.
* We can hardcore the creds file path which is not the best practice.
```terraform
provider "google" {
  credentials = "./keys/my-creds.json"
  project = "my-project-id"
  region  = "us-central1"
}
```
* The next method would be defining the creds file in the env variable. Define the following thing in bash.
```bash
export GOOGLE_CREDENTIALS='/home/user/terraform/keys/my-creds.json'

# Check the variables.
echo $GOOGLE_CREDENTIALS
```
Now run the command `terraform init` on the console.

_Now we are ready to perform terraform actions on cloud._

**Example Usage - Life cycle settings for storage bucket objects**
```terraform
resource "google_storage_bucket" "auto-expire" {
  name          = "auto-expiring-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
```
### **Note:** _Bucket name should be uniqe all over the world._

