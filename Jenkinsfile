pipeline {
    agent any
    environment {
        FLOWS_DIR = 'flows'
    }
    stages {
        stage('Detect Flow Changes') {
            steps {
                script {
                    def changedFiles = sh(
                        script: 'git diff --name-only HEAD~1 HEAD',
                        returnStdout: true
                    ).trim().split('\n')

                    def jsonFlows = changedFiles.findAll { it.startsWith("/flows/") && it.endsWith('.json') }

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
