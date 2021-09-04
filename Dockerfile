FROM python:3.7-bullseye


RUN curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg

RUN install -o root -g root -m 644 conda.gpg /usr/share/keyrings/conda-archive-keyring.gpg

RUN gpg --keyring /usr/share/keyrings/conda-archive-keyring.gpg --no-default-keyring --fingerprint 34161F5BF5EB1D4BFBBB8F0A8AEB4F8B29D82806

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/conda-archive-keyring.gpg] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" > /etc/apt/sources.list.d/conda.list

RUN apt-get update && apt-get install -y conda

RUN apt-get update && apt-get install gnupg2 -y

SHELL ["/bin/bash", "-c",  "source /opt/conda/etc/profile.d/conda.sh" ]

RUN echo "conda version is $(conda -V)"

WORKDIR /code

COPY . .

RUN conda env create -f ./environment.yml

ENTRYPOINT ["/bin/bash", "-c",  "source /opt/conda/etc/profile.d/conda.sh" ]
