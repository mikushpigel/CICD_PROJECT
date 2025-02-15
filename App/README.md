# Task Manager CI/CD Pipeline: 1.0.21

This project powers a modern **CI/CD pipeline** for a **Task Manager App** built in **Python**. It drives seamless continuous integration and deployment using **Jenkins**, **Docker**, **Amazon ECR**, and **ArgoCD**. The pipeline ensures an efficient, seamless, and reliable process for managing updates and releases. The entire project infrastructure is provisioned with **Terraform** for consistent and repeatable deployments, and all services run on **Amazon EKS**.

---

## Project Structure
This project is organized into three distinct repositories:
- **Application Repo**: Contains the source code for the Task Manager App.
- **IaC Repo**: Holds all Terraform configurations for provisioning the complete infrastructure.
- **Jenkins Shared Libraries Repo**: Contains shared libraries and plugins (including the Jenkins Kubernetes Plugin) used across Jenkins jobs.

All sensitive information (such as secrets and credentials) is securely stored in **Vault**.

---

## Features
- **Automated Build and Test**: Automatically builds and tests code upon each push.
- **Static Code Analysis**: Ensures high-quality code using **SonarQube**.
- **Functional Testing**: Validates application functionality using **Selenium**.
- **Artifact Publishing**: Stores build artifacts in **Amazon ECR**.
- **Kubernetes Deployment**: Deploys the application to **Amazon EKS** clusters using **ArgoCD**.
- **Caching and Database Management**: Uses **Redis** for caching and **Amazon RDS** for database management.
- **Jenkins Kubernetes Plugin**: Enhances integration with Kubernetes.
- **Slack Notifications**: Sends pipeline status updates to **Slack**.

---

## Prerequisites
Before running this pipeline, ensure the following components are installed and configured:

- **Jenkins**: Configured with the following plugins:
  - Docker
  - Amazon EC2
  - Cloud Agent
  - Slack
  - Git
  - Kubernetes
- **Docker**: For containerizing the application.
- **Amazon ECR**: For storing Docker images as build artifacts.
- **Amazon EKS**: For deploying the application.
- **ArgoCD**: For managing Kubernetes deployments.
- **Terraform**: For provisioning the entire project infrastructure.
- **Vault**: For securely managing sensitive information.
- **SonarQube**: For static code analysis.
- **Selenium**: For functional testing.
- **Slack**: For receiving notifications on pipeline status.

---

## Pipeline Workflow
The CI/CD pipeline performs the following steps:

1. **Code Checkout**: Jenkins retrieves the latest code from the repository.
2. **Static Analysis**: SonarQube performs static analysis to maintain code quality.
3. **Build**: Compiles the application code and creates a Docker image.
4. **Testing**: Executes Selenium tests to validate the application's functionality.
5. **Artifact Publishing**: Pushes the Docker image to **Amazon ECR** for storage.
6. **Deployment**: Deploys the application to **Amazon EKS** using **ArgoCD**.
7. **Notifications**: Sends Slack notifications regarding the pipeline's progress and results.

---

## Technologies Used
This project leverages a range of modern technologies:

- **Jenkins**: For CI/CD automation.
- **Docker**: To containerize the application.
- **Amazon ECR**: For storing Docker images.
- **Amazon EKS**: For Kubernetes-based deployments.
- **ArgoCD**: For GitOps-based Kubernetes deployment.
- **Terraform**: For provisioning the entire project infrastructure.
- **Vault**: For secure storage of sensitive information.
- **SonarQube**: For static code analysis.
- **Selenium**: For functional testing.
- **Redis**: For caching.
- **Amazon RDS**: For database management.
- **Slack**: For sending pipeline status notifications.
- **Jenkins Kubernetes Plugin**: For enhanced Kubernetes integration.