FROM jenkins/jenkins:lts

USER root

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io curl apt-transport-https ca-certificates gnupg lsb-release sudo

# Install kubectl
RUN bash -c '\
  curl -LO https://dl.k8s.io/release/v1.33.2/bin/linux/amd64/kubectl && \
  install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
  rm kubectl'

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Give Jenkins user Docker access
RUN usermod -aG docker jenkins

USER jenkins
