import yaml
import argparse
import os
from datetime import datetime

# pod,deploy,service,ingress,configmap,secret

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
    

if __name__ == "__main__":
    main()

