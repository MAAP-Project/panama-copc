FROM continuumio/miniconda3:24.1.2-0 as base

COPY environment.yml ./
RUN conda update conda && \
    conda env update -f environment.yml -n base && \
    conda clean -af


FROM base as dependencies

ENV PATH="/opt/conda/bin:$PATH"
WORKDIR /opt/stactools-panama-copc
COPY --from=base /opt/conda /opt/conda
COPY pyproject.toml ./
COPY src/stactools/panama_copc/__init__.py src/stactools/panama_copc/
RUN apt-get -y -q update \
    && apt-get -y -q install build-essential \
    && rm -rf /var/lib/apt/lists/
RUN pip install .
RUN rm -r /opt/conda/lib/python3.11/site-packages/stactools/panama_copc


FROM dependencies as builder

ENV PATH="/opt/conda/bin:$PATH"
WORKDIR /opt/stactools-panama-copc
COPY --from=base /opt/conda /opt/conda
COPY pyproject.toml ./
COPY src ./src
RUN pip install -U pip \
    && pip install .
WORKDIR /
RUN rm -rf /opt/stactools-panama-copc
CMD [ "stac", "panamacopc" ]


FROM dependencies as dev-dependencies

ENV PATH="/opt/conda/bin:$PATH"
WORKDIR /opt/stactools-panama-copc
COPY --from=base /opt/conda /opt/conda
COPY pyproject.toml .
RUN pip install -e '.[dev]' \
    && git init


FROM dev-dependencies as dev-builder

ENV PATH="/opt/conda/bin:$PATH"
WORKDIR /opt/stactools-panama-copc
COPY --from=base /opt/conda /opt/conda
COPY . .
CMD [ "stac", "panamacopc" ]
