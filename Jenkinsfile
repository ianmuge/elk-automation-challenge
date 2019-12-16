
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
        // stage("send mail"){
        //     steps{
        //         mail (
        //             to: env.NOTIFY_MAIL,
        //             subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is completed successfully",
        //             body: "Build URL to ${env.BUILD_URL}.")
        //     }
        // }
    }    
}
