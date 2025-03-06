import sys
import os

# Aggiungi il percorso della root del progetto per permettere l'import del modulo
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from kubernetes_manifest_generator import (
    generate_namespace,
    generate_pod,
    generate_deployment,
    generate_service,
    generate_configmap,
    generate_secret,
    generate_ingress,
    save_manifest,
)
import yaml


# Test per la generazione del namespace
def test_generate_namespace():
    ns = generate_namespace("test-namespace")
    assert ns["apiVersion"] == "v1"
    assert ns["kind"] == "Namespace"
    assert ns["metadata"]["name"] == "test-namespace"


# Test per la generazione di un pod
def test_generate_pod():
    pod = generate_pod("test-pod", "nginx:latest", "default")
    assert pod["apiVersion"] == "v1"
    assert pod["kind"] == "Pod"
    assert pod["metadata"]["name"] == "test-pod"
    assert pod["spec"]["containers"][0]["name"] == "test-pod"
    assert pod["spec"]["containers"][0]["image"] == "nginx:latest"


# Test per la generazione di un deployment
def test_generate_deployment():
    deployment = generate_deployment(
        "test-deploy", "nginx:latest", 3, "default"
    )
    assert deployment["apiVersion"] == "apps/v1"
    assert deployment["kind"] == "Deployment"
    assert deployment["metadata"]["name"] == "test-deploy"
    assert deployment["spec"]["replicas"] == 3
    assert (
        deployment["spec"]["template"]["metadata"]["labels"]["app"]
        == "test-deploy"
    )


# Test per la generazione di un service
def test_generate_service():
    service = generate_service("test-service", 80, 8080, "default")
    assert service["apiVersion"] == "v1"
    assert service["kind"] == "Service"
    assert service["metadata"]["name"] == "test-service"
    assert service["spec"]["ports"][0]["port"] == 80
    assert service["spec"]["ports"][0]["targetPort"] == 8080


# Test per la generazione di un configmap
def test_generate_configmap():
    data = {"config_key": "config_value"}
    configmap = generate_configmap("test-configmap", data, "default")
    assert configmap["apiVersion"] == "v1"
    assert configmap["kind"] == "ConfigMap"
    assert configmap["metadata"]["name"] == "test-configmap"
    assert configmap["data"]["config_key"] == "config_value"


# Test per la generazione di un secret
def test_generate_secret():
    data = {"password": "cGFzc3dvcmQ="}  # Base64 encoding of "password"
    secret = generate_secret("test-secret", data, "default")
    assert secret["apiVersion"] == "v1"
    assert secret["kind"] == "Secret"
    assert secret["metadata"]["name"] == "test-secret"
    assert secret["data"]["password"] == "cGFzc3dvcmQ="


# Test per la generazione di un Ingress
def test_generate_ingress():
    ingress = generate_ingress(
        "test-ingress", "default", "example.com", "/", "test-service", 80
    )
    assert ingress["apiVersion"] == "networking.k8s.io/v1"
    assert ingress["kind"] == "Ingress"
    assert ingress["metadata"]["name"] == "test-ingress"
    assert ingress["spec"]["rules"][0]["host"] == "example.com"
    assert (
        ingress["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"][
            "name"
        ]
        == "test-service"
    )


# Test per il salvataggio del manifest
def test_save_manifest(tmpdir):
    manifest_data = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": "test-pod"},
    }
    filename = save_manifest(manifest_data, tmpdir, "pod", "test-pod")

    # Verifica che il file sia stato creato
    assert os.path.exists(filename)

    # Verifica che il contenuto sia corretto
    with open(filename, "r") as f:
        loaded_data = yaml.safe_load(f)
        assert loaded_data == manifest_data
