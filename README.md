## Cloud DevOps Nanodegree Capstone Project

This is the Capstone Project where I could demonstrate all the things that I have learned in the Nanodegree Program.

_________________________________________________________________________________________________________________________

### Ojective of the Project

The main objective is to use AWS, Jenkins, Docker and Kubernetes to develop a microservice application, containerize the microservice application and build a CI/CD pipeline for that application. Finally deploy it on a Kubernetes cluster.

_________________________________________________________________________________________________________________________

### Tasks to be completed [TODOs] --

- [x] Step 1: Propose and Scope the Project
- [x] Step 2: Use Jenkins, and implement blue/green or rolling deployment
- [x] Step 3: Pick AWS Kubernetes as a Service, or build your own Kubernetes cluster
- [x] Step 4: Build your pipeline
- [x] Step 5: Test your pipeline

_________________________________________________________________________________________________________________________

### Requirements and Dependencies to run the Project

* The project requires [Hadolint](https://github.com/hadolint/hadolint) to lint the Dockerfile
* The Project requires pylint python package
  ```python
  pip install pylint
  ```
* The Project requires an AWS account to create all the resources
* The Project required [Jenkins](https://www.jenkins.io/doc/book/installing/) CI/CD tool
* The Project requires aws cli installed
* The Project requires Docker[https://docs.docker.com/get-docker/] and [Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl/#before-you-begin)
* The Project might need a [Dockerhub](https://hub.docker.com/) account if you want to push or pull the container images
* The Project required [eksctl](https://github.com/weaveworks/eksctl) cli tool for creating kubernetes cluster on Amazon EKS.
  (eksctl uses the AWS CloudFormation tool under the hood to create the necessary cluster infrastructure elements and it is till the easiest and the fastest was to create a kuberenets cluster on Amazon AWS)

_________________________________________________________________________________________________________________________

### Steps to run the Jenkins pipeline

* Follow the necessary steps to install Jenkins and login to it
* Install the required plugins like -
  - BlueOcean
  - Amazon ECR
  - Pipeline: AWS Steps
* Get into BlueOcean after installation
* Sync it with your GitHub Account and select the required Repo
* Jenkins then Builds the Project pipeline for you

_________________________________________________________________________________________________________________________

### Project and its branches

* I have created two other branches of the project in order to create two versions of the webapp that I want to deploy
* *blue_branch* creates and pushes the blue version of the webapp
  ![alt text](https://github.com/SavanGowda/Udacity_Capstone/tree/master/images/udacap_blue_page.png)
* *green_branch* creates and pushes the blue version of the webapp
  ![alt text](https://github.com/SavanGowda/Udacity_Capstone/tree/master/images/udacap_green_page.png)
* *master*
  - The Jenkinsfile in the *master* builds and pushes the blue version of the webapp by default
  - The Jenkinsfile further contains a stage to create the Kubernetes cluster with the help of eksctl and deploy the blue-nodegroups and the service (LoadBalancer) and deploys the blue version of the webapp (which could be accessed through the LoadBalancer DNS)
  - After completion of the deployment the Jekinsfile further asks for the User input or approval to deploy the green version of the webapp.
  - If the User chooses to approve the deployment, Jenkins proceeds further and creates the green-nodegroups and deploy the green version of the app. The Loadbalancer then switches its route and sends the web-traffic to the these node-group. (The green version of the webapp is accessible with the same LoadBalancer DNS)
  - If the User chooses not to approve, then Jenkins end the pipeline giving a abort message. Nevertheless, the blue version of the webapp could still be accessed.
