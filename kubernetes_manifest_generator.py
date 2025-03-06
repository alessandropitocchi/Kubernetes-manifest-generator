import yaml
import argparse
import os
from datetime import datetime


def generate_namespace(name):
    """Generate namespace manifest"""
    return {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": name}}


def generate_pod(name, image, namespace):
    """Generate pod manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name},
        "spec": {"containers": [{"name": name, "image": image}]},
    }


def generate_deployment(name, image, replicas, namespace):
    """Generate deployment manifest"""
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {"containers": [{"name": name, "image": image}]},
            },
        },
    }


def generate_service(name, port, target_port, namespace):
    """Generate service manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "ports": [{"port": port, "targetPort": target_port}],
            "selector": {"app": name},
        },
    }


def generate_configmap(name, data, namespace):
    """Generate configmap manifest"""
    return {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": name, "namespace": namespace},
        "data": data,
    }


def generate_secret(name, data, namespace):
    """Generate secret manifest"""
    return {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {"name": name, "namespace": namespace},
        "data": data,
    }


def generate_ingress(name, namespace, host, path, service_name, service_port):
    """Generate ingress manifest"""
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "rules": [
                {
                    "host": host,
                    "http": {
                        "paths": [
                            {
                                "path": path,
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": service_name,
                                        "port": {"number": service_port},
                                    }
                                },
                            }
                        ]
                    },
                }
            ]
        },
    }


def save_manifest(resource, output_dir, resource_type, name):
    """Save the manifest file"""
    output_dir = output_dir or "."
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(
        output_dir,
        f"{resource_type}-{name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml",
    )

    with open(filename, "w") as f:
        yaml.dump(resource, f, default_flow_style=False)

    print(f"Manifest file saved to {filename}")
    return filename


def main():
    """CLI for generating Kubernetes manifest files"""
    parser = argparse.ArgumentParser(description="Generate Kubernetes manifest files")

    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Specify the output directory for YAML files",
    )

    subparsers = parser.add_subparsers(dest="resource", required=True)

    ns_parser = subparsers.add_parser(
        "namespace", help="Generate a Kubernetes Namespace manifest"
    )
    ns_parser.add_argument(
        "--name", type=str, required=True, help="Specify the namespace name"
    )

    pod_parser = subparsers.add_parser("pod", help="Generate a Kubernetes Pod manifest")
    pod_parser.add_argument(
        "--name", type=str, required=True, help="Specify the pod name"
    )
    pod_parser.add_argument(
        "--image", type=str, required=True, help="Specify the image"
    )
    pod_parser.add_argument(
        "--namespace", type=str, default="default", help="Specify the namespace name"
    )

    deploy_parser = subparsers.add_parser(
        "deployment", help="Generate a Kubernetes Deployment manifest"
    )
    deploy_parser.add_argument(
        "--name", type=str, required=True, help="Specify the deployment name"
    )
    deploy_parser.add_argument(
        "--image", type=str, required=True, help="Specify the image"
    )
    deploy_parser.add_argument(
        "--replicas", type=int, default=1, help="Specify the number of replicas"
    )
    deploy_parser.add_argument(
        "--namespace", type=str, required=True, help="Specify the namespace name"
    )

    service_parser = subparsers.add_parser(
        "service", help="Generate a Kubernetes Service manifest"
    )
    service_parser.add_argument(
        "--name", type=str, required=True, help="Specify the service name"
    )
    service_parser.add_argument(
        "--port", type=int, required=True, help="Specify the service port"
    )
    service_parser.add_argument(
        "--target-port", type=int, help="Specify the target port"
    )
    service_parser.add_argument(
        "--namespace", type=str, required=True, help="Specify the namespace name"
    )

    configmap_parser = subparsers.add_parser(
        "configmap", help="Generate a Kubernetes ConfigMap manifest"
    )
    configmap_parser.add_argument(
        "--name", type=str, required=True, help="Specify the configmap name"
    )
    configmap_parser.add_argument(
        "--data", type=str, required=True, help="Specify the data"
    )
    configmap_parser.add_argument(
        "--namespace", type=str, help="Specify the namespace name"
    )

    secret_parser = subparsers.add_parser(
        "secret", help="Generate a Kubernetes Secret manifest"
    )
    secret_parser.add_argument(
        "--name", type=str, required=True, help="Specify the secret name"
    )
    secret_parser.add_argument(
        "--data", type=str, required=True, help="Specify the data"
    )
    secret_parser.add_argument(
        "--namespace", type=str, help="Specify the namespace name"
    )

    ingress_parser = subparsers.add_parser(
        "ingress", help="Generate a Kubernetes Ingress manifest"
    )
    ingress_parser.add_argument(
        "--name", type=str, required=True, help="Specify the ingress name"
    )
    ingress_parser.add_argument(
        "--namespace", type=str, help="Specify the namespace name"
    )
    ingress_parser.add_argument(
        "--host", type=str, required=True, help="Specify the host"
    )
    ingress_parser.add_argument(
        "--path", type=str, required=True, help="Specify the path"
    )
    ingress_parser.add_argument(
        "--service-name", type=str, required=True, help="Specify the service name"
    )
    ingress_parser.add_argument(
        "--service-port", type=int, required=True, help="Specify the service port"
    )

    import sys

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    if args.resource == "namespace":
        resource = generate_namespace(args.name)
    elif args.resource == "pod":
        resource = generate_pod(args.name, args.image, args.namespace)
    elif args.resource == "deployment":
        resource = generate_deployment(
            args.name, args.image, args.replicas, args.namespace
        )
    elif args.resource == "service":
        resource = generate_service(
            args.name, args.port, args.target_port, args.namespace
        )
    elif args.resource == "configmap":
        resource = generate_configmap(
            args.name, yaml.safe_load(args.data), args.namespace
        )
    elif args.resource == "secret":
        resource = generate_secret(args.name, yaml.safe_load(args.data), args.namespace)
    elif args.resource == "ingress":
        resource = generate_ingress(
            args.name,
            args.namespace,
            args.host,
            args.path,
            args.service_name,
            args.service_port,
        )

    save_manifest(resource, args.output, args.resource, args.name)


if __name__ == "__main__":
    main()
