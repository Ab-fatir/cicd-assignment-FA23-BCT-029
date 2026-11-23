pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'assignment3-site'
        STAGING_PORT = '8091'
        PROD_PORT    = '8081'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f assignment3-staging || true
                    docker run -d --name assignment3-staging -p ${STAGING_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://localhost:${STAGING_PORT}/ > /dev/null
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }
            environment {
                HOME     = '/tmp'
                BASE_URL = "http://localhost:${STAGING_PORT}"
            }
            steps {
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "All automated Selenium tests passed. Deploying to production port ${PROD_PORT}..."
                sh '''
                    docker rm -f assignment3-prod || true
                    docker run -d --name assignment3-prod --restart unless-stopped -p ${PROD_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f assignment3-staging || true'
        }
        success {
            echo "Build ${BUILD_NUMBER} successfully deployed to production port ${PROD_PORT}."
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed quality gate. Production was not modified."
        }
    }
}
