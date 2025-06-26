pipeline {
  agent any

  environment {
    FLOWS_DIR = "flows"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Detect Updated Flows') {
      steps {
        script {
          // Get list of added/modified .json files in flows dir
          def changedFlows = sh(
            script: "git diff --name-only HEAD~1 HEAD | grep '^${FLOWS_DIR}/.*\\.json$' || true",
            returnStdout: true
          ).trim().split("\n").findAll { it }

          if (changedFlows.isEmpty()) {
            echo "No updated flows found, skipping deploy."
            currentBuild.result = 'SUCCESS'
            return
          }

          // Deploy each flow
          for (flowPath in changedFlows) {
            def fileName = flowPath.tokenize('/').last()
            def flowId = fileName.replace('.json', '')
            def flowDir = flowPath.replaceAll("/${fileName}$", '')

            echo "Deploying Flow ID: ${flowId}, from path: ${flowDir}"

            sh """
              helm upgrade --install langflow-${flowId} ./langflow-runtime \
                --set flow.flow-id=${flowId} \
                --set flow.downloadFlows.path=/${flowDir}
            """
          }
        }
      }
    }
  }
}
