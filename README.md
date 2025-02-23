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

```mermaid
%% קובץ Mermaid של Task Manager Architecture %%
flowchart LR
  subgraph EKS["EKS Cluster"]
    direction TB
      DynamicAgent(["Dynamic Agent"])
      ArgoCD(["ArgoCD"])
      TaskManager(["Tasks Manager App"])
      Vault(["Vault"])
      Redis(["Redis"])
  end
  subgraph Private_Subnet["Private Subnet"]
    direction TB
      GitLab["GitLab Server (Container)"]
      Jenkins["Jenkins Server (Container)"]
      Sonar["Sonar (Container)"]
      EKS
  end
  subgraph Public_Subnet["Public Subnet"]
    direction TB
      ALB(("Application Load Balancer"))
  end
  subgraph AWS_VPC["AWS VPC"]
    direction LR
      Private_Subnet
      Public_Subnet
  end
  subgraph AWS["AWS"]
    direction LR
      AmazonECR["Amazon ECR"]
      AmazonRDS["Amazon RDS"]
      AmazonEBS["Amazon EBS"]
      AWS_VPC
  end
  GitLab -- Webhook --> Jenkins
  Jenkins -- Create --> DynamicAgent
  DynamicAgent -- Code Analysis --> Sonar
  DynamicAgent -- Push Image --> AmazonECR
  AmazonECR -- Update Deployment --> TaskManager
  Vault -- Use Credentials --> DynamicAgent & ArgoCD
  Vault -- Save Credentials --> AmazonEBS
  ArgoCD -- Deploy --> TaskManager
  ALB -- Route Traffic --> TaskManager
  TaskManager -- Caching --> Redis
  TaskManager -- Pull Data And Update Redis --> AmazonRDS
  style DynamicAgent fill:#F48FB1,stroke:#AD1457,color:#000000,stroke-width:1px
  style ArgoCD fill:#F48FB1,stroke:#AD1457,color:#000000,stroke-width:1px
  style TaskManager fill:#F48FB1,stroke:#AD1457,color:#000000,stroke-width:1px
  style Vault fill:#F48FB1,stroke:#AD1457,color:#000000,stroke-width:1px
  style Redis fill:#F48FB1,stroke:#AD1457,color:#000000,stroke-width:1px
  style GitLab fill:#F3E5F5,stroke:#9C27B0,color:#000000,stroke-width:1px
  style Jenkins fill:#F3E5F5,stroke:#9C27B0,color:#000000,stroke-width:1px
  style Sonar fill:#F3E5F5,stroke:#9C27B0,color:#000000,stroke-width:1px
  style EKS fill:#E1BEE7,stroke:#8E24AA,color:#000000,stroke-width:1px
  style ALB fill:#FCE4EC,stroke:#C2185B,color:#000000,stroke-width:1px
  style Private_Subnet fill:#FFF8E1,stroke:#FBC02D,color:#000000,stroke-width:1px
  style Public_Subnet fill:#FFF3E0,stroke:#FFB300,color:#000000,stroke-width:1px
  style AmazonECR fill:#FFF9C4,stroke:#FBC02D,color:#000000,stroke-width:1px
  style AmazonRDS fill:#FFF9C4,stroke:#FBC02D,color:#000000,stroke-width:1px
  style AmazonEBS fill:#FFF9C4,stroke:#FBC02D,color:#000000,stroke-width:1px
  style AWS_VPC fill:#FCE4EC,stroke:#EC407A,color:#000000,stroke-width:2px
  style AWS fill:#F3E5F5,stroke:#9C27B0,color:#000000,stroke-width:2px


