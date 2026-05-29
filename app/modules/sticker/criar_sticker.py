# app/modules/sticker/criar_sticker.py
import os
from app.utils.media_helper import salvar_base64_generico
from app.utils.sender import send_sticker_url


async def criar_sticker(chat: str, message_id: str, data: dict):
    """Lê o base64 do webhook, salva no container e envia como sticker via rede interna"""
    message = data.get("Message", {})
    base64_puro = message.get("base64")

    if not base64_puro:
        print("❌ Erro: O webhook não trouxe o campo 'base64'.")
        return

    # 1. Garante que o base64 tenha o cabeçalho correto para a função genérica extrair a extensão (.jpg)
    if not base64_puro.startswith("data:"):
        mimetype = message.get("imageMessage", {}).get(
            "mimetype", "image/jpeg"
        )
        base64_completo = f"data:{mimetype};base64,{base64_puro}"
    else:
        base64_completo = base64_puro

    # 2. Salva o arquivo usando a sua função genérica (vai para temp_media/)
    caminho_salvo = salvar_base64_generico(base64_completo, message_id)

    if not caminho_salvo:
        print("❌ Erro ao tentar salvar o arquivo base64 no disco.")
        return

    try:
        # 3. Pega o nome do arquivo gerado (ex: '3EB0546D154AB4C90A11E1.jpg')
        nome_arquivo = os.path.basename(caminho_salvo)

        # 4. Monta a URL usando o nome do serviço do seu FastAPI na rede do Docker
        # Substitua 'bot-fastapi:8000' pelo nome/porta real do seu service do compose
        url_interna_docker = (
            f"http://192.168.100.159:8000/temp_media/{nome_arquivo}"
        )

        print(f"📡 Solicitando sticker via Docker: {url_interna_docker}")

        # 5. Envia a URL para a Evolution API buscar de dentro do Docker
        await send_sticker_url(chat, url_interna_docker)

    except Exception as e:
        print(f"❌ Erro no processo de criação/envio do sticker: {e}")

    finally:
        # 6. Limpeza do arquivo temporário local para não entupir o HD
        if caminho_salvo and os.path.exists(caminho_salvo):
            os.remove(caminho_salvo)
            print("🧹 Arquivo temporário do sticker removido do container.")
        pass
