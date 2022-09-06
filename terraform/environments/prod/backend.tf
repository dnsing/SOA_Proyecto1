terraform {
  backend "gcs" {
    bucket = "soaproyecto1"
    prefix = "env/dev"
  }
}
