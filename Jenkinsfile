pipeline {
    agent any
    environment {
        PROJECT_ID = 'interviews-dev'
        CLUSTER_NAME = 'interview-cluster'
        LOCATION = 'europe-west1-b'
        CREDENTIALS_ID = 'gke'
    }
    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }        
        stage('Deploy to GKE') {
            steps{
                step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: '.', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
            }
        }
    }    
}