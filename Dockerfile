FROM continuumio/miniconda3:4.5.11

RUN apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y \
    vim-tiny vim-athena ssh openssh-server build-essential

RUN adduser --home /home/airflow airflow

RUN mkdir -p /home/airflow/airflow
RUN mkdir -p /home/airflow/.ssh
COPY airflow/airflow.cfg /home/airflow/airflow/airflow.cfg
COPY airflow/airflow_cors.patch /home/airflow
RUN chown -R airflow:airflow /home/airflow/airflow
RUN chown -R airflow:airflow /home/airflow/.ssh

USER airflow
WORKDIR /home/airflow

COPY environment.yml environment.yml

RUN conda env create -f environment.yml
RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN echo "source activate airflow" >> ~/.bashrc

ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /home/airflow/.conda/envs/airflow
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (airflow)
ENV CONDA_DEFAULT_ENV airflow
ENV PATH /home/airflow/.conda/envs/airflow/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN mv airflow_cors.patch /home/airflow/.conda/envs/airflow/lib && \
    cd /home/airflow/.conda/envs/airflow/lib && \
    patch python3.6/site-packages/airflow/www/app.py airflow_cors.patch

# For this tutorial I don't need root access, but if you need to mount a directory with read/write access, just run everything as root
# If you do this tho celery complains, loudly
#USER root
#
#RUN mkdir $HOME/airflow
#RUN cp /home/airflow/airflow/airflow.cfg $HOME/airflow/airflow.cfg
#
#ENV C_FORCE_ROOT true
#ENV CONDA_EXE /opt/conda/bin/conda
#ENV CONDA_PREFIX /home/airflow/.conda/envs/airflow
#ENV CONDA_PYTHON_EXE /opt/conda/bin/python
#ENV CONDA_PROMPT_MODIFIER (airflow)
#ENV CONDA_DEFAULT_ENV airflow
#ENV PATH /home/airflow/.conda/envs/airflow/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
