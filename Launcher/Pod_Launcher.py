from fastapi import FastAPI
from kubernetes import client, config
import uuid

app = FastAPI()

# Load kube config
config.load_kube_config()

apps_v1 = client.AppsV1Api()

@app.post("/launch-langflow/")
async def launch_langflow():
    deployment_name = f"langflow-{uuid.uuid4().hex[:5]}"
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name, labels={"app": "langflow-prod"}),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"app": "langflow-prod"}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "langflow-prod"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="langflow-prod",
                            image="langflowai/langflow",  # 🛠️ Put your image here
                            image_pull_policy="IfNotPresent",
                            ports=[client.V1ContainerPort(container_port=7860)],
                            env=[
                                client.V1EnvVar(name="LANGFLOW_BACKEND_ONLY", value="true"),
                                client.V1EnvVar(name="LANGFLOW_LOAD_FLOWS_PATH", value="/app/langflow2/flows"),
                                client.V1EnvVar(name="LANGFLOW_SUPERUSER", value="administrator"),
                                client.V1EnvVar(name="LANGFLOW_SUPERUSER_PASSWORD", value="securepassword"),
                                client.V1EnvVar(name="LANGFLOW_CONFIG_DIR", value="/app/langflow"),
                                client.V1EnvVar(name="LANGFLOW_COMPONENTS_PATH", value="/app/langflow/components"),
                                client.V1EnvVar(name="LANGFLOW_SAVE_DB_IN_CONFIG_DIR", value="false"),
                                client.V1EnvVar(name="LANGFLOW_UPDATE_STARTER_PROJECTS", value="true"),
                                client.V1EnvVar(
                                    name="LANGFLOW_DATABASE_URL",
                                    value="postgresql://admin:admin@postgres:5432/langflow-prod"
                                ),
                            ]
                        )
                    ]
                )
            )
        )
    )

    apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
    return {"status": "created", "deployment_name": deployment_name}
