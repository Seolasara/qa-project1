pipeline {
    agent any

    environment {
        WORKDIR = "project_root"
        VENV = "venv"
        ALLURE_DIR = "reports/allure"
    }

    stages {

        /* --- 1. 프로젝트 체크아웃 --- */
        stage('준비') {
            steps {
                checkout scm
                echo "📌 HelpyChat QA Pipeline Started"
            }
        }

        /* --- 2. Python 가상환경 생성 + 최신 requirements 설치 --- */
        stage('환경 설정') {
            steps {
                dir("${WORKDIR}") {
                    sh """
                        echo "🐍  Python 가상환경 생성"
                        python3 -m venv ${VENV}

                        echo "📦 pip 최신화 및 최신 requirements 설치"
                        ${VENV}/bin/python -m pip install --upgrade pip
                        ${VENV}/bin/python -m pip install -r ../requirements.txt
                    """
                }
            }
        }

        /* --- 3. pytest 실행 (pytest.ini 반영, Allure 포함) --- */
        stage('전체 테스트 실행') {
            steps {
                dir("${WORKDIR}") {
                    sh """
                        echo "🧪  pytest 실행"
                        ${VENV}/bin/python -m pytest \
                            --junit-xml=reports/all-results.xml \
                    """
                }
            }
        }

        /* --- 4. 브랜치 조건부 배포 --- */
        stage('배포') {
            when { anyOf { branch 'develop'; branch 'main' } }
            steps {
                echo "🚀 배포 단계 (현재는 메시지만 출력)"
            }
        }
    }

    post {
        always {
            echo "📄  테스트 리포트 업로드"
            junit "${WORKDIR}/reports/all-results.xml"
            publishHTML([
                reportDir: "${WORKDIR}/reports/htmlcov",
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            allure([
                includeProperties: false,
                results: [[path: "${WORKDIR}/reports/allure"]],
                commandline: 'Allure'
            ])
        }

        success {
            echo "✅ HelpyChat QA Pipeline ALL PASSED!"
        }

        failure {
            echo "❌ Pipeline FAILED — 확인 필요"
        }
    }
}
