# CI/CD Pipeline for Task Manager App

## Overview
This project powers a modern **CI/CD pipeline** utilizing **GitLab** for source code management (SCM). On every push, **Jenkins** dynamically provisions a pod within **Amazon EKS** to run the pipeline. The process begins with building a Docker image from the latest code, followed by dependency scanning to detect vulnerabilities in third-party libraries. Next, static code analysis with **SonarQube** and functional testing with **Selenium** are executed. Once the tests pass, the Docker image is published to **Amazon ECR**, then signed and verified using **Cosign**. Finally, the verified image is deployed to **Amazon EKS**, where the application connects to **Amazon RDS** for database management and **Redis** for caching. The entire infrastructure is provisioned using **Terraform** to deploy the necessary AWS resources. Additionally, **ArgoCD** running on the EKS cluster monitors GitLab for configuration changes and automatically triggers rolling updates to the application.

---

## Pipeline Workflow
1. **Code Checkout**  
   - GitLab detects a push and triggers Jenkins to pull the latest code.
2. **Image Build**  
   - A Docker image is built from the application code.
3. **Dependency Scanning**  
   - The built image is scanned for vulnerabilities in dependencies to ensure security.
4. **Static Analysis & Testing**  
   - **SonarQube** performs static code analysis to ensure code quality.  
   - **Selenium** executes functional tests to validate application behavior.
5. **Artifact Publishing & Security**  
   - The Docker image is published to **Amazon ECR**.  
   - **Cosign** signs the image and verifies its integrity.
6. **Deployment**  
   - The verified image is deployed to **Amazon EKS**.  
   - The application integrates with **Amazon RDS** for database management and **Redis** for caching.
7. **Rolling Updates with ArgoCD**  
   - **ArgoCD** monitors GitLab for configuration changes.  
   - Upon detecting updates, it performs a rolling update to ensure zero downtime.

---

## Project Structure
- **Application Repo**: Contains the source code for the Task Manager App.
- **IaC Repo**: Contains Terraform configurations for provisioning the complete infrastructure.
- **Jenkins Shared Libraries Repo**: Contains all the functions executed within the pipeline stages.

---

## Technologies Used
- **☁️ Cloud Platform: AWS**  
  - Services: EKS, ECR, RDS, EBS
- **🐳 Container Runtime: Docker**
- **☸️ Container Orchestration: Kubernetes (EKS)**
- **🏗️ Infrastructure as Code: Terraform**
- **🔐 Secret Management: HashiCorp Vault**
- **🤖 CI/CD Tools**:  
  - **Jenkins**  
  - **GitLab** (SCM)  
  - **ArgoCD** (GitOps workflow)
- **🔎 Static Code Analysis: SonarQube**
- **🧪 Functional Testing: Selenium**
- **🔏 Security Tools**:  
  - **Cosign** (Image signing and verification)
  - **Dependency Scanning** (for detecting vulnerabilities in third-party libraries)
- **🗃️ Caching**: Redis
- **🐍 Programming Language: Python**

---

## Additional Notes
- **Dynamic Pod Execution**: Jenkins dynamically creates a pod in EKS for each pipeline run, ensuring an isolated and scalable execution environment.
- **GitOps with ArgoCD**: ArgoCD continuously monitors GitLab for configuration changes and automatically initiates rolling updates to keep the deployment in sync with the source code.

