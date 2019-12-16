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
                kubernetesDeploy(kubeconfigId: 'kubeconfig',               // REQUIRED
                 configs: 'beats/auditbeat.yml,beats/filebeat.yml,beats/metricbeat.yml', // REQUIRED
                 enableConfigSubstitution: true
)
            }
        }
        stage("send mail"){
            steps{
                mail (
                    to: env.NOTIFY_MAIL,
                    subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is completed successfully",
                    body: "Please go to ${env.BUILD_URL}.")
            }
        }
    }    
}