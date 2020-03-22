FROM continuumio/miniconda3:latest

RUN apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y \
    vim-tiny vim-athena build-essential

RUN  conda update conda \
    && conda clean --all --yes

RUN adduser --home /home/airflow airflow

RUN mkdir -p /home/airflow/airflow
COPY airflow/airflow.cfg /home/airflow/airflow/airflow.cfg
RUN chown -R airflow:airflow /home/airflow/airflow

USER airflow
WORKDIR /home/airflow

COPY environment.yml environment.yml

RUN conda env create -f environment.yml \
    && conda clean --all --yes

RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN echo "source activate airflow" >> ~/.bashrc

ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /home/airflow/.conda/envs/airflow
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (airflow)
ENV CONDA_DEFAULT_ENV airflow
ENV PATH /home/airflow/.conda/envs/airflow/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

## AIRFLOW CORS
## IF you want CORS on airflow uncomment this
#COPY airflow/airflow_cors.patch /home/airflow
#RUN mv airflow_cors.patch /home/airflow/.conda/envs/airflow/lib && \
#    cd /home/airflow/.conda/envs/airflow/lib && \
#    patch python3.6/site-packages/airflow/www/app.py airflow_cors.patch

# For this tutorial I don't need root access, but if you need to mount a directory with read/write access, just run everything as root
# If you do this tho celery complains, loudly
#USER root
#
#RUN mkdir $HOME/airflow
#RUN cp /home/airflow/airflow/airflow.cfg $HOME/airflow/airflow.cfg
#
#ENV C_FORCE_ROOT true
#ENV CONDA_EXE /opt/conda/bin/conda
#ENV CONDA_PREFIX /opt/conda/envs/airflow
#ENV CONDA_PYTHON_EXE /opt/conda/bin/python
#ENV CONDA_PROMPT_MODIFIER (airflow)
#ENV CONDA_DEFAULT_ENV airflow
#ENV PATH /opt/conda/envs/airflow/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
