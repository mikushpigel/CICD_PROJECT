FROM ubuntu:22.04

# Installing basic requirements including Docker
RUN apt update && apt install -y \
    docker.io \
    curl \
    unzip \
    wget \
    tar \
    python3 \
    python3-pip \
    libx11-xcb1 \
    libgbm1 \
    libasound2 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && apt clean && rm -rf /var/lib/apt/lists/*

    # Add Python dependencies for testing
RUN pip3 install \
selenium \
pytest \
pytest-selenium \
flask \
flask-sqlalchemy \
pymysql \
redis \
werkzeug \
unittest-xml-reporting

# Configure Docker daemon
VOLUME /var/lib/docker
RUN mkdir -p /etc/docker
RUN echo '{"storage-driver": "overlay2"}' > /etc/docker/daemon.json

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.31.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Install sonar-scanner
RUN curl -sSL https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip -o sonar-scanner.zip \
    && unzip sonar-scanner.zip -d /opt/ \
    && ln -s /opt/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner \
    && rm sonar-scanner.zip

# Install Google Chrome first
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt update && apt install -y google-chrome-stable

# Install matching ChromeDriver version
RUN CHROME_VERSION="$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}')" \
    && wget -q https://storage.googleapis.com/chrome-for-testing-public/"$CHROME_VERSION".0.6943.53/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver-linux64.zip

# Install Trivy
ADD https://github.com/aquasecurity/trivy/releases/download/v0.58.0/trivy_0.58.0_Linux-64bit.deb /tmp/trivy_0.58.0_Linux-64bit.deb
RUN dpkg -i /tmp/trivy_0.58.0_Linux-64bit.deb \
    && rm /tmp/trivy_0.58.0_Linux-64bit.deb

# Install Selenium
RUN pip3 install selenium webdriver_manager

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" \
    && unzip /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip

# Install Cosign
RUN curl -sSL "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64" -o /usr/local/bin/cosign \
    && chmod +x /usr/local/bin/cosign

WORKDIR /workspace

# Run Docker daemon when container starts
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["bash"]