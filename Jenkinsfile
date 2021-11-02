pipeline {
    agent { docker { image 'python:3.9.5' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}