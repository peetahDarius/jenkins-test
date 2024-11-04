pipeline {
    agent any
    environment {
        // Initialize BRANCH_NAME here for use in all stages
        BRANCH_NAME = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
        DOCKER_HUB_USERNAME = credentials('dockerhub') // Use Jenkins credentials
        DOCKER_HUB_PASSWORD = credentials('dockerhub') // Use Jenkins credentials
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
                    def frontendImage = "myapp/frontend"
                    def backendImage = "myapp/backend"
                    def version = "1.0.0" // or dynamic versioning

                    sh "docker tag ${frontendImage}:latest ${frontendImage}:${version}"
                    sh "docker tag ${backendImage}:latest ${backendImage}:${version}"
                }
            }
        }
        stage("Login to Docker Hub") {
            steps {
                script {
                    sh "echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin"
                }
            }
        }
        stage("Push Containers to Docker Hub") {
            steps {
                script {
                    def frontendImage = "peetahdarius/jenkins-test/frontend"
                    def backendImage = "peetahdarius/jenkins-test/backend"
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
