from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

api_client = client.ApiClient()

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="994857209012.dkr.ecr.us-east-1.amazonaws.com/my_cloud_monitoring_app_image:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

try:
    api_instance = client.AppsV1Api(api_client)
    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    print("Deployment created.")
except client.exceptions.ApiException as e:
    if e.status == 409 and "AlreadyExists" in e.body:
        print("Deployment already exists. Updating or deleting existing deployment.")
        # Implement your update or delete logic here
    else:
        print(f"An error occurred while creating deployment: {e}")


service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)


try:
    api_instance = client.CoreV1Api(api_client)
    api_instance.create_namespaced_service(
        namespace="default",
        body=service
    )
    print("Service created.")
except client.exceptions.ApiException as e:
    if e.status == 409 and "AlreadyExists" in e.body:
        print("Service already exists. Updating or deleting existing service.")
        # Implement your update or delete logic here
    else:
        print(f"An error occurred while creating service: {e}")
