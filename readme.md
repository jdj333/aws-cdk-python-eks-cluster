# AWS CDK EKS Cluster Project

This project contains an AWS CDK stack that deploys an EKS cluster and an NGINX web application using a Helm chart. The NGINX web app is exposed via an ALB load balancer.

## Project Structure

```
cdk_project/
├── app.py
├── nginx-app/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── requirements.txt
└── .github/
    └── workflows/
        └── deploy.yml
```

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured.
- [Node.js](https://nodejs.org/) (for AWS CDK) installed.
- [Python 3.9](https://www.python.org/downloads/) installed.
- [AWS CDK](https://aws.amazon.com/cdk/) installed globally.
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed.
- [Helm](https://helm.sh/) installed.

## Setup Instructions

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name/cdk_project
    ```

2. **Install dependencies:**

    ```sh
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    npm install -g aws-cdk
    ```

3. **Bootstrap your environment (if not already done):**

    ```sh
    cdk bootstrap aws://ACCOUNT-NUMBER/REGION
    ```

## CDK Commands

1. **Synthesize the CloudFormation template:**

    ```sh
    cdk synth
    ```

2. **Deploy the stack:**

    ```sh
    cdk deploy
    ```

3. **Destroy the stack:**

    ```sh
    cdk destroy
    ```

4. **Check the diff between deployed stack and local changes:**

    ```sh
    cdk diff
    ```

## GitHub Actions Deployment

This project includes a GitHub Actions workflow for automatic deployment.

**Relative Path: `.github/workflows/deploy.yml`**

```yaml
name: Deploy EKS Cluster

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          npm install -g aws-cdk

      - name: CDK Deploy
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: 'us-west-2'
        run: cdk deploy --require-approval never
```

## Setting Up GitHub Secrets

Ensure you have the following secrets set up in your GitHub repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Useful Links

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
