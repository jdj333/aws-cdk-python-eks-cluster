#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import aws_eks as eks
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2

class EksClusterStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Define an EKS Cluster
        cluster = eks.Cluster(self, "MyCluster",
            vpc=vpc,
            default_capacity=2,
            masters_role=iam.Role(self, "AdminRole",
                assumed_by=iam.AccountRootPrincipal()
            )
        )

        # Apply the Helm Chart for NGINX Ingress Controller
        cluster.add_helm_chart("nginx-ingress",
            chart="nginx-ingress",
            repository="https://kubernetes.github.io/ingress-nginx",
            namespace="kube-system"
        )

        # Deploy an NGINX web app with a Helm chart
        cluster.add_helm_chart("nginx-app",
            chart="nginx",
            repository="https://charts.bitnami.com/bitnami",
            namespace="default",
            values={
                "service": {
                    "type": "LoadBalancer"
                }
            }
        )

app = cdk.App()
EksClusterStack(app, "EksClusterStack")
app.synth()
