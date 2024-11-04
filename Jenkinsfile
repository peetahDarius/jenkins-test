pipeline{
    agent any
    stages{
        stage("build release containers"){
            when {
                expression { env.GIT_BRANCH.startsWith('release-') }
            }
            steps{
                echo "========executing A========"
                script {
                    sh '''
                    docker-compose build
                    '''
                }
            }
            post{
                always{
                    echo "========always========"
                    echo "post execution!."
                }
                success{
                    echo "========A executed successfully !========"
                }
                failure{
                    echo "========A execution failed========"
                }
            }
        }
        stage("pushing containers to dockerhub"){
            when {
                expression { env.GIT_BRANCH.startsWith('release-') }
            }
            steps{
                echo "========executing A========"
            }
            post{
                always{
                    echo "========always========"
                }
                success{
                    echo "========A executed successfully========"
                }
                failure{
                    echo "========A execution failed========"
                }
            }
        }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}