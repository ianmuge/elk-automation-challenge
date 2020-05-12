
pipeline {
    agent any
    environment {
        PROJECT_ID = ''
        CLUSTER_NAME = ''
        LOCATION = ''
        CREDENTIALS_ID = ''
        NOTIFY_MAIL=''
    }
    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }        
        stage('Compile manifests') {
            steps{
            sh """ 
                kubectl kustomize . > compiled.yml 
                """        
            }
        }
        stage('Deploy to GKE') {
            steps{
                step([
                $class: 'KubernetesEngineBuilder',
                projectId: env.PROJECT_ID,
                clusterName: env.CLUSTER_NAME,
                location: env.LOCATION,
                manifestPattern: 'compiled.yml',
                credentialsId: env.CREDENTIALS_ID,
                verifyDeployments: false])
            }
        }
        stage("Prepare for Infrastructure testing"){
         steps {
            script {
                withCredentials([file(credentialsId: 'service-account', variable: 'service_account')]) {

                   sh """
                   cp \$service_account ./service-account.json
                   chmod 640 ./service-account.json
                   """
                }
                }
            }
         }
         stage("Create Virtual Environment"){
            steps{
            sh """
                python3 -m venv env
                . env/bin/activate
                pip3 install -r requirements.txt
                """
            }
         }
         stage("Integration testing"){
            steps{
            sh """
                . env/bin/activate
                python3 -m unittest discover -s ./tests/integration -t ./tests/integration
                """
            }
         }
         stage("Performance testing"){
            steps{
            sh """
                . env/bin/activate
                python3 ./tests/performance/main.py
                """
            }
         }

         stage("Infrastructure testing"){
            steps{
            sh """
                . env/bin/activate
                python3 -m unittest discover -s ./tests/infrastructure -t ./tests/infrastructure
                """
            }
         }
    }    
}
