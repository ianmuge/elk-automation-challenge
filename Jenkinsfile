pipeline {
    agent any
    environment {
        PROJECT_ID = 'interviews-dev'
        CLUSTER_NAME = 'interview-cluster'
        LOCATION = 'europe-west1-b'
        CREDENTIALS_ID = 'interviews'
    }
    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }        
        stage('Deploy ELK') {
            steps{
                kubernetesDeploy(kubeconfigId: 'kubeconfig',               // REQUIRED
                 configs: 'elasticsearch.yml,kibana.yml,logstash.yml', // REQUIRED
                 enableConfigSubstitution: true
)
            }
        }
        stage('Deploy Beats') {
            steps{
                step()
            }
        }
    }    
}