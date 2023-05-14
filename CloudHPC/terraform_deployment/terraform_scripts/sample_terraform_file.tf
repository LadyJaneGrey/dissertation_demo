# resource "google_service_account" "default" {
#   account_id   = "service-account-id"
#   display_name = "Service Account"
# }

resource "google_container_cluster" "primary" {
  name     = "ron-tf-gke-cluster"
  location = "us-central1"
  node_locations = ["us-central1-a"]

  project = "platinum-chain-308019"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary" {
  name       = "my-node-pool"
  location = "us-central1"
  node_locations = ["us-central1-a"]

  project = "platinum-chain-308019"

  cluster    = google_container_cluster.primary.name
#   preemptible = false
  node_count = var.numNodes

  node_config {
    machine_type = "e2-standard-8"
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    # service_account = google_service_account.default.email
    advanced_machine_features {
        threads_per_core = 1
      
    }
    
    
    labels = {
      "num_threads" = "1"
    }
    
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}