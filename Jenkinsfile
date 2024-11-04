pipeline {
    agent any
    environment {
        // Retrieve Docker Hub credentials as a single variable
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub') // Use Jenkins credentials
        BRANCH_NAME = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
    }
    stages {
        stage("Prepare") {
            steps {
                echo "Branch Name: ${env.BRANCH_NAME}"
            }
        }
        stage("Build Release Containers") {
            steps {
                echo "=======executing build======="
                script {
                    sh '''
                    docker-compose build
                    '''
                }
            }
            post {
                always {
                    echo "========always========"
                }
                success {
                    echo "========Build executed successfully!========"
                }
                failure {
                    echo "========Build execution failed========"
                }
            }
        }
        stage("Tag Images") {
            steps {
                script {
                    def frontendImage = "peetahdarius/jenkins-test-frontend"
                    def backendImage = "peetahdarius/jenkins-test-backend"
                    def version = "1.0.1" // or dynamic versioning

                    sh "docker tag ${frontendImage}:latest ${frontendImage}:${version}"
                    sh "docker tag ${backendImage}:latest ${backendImage}:${version}"
                }
            }
        }
        stage("Login to Docker Hub") {
            steps {
                script {
                    // Securely login to Docker Hub without exposing credentials
                    sh '''
                    echo "${DOCKER_HUB_CREDENTIALS_PSW}" | docker login -u "${DOCKER_HUB_CREDENTIALS_USR}" --password-stdin
                    '''
                }
            }
        }
        stage("Push Containers to Docker Hub") {
            steps {
                script {
                    def frontendImage = "peetahdarius/jenkins-test-frontend"
                    def backendImage = "peetahdarius/jenkins-test-backend"
                    def version = "1.0.0" // or dynamic versioning

                    sh "docker push ${frontendImage}:${version}"
                    sh "docker push ${backendImage}:${version}"
                }
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
