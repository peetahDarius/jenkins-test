pipeline {
    agent any
    stages {
        stage("build release containers") {
            steps {
                script {
                    // Retrieve BRANCH_NAME dynamically
                    env.BRANCH_NAME = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
                    echo "Branch Name: ${env.BRANCH_NAME}"
                }
            }
            when {
                expression { (env.BRANCH_NAME ?: env.GIT_BRANCH).startsWith('release-') }
            }
            steps {
                echo "========executing A========"
                script {
                    sh '''
                    docker-compose build
                    '''
                }
            }
            post {
                always {
                    echo "========always========"
                    echo "post execution!."
                }
                success {
                    echo "========A executed successfully!========"
                }
                failure {
                    echo "========A execution failed========"
                }
            }
        }
        stage("pushing containers to dockerhub") {
            steps {
                script {
                    // Retrieve BRANCH_NAME dynamically again if needed
                    env.BRANCH_NAME = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
                    echo "Branch Name: ${env.BRANCH_NAME}"
                }
            }
            when {
                expression { (env.BRANCH_NAME ?: env.GIT_BRANCH).startsWith('release-') }
            }
            steps {
                echo "========executing A========"
            }
            post {
                always {
                    echo "========always========"
                }
                success {
                    echo "========A executed successfully========"
                }
                failure {
                    echo "========A execution failed========"
                }
            }
        }
    }
    post {
        always {
            echo "========always========"
        }
        success {
            echo "========pipeline executed successfully========"
        }
        failure {
            echo "========pipeline execution failed========"
        }
    }
}
