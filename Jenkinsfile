pipeline{
  agent any
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
        sh '''
            REG_ADDRESS="981422959347.dkr.ecr.us-west-2.amazonaws.com"
            REPO="udacitycap"

            #Tag the build with BUILD_NUMBER version
            docker tag ${REPO}:${BUILD_NUMBER} ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}

            #Publish image
            docker push ${REG_ADDRESS}/${REPO}:${BUILD_NUMBER}
          '''
        }
      }

    stage('Create Stack and Deploy to K8s'){
      steps{
            sh 'echo "Uploading to ECR Complete!"'
        }
      }
    }
}
