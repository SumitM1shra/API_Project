from fastapi import FastAPI
from kubernetes import client, config
from prometheus_api_client import PrometheusConnect

app = FastAPI()

config.load_kube_config()

@app.post("/createDeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    apps_v1 = client.AppsV1Api()
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector={'matchLabels': {'app': deployment_name}},
            template=client.V1PodTemplateSpec(
                metadata={'labels': {'app': deployment_name}},
                spec=client.V1PodSpec(containers=[client.V1Container(
                    name=deployment_name,
                    image="nginx:latest",
                    ports=[client.V1ContainerPort(container_port=80)],
                )])
            )
        )
    )
    apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
    return {"message": f"Deployment {deployment_name} created"}

@app.get("/getPromdetails")
async def get_prom_details():
    prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
    return prom.all_metrics()
