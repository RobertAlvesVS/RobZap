import base64
import mimetypes
import os
import re


def salvar_base64_generico(base64_string: str, nome_base_arquivo: str) -> str | None:
    """
    Decodifica qualquer string Base64 (imagem, vídeo, áudio) e salva na pasta raiz 'temp_media/'.
    Descobre a extensão automaticamente baseada no cabeçalho do MIME type.

    :param base64_string: A string Base64 completa (com ou sem o prefixo data:)
    :param nome_base_arquivo: O nome do arquivo sem extensão (geralmente o ID da mensagem)
    :return: Retorna o caminho relativo do arquivo salvo (str) ou None se falhar.
    """
    try:
        # 1. Define e garante que a pasta temporária existe na raiz do projeto (fora de app/)
        pasta_destino = "temp_media"

        extensao = (
            ".bin"  # Extensão genérica padrão caso não encontre nenhuma no cabeçalho
        )

        # 2. Se a string contiver o cabeçalho "data:tipo/subtipo;base64,", extrai o tipo e limpa a string
        if "," in base64_string:
            cabecalho, base64_string = base64_string.split(",", 1)

            # Expressão regular para capturar o mime-type (ex: image/jpeg ou video/mp4)
            match = re.search(r"data:(.*?);", cabecalho)
            if match:
                mime_type = match.group(1)
                # Adivinha a extensão certa pelo mime-type (ex: image/jpeg -> .jpg)
                ext_descoberta = mimetypes.guess_extension(mime_type)
                if ext_descoberta:
                    extensao = ext_descoberta

        # 3. Decodifica o texto Base64 de volta para os bytes puros do arquivo
        dados_bytes = base64.b64decode(base64_string)

        # 4. Monta o nome final do arquivo combinando o ID da mensagem e a extensão
        nome_completo_arquivo = f"{nome_base_arquivo}{extensao}"
        caminho_final = os.path.join(pasta_destino, nome_completo_arquivo)

        # 5. Grava os bytes diretamente no disco do container
        with open(caminho_final, "wb") as arquivo:
            arquivo.write(dados_bytes)

        return caminho_final

    except Exception:
        return None
