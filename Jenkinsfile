pipeline{
  agent any

  parameters{
        string(defaultValue: "981422959347.dkr.ecr.us-west-2.amazonaws.com", description: 'AWS Account Number?', name: 'REG_ADDRESS')
        string(defaultValue: "udacitycap", description: 'Name of the ECR registry', name: 'REPO')
	}

  stages{

    stage('Install Dependencies') {
      steps{
            sh """
              . venv/bin/activate
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
              pylint --disable=R,C,W1203,W1202 app.py
            '''
      }
    }

    stage('Build Dockerimage'){
      steps{
        sh '''
            cd ${WORKSPACE}
            REPO="udacitycap"

            #Build container images using Dockerfile
            docker build --no-cache -t ${REPO}:${BUILD_NUMBER} .
            '''
        }
      }

    stage('Pushing_Image_To_ECR') {
      steps {

            withDockerRegistry([url: "https://981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap",credentialsId: "ecr:us-west-2:ecr-credentials"]){

                sh "docker tag ${REPO}:${BUILD_NUMBER} ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}"

                sh "docker push ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}"
            }
        }
      }

    stage('Create Stack and Deploy to K8s'){
      steps{
            sh 'eksctl create cluster -f main.yaml --kubeconfig=kubeconfigs/green-cluster-config.yaml'
            sh 'export KUBECONFIG=kubeconfigs/green-cluster-config.yaml'
            sh 'kubectl get all --all-namespaces'
            sh 'kubectl apply -f deploy.yaml'
            sh 'kubectl apply -f k8s-svc.yaml'
            sh 'kubectl get svc'


            timeout(time: 5, unit: 'MINUTES') {
                    retry(5) {
                        sh 'kubectl describe services udacity-cap'
                        sh 'kubectl get pods --selector="app=udacity-cap" --output=wide'
                    }
            }
        }
      }

    stage('Make Predictions'){
      steps{
            timeout(time: 5, unit: 'MINUTES') {
              sh './make_prediction.sh'
            }
        }
      }
    }
}
post{
  always{
    echo 'Deleting the Stack'
    sh '''
    kubectl delete -f deploy.yaml
    kubectl delete -f k8s-svc.yaml
    eksctl delete cluster --name=green-cluster
    '''
  }
}
