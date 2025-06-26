pipeline {
  agent any

  environment {
    FLOW_ID = "abcdef"
    FLOWS_PATH = ""
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/<your-username>/<your-repo>.git', branch: 'main'
      }
    }

    stage('Deploy Langflow Runtime') {
      steps {
        sh '''
          echo "Using flow ID: $FLOW_ID"
          echo "Download path: $FLOWS_PATH"
          helm upgrade --install langflow-runtime ./helm-chart \
            --set flow.flow-id=$FLOW_ID \
            --set flow.downloadFlows.path=$FLOWS_PATH
        '''
      }
    }
  }
}
