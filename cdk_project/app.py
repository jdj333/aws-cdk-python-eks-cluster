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

        # Apply the Helm Chart for ALB Ingress Controller
        cluster.add_helm_chart("alb-ingress-controller",
            chart="aws-load-balancer-controller",
            repository="https://aws.github.io/eks-charts",
            namespace="kube-system",
            values={
                "clusterName": cluster.cluster_name,
                "serviceAccount.create": False,
                "serviceAccount.name": "aws-load-balancer-controller"
            }
        )

        # Create the service account for ALB Ingress Controller
        alb_sa = cluster.add_service_account("aws-load-balancer-controller",
            name="aws-load-balancer-controller",
            namespace="kube-system"
        )

        alb_sa.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_ALB_Ingress_Controller"))
        alb_sa.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSClusterPolicy"))

        # Deploy an NGINX web app with a Helm chart
        cluster.add_helm_chart("nginx-app",
            chart="nginx-app",
            repository=".",
            namespace="default",
            values={
                "service": {
                    "type": "ClusterIP"
                },
                "ingress": {
                    "enabled": True,
                    "annotations": {
                        "kubernetes.io/ingress.class": "alb",
                        "alb.ingress.kubernetes.io/scheme": "internet-facing"
                    },
                    "hosts": [
                        {
                            "host": "your-domain.com",
                            "paths": ["/"]
                        }
                    ]
                }
            }
        )

app = cdk.App()
EksClusterStack(app, "EksClusterStack")
app.synth()
