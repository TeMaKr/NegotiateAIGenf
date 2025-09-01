variable "ssh_key" {
  type      = string
  sensitive = true
}

variable "ci_registry" {
  type      = string
  sensitive = true
}

variable "ci_deploy_user" {
  type      = string
  sensitive = true
}

variable "ci_deploy_password" {
  type      = string
  sensitive = true
}

variable "ci_environment_name" {
  type = string
}


variable "bitwarden_secrets_access_token" {
  type      = string
  sensitive = true
}

variable "docker_image_orchestration_pocketbase" {
  type = string
}

variable "docker_image_orchestration_fastapi" {
  type = string
}

variable "docker_image_webapp" {
  type = string
}

variable "target_host" {
  type    = string
  default = "dev-negotiate-ai.social-data-company.de"
}
