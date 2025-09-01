terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

locals {
  target_host = yamldecode(file("${path.module}/environments/${var.ci_environment_name}.yaml")).target_host
  caddy       = yamldecode(file("${path.module}/environments/${var.ci_environment_name}.yaml")).caddy
}

provider "docker" {
  host     = "ssh://deploy@${local.target_host}:22"
  ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]

  registry_auth {
    address  = var.ci_registry
    username = var.ci_deploy_user
    password = var.ci_deploy_password
  }
}

resource "docker_network" "network" {
  name = "${var.ci_environment_name}_negotiate_ai_network"
}

resource "docker_image" "orchestration_fastapi" {
  name = var.docker_image_orchestration_fastapi
}

resource "docker_image" "orchestration_pocketbase" {
  name = var.docker_image_orchestration_pocketbase
}

resource "docker_container" "orchestration_pocketbase" {
  image   = docker_image.orchestration_pocketbase.image_id
  name    = "${var.ci_environment_name}_negotiate_ai_orchestration_pocketbase"
  restart = "unless-stopped"

  command = [
    "sh",
    "-c",
    "export BWS_ACCESS_TOKEN=$BWS_ACCESS_TOKEN && bws run --server-url https://vault.bitwarden.eu -- /pb/pocketbase serve --http=0.0.0.0:8080"
  ]

  env = [
    "BWS_ACCESS_TOKEN=${var.bitwarden_secrets_access_token}",
  ]

  volumes {
    host_path      = "/home/deploy/dev_negotiate_ai/pb_data"
    container_path = "/pb/pb_data"
  }
  ports {
    internal = 8080
  }


  networks_advanced {
    name = docker_network.network.name
  }
}

resource "docker_container" "scripts" {
  image = docker_image.orchestration_fastapi.image_id
  name  = "${var.ci_environment_name}_negotiate_ai_scripts"
  command = [
    "sh",
    "-c",
    "export BWS_ACCESS_TOKEN=$BWS_ACCESS_TOKEN && bws run --server-url https://vault.bitwarden.eu -- python -m scripts"
  ]

  env = [
    "BWS_ACCESS_TOKEN=${var.bitwarden_secrets_access_token}",
  ]

  restart = "no"
  rm      = true

  networks_advanced {
    name = docker_network.network.name
  }
}


resource "docker_container" "redis" {
  image   = "redis:7"
  name    = "${var.ci_environment_name}_negotiate_ai_redis"
  restart = "unless-stopped"
  command = [
    "redis-server",
  ]


  networks_advanced {
    name    = docker_network.network.name
    aliases = ["redis"]
  }
}

resource "docker_container" "worker" {
  image   = docker_image.orchestration_fastapi.image_id
  name    = "${var.ci_environment_name}_negotiate_ai_worker"
  restart = "unless-stopped"
  command = [
    "sh",
    "-c",
    "export BWS_ACCESS_TOKEN=$BWS_ACCESS_TOKEN && bws run --server-url https://vault.bitwarden.eu -- celery --app=worker worker --loglevel=INFO --concurrency=4 --queues default --pool=threads"
  ]

  env = [
    "BWS_ACCESS_TOKEN=${var.bitwarden_secrets_access_token}",
  ]


  networks_advanced {
    name = docker_network.network.name
  }
}


resource "docker_container" "orchestration_fastapi" {
  image   = docker_image.orchestration_fastapi.image_id
  name    = "${var.ci_environment_name}_negotiate_ai_orchestration_fastapi"
  restart = "unless-stopped"
  command = [
    "sh",
    "-c",
    "export BWS_ACCESS_TOKEN=$BWS_ACCESS_TOKEN && bws run --server-url https://vault.bitwarden.eu -- uvicorn api:app --workers=1 --host '0.0.0.0' --port '8000' --access-log"
  ]

  env = [
    "BWS_ACCESS_TOKEN=${var.bitwarden_secrets_access_token}",
  ]

  ports {
    internal = 8000
  }

  networks_advanced {
    name = docker_network.network.name
  }
}

resource "docker_image" "webapp" {
  name = var.docker_image_webapp
}

resource "docker_container" "webapp" {
  image   = docker_image.webapp.image_id
  name    = "${var.ci_environment_name}_negotiate_ai_webapp"
  restart = "unless-stopped"

  ports {
    internal = 80
  }
}


resource "local_file" "caddyfile" {
  content = templatefile("./Caddyfile.tftpl", {
    primary_host                         = local.caddy.primary_host,
    redirect_hosts                       = local.caddy.redirect_hosts,
    docker_port_webapp                   = docker_container.webapp.ports[0].external,
    docker_port_orchestration_pocketbase = docker_container.orchestration_pocketbase.ports[0].external,
    docker_port_orchestration_fastapi    = docker_container.orchestration_fastapi.ports[0].external,
    basic_auth                           = local.caddy.basic_auth
  })
  filename = "./Caddyfile"
}

resource "null_resource" "caddyfile_template" {
  triggers = {
    "docker_port_webapp"                   = docker_container.webapp.ports[0].external
    "docker_port_orchestration_pocketbase" = docker_container.orchestration_pocketbase.ports[0].external
    "docker_port_orchestration_fastapi"    = docker_container.orchestration_fastapi.ports[0].external
  }

  provisioner "file" {
    source      = local_file.caddyfile.filename
    destination = "/etc/caddy/caddy.d/${local.target_host}.conf"
  }

  provisioner "remote-exec" {
    inline = ["sudo systemctl reload caddy"]
  }

  connection {
    type = "ssh"
    user = "deploy"
    host = local.target_host
  }
}
