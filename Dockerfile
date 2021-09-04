FROM continuumio/miniconda3:4.10.3

RUN apt-get update && apt-get install gnupg2 libgl1 -y

WORKDIR /code

COPY . .

RUN echo "conda version is something a $(conda -V)"

RUN conda env create -f ./environment.yml

RUN echo "source activate $(head -1 ./environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 ./environment.yml | cut -d' ' -f2)/bin:$PATH

