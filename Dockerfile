FROM ubuntu:jammy-20220531

WORKDIR /app

RUN apt-get update && \
  apt-get install --no-install-recommends -y wget gnupg build-essential ca-certificates nano

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install --no-install-recommends -y tzdata

RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | gpg --dearmor -o /usr/share/keyrings/r-project.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" | tee -a /etc/apt/sources.list.d/r-project.list && \
    apt-get update && apt install --no-install-recommends -y r-base

RUN apt-get install --no-install-recommends -y libpq-dev gdal-bin libgdal-dev && \
    rm -rf /var/lib/apt/lists/*

RUN Rscript -e 'install.packages(c("lubridate", "rgdal", "terra", "raster", "move"), repos="https://cloud.r-project.org")'

RUN wget \
  "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh" \
  -O Mambaforge.sh && \
  bash "Mambaforge.sh" -b && \
  . "${HOME}/mambaforge/bin/activate"
ENV PATH="/root/mambaforge/bin:$PATH"

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
