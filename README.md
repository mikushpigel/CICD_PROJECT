# Weather App CI/CD Pipeline:1.0.17

## About the Project
This project automates the process of building, testing, and deploying a **Weather App** written in **Python**. The pipeline uses tools like **Jenkins**, **Docker**, and **Amazon EKS** to make the process faster, more reliable, and easier to manage.

---

## What the Pipeline Does
- **Automatic Builds and Tests**: Runs builds and tests every time new code is pushed to the repository.
- **Code Quality Check**: Uses **SonarQube** to ensure the code is clean and follows best practices.
- **Full Application Testing**: Tests how the app works using **Selenium**.
- **Stores Ready-to-Use Images**: Saves Docker images of the app in **DockerHub**.
- **Deploys to Kubernetes**: Deploys the app to **Amazon EKS** using a **Rolling Update** to avoid downtime.
- **Pipeline Notifications**: Sends updates about the pipeline's progress directly to **Slack**.

---

## What You Need
To use this pipeline, make sure you have:
- **Jenkins**: Installed and ready, with plugins for Docker, Git, EC2 agents, and Slack.
- **Docker**: To package the app into a container.
- **SonarQube**: To check and improve code quality.
- **Selenium**: To test how the app works.
- **Amazon EKS**: For deploying the app in a Kubernetes cluster.
- **DockerHub**: To store the Docker images.
- **Slack**: To get notifications about the pipeline.

---

## How It Works
1. **Fetch the Code**: Jenkins downloads the latest code from the repository.
2. **Check Code Quality**: SonarQube analyzes the code and checks for any issues.
3. **Build the App**: Creates a Docker image for the app.
4. **Test the App**:
   - Runs **unit tests** to make sure the code works as expected.
   - Runs **Selenium tests** to check the app's user interface.
5. **Store the Image**: Uploads the Docker image to DockerHub.
6. **Deploy the App**: Deploys the app to **Amazon EKS** using a Rolling Update to ensure no downtime.
7. **Send Notifications**: Updates are sent to Slack about the status of the pipeline.

---

## Tools Used
- **Jenkins**: To automate the pipeline.
- **Docker**: To create and run containers.
- **SonarQube**: To check code quality.
- **Selenium**: To test the app.
- **Slack**: For pipeline updates.
- **DockerHub**: To save the app images.
- **Amazon EKS**: To deploy the app in the cloud.
