pipeline{
  agent any

  environment {
     JENKINS_PATH = sh(script: 'pwd', , returnStdout: true).trim()
  }

  parameters{
        string(defaultValue: "981422959347.dkr.ecr.us-west-2.amazonaws.com", description: 'AWS Account Number?', name: 'REG_ADDRESS')
        string(defaultValue: "udacitycap-green", description: 'Name of the ECR registry', name: 'REPO')
        string(defaultValue: "us-west-2", description: 'AWS Region', name: 'REGION')
        string(defaultValue: "green", description: 'Add the green tag', name: 'TAG')
	}

  stages{
    stage('Install Dependencies') {

      steps{
            sh """
              . .venv/bin/activate
              make install
            """
      }
    }

    stage('Linting Files') {
      steps{
            sh '''
              #Lint Dockerfile
              hadolint Dockerfile

              #Lint Python file
              pylint --disable=R,C,W1203,W1202,W0312,E1101 app.py
            '''
      }
    }

    stage('Build Dockerimage'){
      steps{
        sh '''
            cd ${WORKSPACE}
            #REPO="udacitycap"

            #Build container images using Dockerfile
            docker build --no-cache -t ${REPO}:${BUILD_NUMBER} .
            '''
        }
      }

    stage('Pushing_Image_To_ECR') {
      steps {

            withDockerRegistry([url: "https://981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap",credentialsId: "ecr:us-west-2:ecr-credentials"]){

                sh "docker tag ${REPO}:${BUILD_NUMBER} ${REG_ADDRESS}/${REPO}:${TAG}"

                sh "docker push ${REG_ADDRESS}/${REPO}:${TAG}"
            }
        }
      }

  /*  stage('Create Stack and Deploy to K8s'){
      environment {
         JENKINS_PATH = sh(script: 'pwd', , returnStdout: true).trim()
      }
      steps{
            withEnv(["KUBECONFIG=${JENKINS_PATH}/kubeconfigs/green-cluster-config.yaml", "IMAGE=${REG_ADDRESS}/${REPO}:${TAG}"]){

              sh 'eksctl create nodegroup -f main.yaml'

              sleep 30

              sh 'kubectl get all --all-namespaces'

              sh "sed -i '' 's|IMAGE|${IMAGE}|g' deploy.yaml"

              sh "kubectl apply -f deploy.yaml"

              echo "Creating kubernetes resources"

              sleep 180

              sh 'kubectl get pods'

              sh 'kubectl apply -f k8s-svc.yaml'
              sh 'kubectl get svc'
              sh 'kubectl describe services udacity-cap'
              sh 'kubectl get pods --selector="app=udacity-cap" --output=wide'
          }
        }
      } */
    }
}
