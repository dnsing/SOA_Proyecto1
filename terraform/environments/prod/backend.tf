terraform {
  backend "gcs" {
    bucket = "soaproyecto1-tfstate"
    prefix = "env/dev"
  }
}
