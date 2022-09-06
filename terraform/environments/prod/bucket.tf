resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_id}-function-test"
    location = var.region
}

resource "google_storage_bucket" "input_bucket" {
    name     = "${var.project_id}-input-test"
    location = var.region
}