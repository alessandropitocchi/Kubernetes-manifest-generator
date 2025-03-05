import yaml
import argparse
import os
from datetime import datetime

# service,ingress,configmap,secret

def generate_namespace(name):
    """Generate namespace manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": name}
    }

def generate_pod(name, image, namespace):
    """Generate pod manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name},
        "spec": {
            "containers": [
                {
                    "name": name,
                    "image": image
                }   
            ]
        }
    }

def generate_deployment(name, image, replicas, namespace):
    """Generate deployment manifest"""
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {"app": name}
            },
            "template": {
                "metadata": {
                    "labels": {"app": name}
                },
                "spec": {
                    "containers": [
                        {
                            "name": name,
                            "image": image
                        }
                    ]
                }
            }
        }
    }

def generate_service(name, port, target_port, namespace):
    """Generate service manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "ports": [
                {"port": port, "targetPort": target_port}
            ],
            "selector": {"app": name}
        }
    }
    
def save_manifest(resource, output_dir, resource_type, name):
    """Save the manifest file"""
    output_dir = output_dir or "."  # Usa la directory corrente se None
    os.makedirs(output_dir, exist_ok=True)  # Crea la directory se non esiste

    filename = os.path.join(output_dir, f"{resource_type}-{name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml")

    with open(filename, "w") as f:
        yaml.dump(resource, f, default_flow_style=False)

    print(f"Manifest file saved to {filename}")
    return filename

def main():
    parser = argparse.ArgumentParser(
        description="Generate Kubernetes manifest files"
    )

    # Argomento globale --output
    parser.add_argument("--output", type=str, default=".", help="Specify the output directory for YAML files")

    subparsers = parser.add_subparsers(dest="resource", required=True, help="Available resources to generate")

    # Namespace command
    ns_parser = subparsers.add_parser("namespace", help="Generate a Kubernetes Namespace manifest", description="Creates a YAML file for a Kubernetes Namespace")
    ns_parser.add_argument("--name", type=str, required=True, help="Specify the namespace name")

    # Pod command
    pod_parser = subparsers.add_parser("pod", help="Generate a Kubernetes Pod manifest", description="Creates a YAML file for a Kubernetes POd")
    pod_parser.add_argument("--name", type=str, required=True, help="Specify the pod name")
    pod_parser.add_argument("--image", type=str, required=True, help="Specify the image")
    pod_parser.add_argument("--namespace", type=str, default="default", required=True, help="Specify the namespace name")

    # Deployment command
    deploy_parser = subparsers.add_parser("deployment", help="Generate a Kubernetes Deployment manifest", description="Creates a YAML file for a Kubernetes Deployment")
    deploy_parser.add_argument("--name", type=str, required=True, help="Specify the deployment name")
    deploy_parser.add_argument("--image", type=str, required=True, help="Specify the image")
    deploy_parser.add_argument("--replicas", type=int, default=1, help="Specify the number of replicas")
    deploy_parser.add_argument("--namespace", type=str, default="default", required=True, help="Specify the namespace name")

    # Service command
    service_parser = subparsers.add_parser("service", help="Generate a Kubernetes Service manifest", description="Creates a YAML file for a Kubernetes Service")
    service_parser.add_argument("--name", type=str, required=True, help="Specify the service name")
    service_parser.add_argument("--port", type=int, required=True, help="Specify the service port")
    service_parser.add_argument("--target-port", type=int, help="Specify the target port")
    service_parser.add_argument("--namespace", type=str, default="default", required=True, help="Specify the namespace name")

    # Se non ci sono argomenti, mostra l'help automaticamente
    import sys
    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    if args.resource == "namespace":
        resource = generate_namespace(args.name)
        save_manifest(resource, args.output, "namespace", args.name)
    elif args.resource == "pod":
        resource = generate_pod(args.name, args.image, args.namespace)
        save_manifest(resource, args.output, "pod", args.name)
    elif args.resource == "deployment":
        resource = generate_deployment(args.name, args.image, args.replicas, args.namespace)
        save_manifest(resource, args.output, "deployment", args.name)
    elif args.resource == "service":
        resource = generate_service(args.name, args.port, args.target_port, args.namespace)
        save_manifest(resource, args.output, "service", args.name)
    
if __name__ == "__main__":
    main()

