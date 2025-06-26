pipeline {
    agent any
    environment {
        FLOWS_DIR = 'flows'
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

                    def jsonFlows = changedFiles.findAll { it.startsWith("flows/") && it.endsWith('.json') }

                    if (jsonFlows.size() > 0) {
                        echo "Detected flow changes in: ${jsonFlows}"
                        for (flowFile in jsonFlows) {
                            def flowId = flowFile.tokenize('/').last().replace('.json', '')
                            def path = "/flows"
                            sh "helm upgrade --install langflow-${flowId} . --set flow.flow-id=${flowId} --set flow.downloadFlows.path=${path}"
                        }
                    } else {
                        echo "No new/changed flow JSONs detected."
                    }
                }
            }
        }
    }
}
