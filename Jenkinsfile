// pipeline {
//     agent any

//     environment {
//         WORKDIR = "project_root"
//         VENV = "venv"
//     }

//     stages {

//         /* --- 1. 프로젝트 체크아웃 --- */
//         stage('준비') {
//             steps {
//                 checkout scm
//                 echo "📌 HelpyChat QA Pipeline Started"

//                 dir("${WORKDIR}") {
//                     echo "📁 Working directory: ${WORKDIR}"
//                 }
//             }
//         }

//         /* --- 2. Python 가상환경 생성 + 패키지 설치 --- */
//         stage('의존성 설치') {
//             steps {
//                 script {
//                     dir("${WORKDIR}") {
//                         if (isUnix()) {
//                             sh """
//                                 python3 -m venv ${VENV}
//                                 . ${VENV}/bin/activate
//                                 pip install --upgrade pip
//                                 pip install -r requirements.txt
//                             """
//                         } else {
//                             bat """
//                                 python -m venv ${VENV}
//                                 call ${VENV}\\Scripts\\activate
//                                 pip install --upgrade pip
//                                 pip install -r requirements.txt
//                             """
//                         }
//                     }
//                 }
//             }
//         }

//         /* --- 3. 전체 테스트 실행 --- */
//         stage('전체 테스트 실행') {
//             steps {
//                 script {
//                     dir("${WORKDIR}") {
//                         if (isUnix()) {
//                             sh """
//                                 . ${VENV}/bin/activate
//                                 pytest tests -v \
//                                     --junit-xml=reports/all-results.xml \
//                                     --html=reports/report.html \
//                                     --self-contained-html
//                             """
//                         } else {
//                             bat """
//                                 call ${VENV}\\Scripts\\activate
//                                 pytest tests -v ^
//                                     --junit-xml=reports\\all-results.xml ^
//                                     --html=reports\\report.html ^
//                                     --self-contained-html
//                             """
//                         }
//                     }
//                 }
//             }
//         }

//         /* --- 4. 커버리지 분석 --- */
//         stage('커버리지 분석') {
//             steps {
//                 script {
//                     dir("${WORKDIR}") {
//                         if (isUnix()) {
//                             sh """
//                                 . ${VENV}/bin/activate
//                                 pytest --cov=src \
//                                        --cov-report=html:reports/htmlcov \
//                                        --cov-report=xml:reports/coverage.xml
//                             """
//                         } else {
//                             bat """
//                                 call ${VENV}\\Scripts\\activate
//                                 pytest --cov=src ^
//                                        --cov-report=html:reports\\htmlcov ^
//                                        --cov-report=xml:reports\\coverage.xml
//                             """
//                         }
//                     }
//                 }
//             }
//         }

//         /* --- 5. 브랜치 조건부 배포 --- */
//         stage('배포') {
//             when { anyOf { branch 'develop'; branch 'main' } }
//             steps {
//                 echo "🚀 배포 단계 (현재는 메시지만 출력)"
//             }
//         }
//     }

//     /* --- 6. 테스트 리포트 업로드 --- */
//     post {
//         always {
//             // JUnit XML 업로드
//             junit "project_root/reports/all-results.xml"

//             // Coverage Report 업로드
//             publishHTML([
//                 reportDir: 'project_root/reports/htmlcov',
//                 reportFiles: 'index.html',
//                 reportName: 'Coverage Report'
//             ])

//             // Test HTML Report 업로드
//             publishHTML([
//                 reportDir: 'project_root/reports',
//                 reportFiles: 'report.html',
//                 reportName: 'Test HTML Report'
//             ])
//         }

//         success {
//             echo "✅ HelpyChat QA Pipeline ALL PASSED!"
//         }

//         failure {
//             echo "❌ Pipeline FAILED — 확인 필요"
//         }
//     }
// }



// 히스토리브랜치 실행 코드
pipeline {
    agent any

    environment {
        WORKDIR = "project_root"
        VENV = "venv"
        REPORT_DIR = "reports"
    }

    stages {

        /* --- 0. 브랜치 체크 --- */
        stage('브랜치 체크') {
            steps {
                script {
                    echo "🔍 Checking branch: ${env.BRANCH_NAME}"
                    if (env.BRANCH_NAME != 'feature_history') {
                        echo "⛔ This pipeline runs only on feature_history branch."
                        currentBuild.result = 'NOT_BUILT'
                        error("Stopping pipeline.")
                    }
                }
            }
        }

        /* --- 1. 프로젝트 체크아웃 --- */
        stage('준비') {
            steps {
                checkout scm
                echo "📌 HelpyChat QA Pipeline Started"

                dir("${WORKDIR}") {
                    echo "📁 Working directory: ${WORKDIR}"
                }
            }
        }

        /* --- 2. 리포트 디렉토리 준비 --- */
        stage('리포트 디렉토리 준비') {
            steps {
                dir("${WORKDIR}") {
                    script {
                        if (isUnix()) {
                            sh "mkdir -p ${REPORT_DIR}/htmlcov"
                        } else {
                            bat "if not exist ${REPORT_DIR} mkdir ${REPORT_DIR}"
                            bat "if not exist ${REPORT_DIR}\\htmlcov mkdir ${REPORT_DIR}\\htmlcov"
                        }
                    }
                }
            }
        }

        /* --- 3. Python 가상환경 생성 + 패키지 설치 --- */
        stage('의존성 설치') {
            steps {
                script {
                    dir("${WORKDIR}") {
                        if (isUnix()) {
                            sh """
                                python3 -m venv ${VENV}
                                . ${VENV}/bin/activate
                                pip install --upgrade pip
                                pip install -r requirements.txt
                            """
                        } else {
                            bat """
                                python -m venv ${VENV}
                                call ${VENV}\\Scripts\\activate
                                pip install --upgrade pip
                                pip install -r requirements.txt
                            """
                        }
                    }
                }
            }
        }

        /* --- 4. 전체 테스트 실행 --- */
        stage('전체 테스트 실행') {
            steps {
                script {
                    dir("${WORKDIR}") {
                        if (isUnix()) {
                            sh """
                                . ${VENV}/bin/activate
                                pytest tests -v \
                                    --junit-xml=${REPORT_DIR}/all-results.xml \
                                    --html=${REPORT_DIR}/report.html \
                                    --self-contained-html
                            """
                        } else {
                            bat """
                                call ${VENV}\\Scripts\\activate
                                pytest tests -v ^
                                    --junit-xml=${REPORT_DIR}\\all-results.xml ^
                                    --html=${REPORT_DIR}\\report.html ^
                                    --self-contained-html
                            """
                        }
                    }
                }
            }
        }

        /* --- 5. 커버리지 분석 --- */
        stage('커버리지 분석') {
            steps {
                script {
                    dir("${WORKDIR}") {
                        if (isUnix()) {
                            sh """
                                . ${VENV}/bin/activate
                                pytest --cov=src \
                                       --cov-report=html:${REPORT_DIR}/htmlcov \
                                       --cov-report=xml:${REPORT_DIR}/coverage.xml
                            """
                        } else {
                            bat """
                                call ${VENV}\\Scripts\\activate
                                pytest --cov=src ^
                                       --cov-report=html:${REPORT_DIR}\\htmlcov ^
                                       --cov-report=xml:${REPORT_DIR}\\coverage.xml
                            """
                        }
                    }
                }
            }
        }

    }

    /* --- 6. 테스트 리포트 업로드 --- */
    post {
        always {
            // JUnit XML 업로드
            junit "project_root/reports/all-results.xml"

            // Coverage Report 업로드
            publishHTML([
                reportDir: 'project_root/reports/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])

            // Test HTML Report 업로드
            publishHTML([
                reportDir: 'project_root/reports',
                reportFiles: 'report.html',
                reportName: 'Test HTML Report'
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

