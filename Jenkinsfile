pipeline {
    agent any
    environment {
        FLOWS_DIR = 'flows'
        REPO_URL = 'https://raw.githubusercontent.com/Harshneeraj/Langflow_CICD/main'
        HELM_PATH = './langflow-runtime'
    }

    stages {
        stage('Detect Flow Changes') {
            steps {
                script {
                    def prevCommit = sh(script: 'git rev-parse HEAD~1 || echo ""', returnStdout: true).trim()
                    def currCommit = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()

                    if (!prevCommit) {
                        echo "No previous commit found. Using current commit only."
                        prevCommit = "${currCommit}^"
                    }

                    def changedFiles = sh(
                        script: "git diff --name-only ${prevCommit} ${currCommit}",
                        returnStdout: true
                    ).trim().split('\n')

                    def jsonFlows = changedFiles.findAll { it.startsWith("${FLOWS_DIR}/") && it.endsWith('.json') }

                    if (jsonFlows.size() > 0) {
                        echo "Detected flow changes in: ${jsonFlows.join(', ')}"
                        for (flowFile in jsonFlows) {
                            def flowId = flowFile.tokenize('/').last().replace('.json', '')
                            def fileUrl = "${REPO_URL}/${flowFile}"
                            def path = "/flows"
                            def releaseName = "langflow-${flowId}".toLowerCase()

                            echo "Deploying Helm release for flow: ${flowId}"
                            sh """
                            helm upgrade --install ${releaseName} ${HELM_PATH} \\
                              --set flow.flow-id=${flowId} \\
                              --set downloadFlows.flows[0].url=${fileUrl}
                            """
                        }
                    } else {
                        echo "No new/changed flow JSONs detected."
                    }
                }
            }
        }
    }
}
