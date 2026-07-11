FROM microfluidica/openfoam:13

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        python3-venv \
        cmake \
        build-essential \
        sudo \
    && rm -rf /var/lib/apt/lists/*

RUN echo '' >> /etc/bash.bashrc && \
    echo '# Source OpenFOAM 13 environment' >> /etc/bash.bashrc && \
    echo 'if [ -f /opt/openfoam13/etc/bashrc ]; then' >> /etc/bash.bashrc && \
    echo '    source /opt/openfoam13/etc/bashrc' >> /etc/bash.bashrc && \
    echo 'fi' >> /etc/bash.bashrc

# Resolve whatever user already owns UID 1000, grant sudo, own the workspace
RUN EXISTING_USER=$(getent passwd 1000 | cut -d: -f1) && \
    echo "Resolved UID 1000 to: $EXISTING_USER" && \
    echo "$EXISTING_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$EXISTING_USER && \
    chmod 0440 /etc/sudoers.d/$EXISTING_USER && \
    echo "$EXISTING_USER" > /tmp/devuser

WORKDIR /workspaces/bristled-wing

RUN chown -R 1000:1000 /workspaces/bristled-wing

USER 1000