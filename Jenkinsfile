pipeline {
    agent any
    environment {
        // Initialize BRANCH_NAME here for use in all stages
        BRANCH_NAME = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
    }
    stages {
        stage("Prepare") {
            steps {
                echo "Branch Name: ${env.BRANCH_NAME}"
            }
        }
        stage("Build Release Containers") {
            when {
                expression { env.BRANCH_NAME.startsWith('release-') }
            }
            steps {
                echo "========executing build========"
                script {
                    sh '''
                    docker-compose build
                    '''
                }
            }
            post {
                always {
                    echo "========always========"
                    echo "post execution!"
                }
                success {
                    echo "========Build executed successfully!========"
                }
                failure {
                    echo "========Build execution failed========"
                }
            }
        }
        stage("Push Containers to Docker Hub") {
            when {
                expression { env.BRANCH_NAME.startsWith('release-') }
            }
            steps {
                echo "========executing push to Docker Hub========"
                // Add your Docker push commands here
            }
            post {
                always {
                    echo "========always========"
                }
                success {
                    echo "========Push executed successfully========"
                }
                failure {
                    echo "========Push execution failed========"
                }
            }
        }
    }
    post {
        always {
            echo "========always========"
        }
        success {
            echo "========Pipeline executed successfully========"
        }
        failure {
            echo "========Pipeline execution failed========"
        }
    }
}
