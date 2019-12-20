
pipeline {
    agent any
    environment {
        PROJECT_ID = 'interviews-dev'
        CLUSTER_NAME = 'interview-cluster'
        LOCATION = 'europe-west1-b'
        CREDENTIALS_ID = 'interviews'
        NOTIFY_MAIL='ian.muge@gmail.com'
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
                withCredentials([file(credentialsId: 'service-account', variable: 'service-account')]) {
                   sh "cp \$service-account ./infrastructure/service-account.json"
                }
                }
            }
         }
         stage("Create Virtual Environment and run tests"){
            steps{
            sh """
                python3 -m venv env
                . env/bin/activate
                pip3 install -r requirements.txt
                python3 -m unittest discover -s ./tests/integration -t ./tests/integration
                python3 ./tests/performance/main.py
                python3 -m unittest discover -s ./tests/infrastructure -t ./tests/infrastructure
                """
            }
         }
         stage("Deactivate Virtual Environment"){
            steps{
            sh """
                deactivate
                """
            }
         }
    }    
}
