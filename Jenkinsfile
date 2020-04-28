pipeline{
  agent any

  environment {
     JENKINS_PATH = sh(script: 'pwd', , returnStdout: true).trim()
  }

  parameters{
        string(defaultValue: "981422959347.dkr.ecr.us-west-2.amazonaws.com", description: 'AWS Account Number?', name: 'REG_ADDRESS')
        string(defaultValue: "udacitycap-blue", description: 'Name of the blue ECR registry', name: 'BLUE_REPO')
        string(defaultValue: "udacitycap-green", description: 'Name of the green ECR registry', name: 'GREEN_REPO')
        string(defaultValue: "us-west-2", description: 'AWS Region', name: 'REGION')
        string(defaultValue: "blue", description: 'AWS Region', name: 'BLUE_TAG')
        string(defaultValue: "green", description: 'AWS Region', name: 'GREEN_TAG')
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
            docker build --no-cache -t ${params.BLUE_REPO}:${BUILD_NUMBER} .
            '''
        }
      }

    stage('Pushing_Image_To_ECR') {
      steps {

            withDockerRegistry([url: "https://981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap",credentialsId: "ecr:us-west-2:ecr-credentials"]){

                sh "docker tag ${params.BLUE_REPO}:${BUILD_NUMBER} ${params.REG_ADDRESS}/${params.BLUE_REPO}:${params.BLUE_TAG}"

                sh "docker push ${params.REG_ADDRESS}/${params.BLUE_REPO}:${params.BLUE_TAG}"
            }
        }
      }


    stage('Create Stack and Deploy to K8s'){
      environment {
         JENKINS_PATH = sh(script: 'pwd', , returnStdout: true).trim()
      }
      steps{
            sh 'mkdir -p ${JENKINS_PATH}/kubeconfigs'

            sh 'eksctl create cluster -f blue/main.yaml --kubeconfig=${JENKINS_PATH}/kubeconfigs/bluegreen-cluster-config.yaml'
            withEnv(["KUBECONFIG=${JENKINS_PATH}/kubeconfigs/bluegreen-cluster-config.yaml", "IMAGE=${params.REG_ADDRESS}/${params.BLUE_REPO}:${params.BLUE_TAG}"]){

              sleep 30
              sh 'kubectl get all --all-namespaces'

              sh "sed -i '' 's|IMAGE|${IMAGE}|g' blue_deploy.yaml"

              sh "kubectl apply -f blue_deploy.yaml"


              echo "Creating kubernetes resources"
              sh 'sleep 180'
              sh 'kubectl get pods'

              sh 'kubectl apply -f k8s-blue-svc.yaml'
              sh 'kubectl get svc'
              sh 'kubectl describe services udacity-cap'
              sh 'kubectl get pods --selector="app=udacity-cap-blue" --output=wide'
          }
        }
      }

        stage('Deploy Green Service'){
          environment {
             JENKINS_PATH = sh(script: 'pwd', , returnStdout: true).trim()
          }

          input {
              message "Should we continue?"
              ok "Yes, we should."
              submitter "savan"
            }

          steps{
                //sh 'mkdir -p ${JENKINS_PATH}/kubeconfigs'

                //sh 'eksctl create cluster -f green/main.yaml --kubeconfig=${JENKINS_PATH}/kubeconfigs/bluegreen-cluster-config.yaml'
                withEnv(["KUBECONFIG=${JENKINS_PATH}/kubeconfigs/bluegreen-cluster-config.yaml", "IMAGE=${params.REG_ADDRESS}/${params.GREEN_REPO}:${params.GREEN_TAG}"]){

                  sleep 30
                  //sh 'kubectl get all --all-namespaces'

                  sh "sed -i '' 's|IMAGE|${IMAGE}|g' green_deploy.yaml"
                  sh "eksctl create nodegroup --config-file=green/main.yaml"

                  sh "kubectl apply -f green_deploy.yaml"


                  echo "Creating kubernetes resources"
                  sh 'sleep 180'
                  sh 'kubectl get pods'

                  sh 'kubectl apply -f k8s-green-svc.yaml'
                  sh 'kubectl get svc'
                  sh 'kubectl describe services udacity-cap'
                  sh 'kubectl get pods --selector="app=udacity-cap-green" --output=wide'
              }
            }
        }
    }
    post {
        success {
            echo 'I have finished deploying the blue deployment and with user permission the green deployment'
        }
        aborted {
            echo 'The build has succeeded until blue deployment. The user has aborted the green deployment'
            echo 'Rebuild the pipeline and choose - Yes, we should - to deploy the green deployment'
        }
        failure{
            echo ' The build has failed!'
        }
      }
}
