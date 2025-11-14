pipeline {
    agent any

    environment {
        WORKDIR = "project_root"
        PYTHONPATH = "${WORKSPACE}/${WORKDIR}"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                dir("${WORKDIR}") {
                    script {
                        if (isUnix()) {
                            sh '''
                                set -e

                                # python3 우선, 없으면 python
                                (command -v python3 >/dev/null 2>&1 && python3 -m venv venv) || python -m venv venv

                                . venv/bin/activate
                                pip install --upgrade pip

                                if [ -f requirements.txt ]; then
                                    pip install -r requirements.txt
                                else
                                    pip install pytest
                                fi
                            '''
                        } else {
                            bat '''
                                @echo off
                                py -3 -m venv venv || python -m venv venv

                                call venv\\Scripts\\activate.bat
                                python -m pip install --upgrade pip

                                if exist requirements.txt (
                                    pip install -r requirements.txt
                                ) else (
                                    pip install pytest
                                )
                            '''
                        }
                    }
                }
            }
        }

        stage('Run pytest') {
            steps {
                dir("${WORKDIR}") {
                    script {
                        if (isUnix()) {
                            sh '''
                                set -e
                                . venv/bin/activate
                                pytest src/tests/ --junitxml=pytest-report.xml
                            '''
                        } else {
                            bat '''
                                @echo off
                                call venv\\Scripts\\activate.bat
                                pytest src\\tests\\ --junitxml=pytest-report.xml
                            '''
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: "${WORKDIR}/pytest-report.xml"
        }
        success {
            echo '테스트 자동화가 성공적으로 완료되었습니다!ㅇㅇㅇㅇ'
        }
        failure {
            echo '테스트 자동화 중 일부 테스트가 실패했습니다. 리포트를 확인해주세요.'
        }
    }
}
