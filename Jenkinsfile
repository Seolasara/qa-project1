pipeline {
    agent any

    environment {
        WORKDIR = "project_root"
        VENV = "venv"
        ALLURE_DIR = "reports/allure"
        CHROME_DRIVER_VERSION = "142.0.7444.162"
    }

    stages {

        /* --- 1. 프로젝트 체크아웃 --- */
        stage('준비') {
            steps {
                checkout scm
                echo "📌 HelpyChat QA Pipeline Started"
            }
        }

        /* --- 2. 환경 준비: Python, Chrome, ChromeDriver --- */
        stage('환경 준비') {
            steps {
                sh """
                    echo "⚙️  Python 설치"
                    apt-get update
                    apt-get install -y python3 python3-venv python3-pip wget unzip curl

                    echo "⚙️  Google Chrome 설치"
                    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
                    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

                    echo "⚙️  ChromeDriver 설치 (v${CHROME_DRIVER_VERSION})"
                    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip
                    unzip /tmp/chromedriver.zip -d /usr/local/bin/
                    chmod +x /usr/local/bin/chromedriver

                    echo "✅ 설치 확인"
                    google-chrome --version
                    chromedriver --version
                """
            }
        }

        /* --- 3. Python 가상환경 생성 + 최신 requirements 설치 + 테스트 실행 --- */
        stage('전체 테스트 실행') {
            steps {
                dir("${WORKDIR}") {
                    sh """
                        echo "🐍  Python 가상환경 생성"
                        python3 -m venv ${VENV}

                        echo "📦 pip 최신화 및 requirements 설치"
                        ${VENV}/bin/python -m pip install --upgrade pip
                        ${VENV}/bin/python -m pip install -r ../requirements.txt

                        echo "🧪  pytest 실행 (pytest.ini 반영)"
                        ${VENV}/bin/python -m pytest
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
            junit "${WORKDIR}/reports/all-results.xml"
            publishHTML([
                reportDir: "${WORKDIR}/reports/htmlcov",
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            allure([
                includeProperties: false,
                results: [[path: "${WORKDIR}/${ALLURE_DIR}"]]
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
