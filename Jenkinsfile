pipeline{
  agent any

  parameters([
        string(defaultValue: "981422959347.dkr.ecr.us-west-2.amazonaws.com", description: 'AWS Account Number?', name: 'REG_ADDRESS'),
        string(defaultValue: "udacitycap", description: 'Name of the ECR registry', name: 'REPO')
	])

  stages{

    stage('Install Dependencies') {
      steps{
            sh "make install"
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

            withDockerRegistry([url: "https://981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap",credentialsId: "udacity-cap"]){

                sh "docker tag ${REPO}:${BUILD_NUMBER} ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}"

                sh "docker push ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}"
            }
        }
      }

    stage('Create Stack and Deploy to K8s'){
      steps{
            sh 'echo "Uploading to ECR Complete!"'
        }
      }
    }
}
