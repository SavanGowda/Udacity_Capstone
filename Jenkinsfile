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

            #REG_ADDRESS="981422959347.dkr.ecr.us-west-2.amazonaws.com"
            #REPO="udacitycap"
            #sh 'aws ecr get-login --no-include-email --region us-west-2'
            #sh "$(aws ecr get-login --no-include-email --region us-west-2)"

            #aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap
            #withDockerRegistry([url: "https://536703334988.dkr.ecr.ap-southeast-2.amazonaws.com/test-repository",credentialsId: "udacity-cap"]

            withDockerRegistry([url: "https://981422959347.dkr.ecr.us-west-2.amazonaws.com/udacitycap",credentialsId: "udacity-cap"]){
                #Tag the build with BUILD_NUMBER version
                docker tag ${REPO}:${BUILD_NUMBER} ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}

                #Publish image
                docker push ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}
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
