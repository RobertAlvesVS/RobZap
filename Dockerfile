# Stage 1: Usar a imagem oficial do uv para preparar o ambiente
FROM astral-sh/uv:python3.14-bookworm-slim AS builder

# Ativar a compilação de bytes do Python para acelerar a inicialização do container
ENV UV_COMPILE_BYTECODE=1

# Definir o diretório de trabalho interno
WORKDIR /app

# Sincronizar e instalar as dependências primeiro (aproveita o cache do Docker)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Stage 2: Imagem final de execução (limpa e sem o binário do uv)
FROM python:3.14-slim-bookworm

WORKDIR /app

# 🔴 Instala o FFmpeg (Obrigatório para o funcionamento correto do yt-dlp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copia o ambiente virtual criado pelo uv do estágio anterior
COPY --from=builder /app/.venv /app/.venv

# Copia o código da sua aplicação para o container
COPY . /app

# Coloca o ambiente virtual no PATH para que o python e uvicorn rodem direto dele
ENV PATH="/app/.venv/bin:$PATH"

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8002

# Comando para iniciar o seu Bot/API com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]