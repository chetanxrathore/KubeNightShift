from kubernetes import client, config
import os

SCALE_TO = int(os.getenv('SCALE_TO', 0))

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    namespaces = [
        ns.metadata.name for ns in v1.list_namespace().items
        if ns.metadata.name not in ['kube-system', 'kube-public', 'kube-node-lease']
    ]

    for ns in namespaces:
        deployments = apps_v1.list_namespaced_deployment(ns).items
        for deploy in deployments:
            name = deploy.metadata.name

            if SCALE_TO == 0:
                # Store original replica count in annotation before scaling down
                original_replicas = deploy.spec.replicas or 1
                patch_body = {
                    "metadata": {
                        "annotations": {
                            "original_replicas": str(original_replicas)
                        }
                    },
                    "spec": {"replicas": SCALE_TO}
                }
                print(f"Scaling down '{name}' in '{ns}' from {original_replicas} to {SCALE_TO}")
            else:
                # Retrieve original replica count from annotation during scale-up
                annotations = deploy.metadata.annotations or {}
                original_replicas = int(annotations.get("original_replicas", "1"))
                patch_body = {
                    "metadata": {
                        "annotations": {
                            "original_replicas": None  # Remove annotation after restoring
                        }
                    },
                    "spec": {"replicas": original_replicas}
                }
                print(f"Scaling up '{name}' in '{ns}' back to {original_replicas}")

            # Patch the deployment directly (not the scale subresource!)
            apps_v1.patch_namespaced_deployment(name, ns, patch_body)

if __name__ == "__main__":
    main()
