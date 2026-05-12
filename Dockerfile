FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    wget \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Put conda in path
ENV PATH=$CONDA_DIR/bin:$PATH

# Create the environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "neuro_env", "/bin/bash", "-c"]

# Set the working directory
WORKDIR /app

# Copy the source code
COPY . .

# Expose the streamlit port
EXPOSE 8501

# Entrypoint to run streamlit
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "neuro_env", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
