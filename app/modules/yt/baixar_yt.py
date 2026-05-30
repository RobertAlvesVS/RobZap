import asyncio
import os
import yt_dlp
from app.utils.sender import send_media, send_text


def _executar_download(ydl_opts, video_url):
    """Função síncrona executada em background para não travar o bot"""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extrai informações e baixa o vídeo
        info = ydl.extract_info(video_url, download=True)
        # Retorna o caminho exato e o título do vídeo gerado
        return ydl.prepare_filename(info), info.get("title", "video")


async def baixar_yt(name: str, sender: str, chat: str, text: str):
    video_url = text.split(" ", 1)[1] if " " in text else None
    if not video_url:
        await send_text(
            chat,
            f"{name}, Para usar o comando /baixar, envie o link do vídeo do YouTube após o comando. Exemplo: /baixar https://www.youtube.com/watch?v=example",
        )
        return
    print(f"Recebido comando de {name} para baixar vídeo: {video_url}")
    # Ajustado para forçar MP4 leve (limite de 1080p) para o WhatsApp aceitar sem problemas
    ydl_opts = {
        "format": "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": "temp_media/%(title)s.%(ext)s",
        "quiet": True,
        "cookiefile": "cookies.txt",
    }

    try:
        print("Iniciando o download de forma remota...")

        # Executa o download pesado em uma thread separada
        loop = asyncio.get_running_loop()
        caminho_arquivo, titulo_video = await loop.run_in_executor(
            None, _executar_download, ydl_opts, video_url
        )

        print(f"Download concluído: {caminho_arquivo}")

        # Verifica se o arquivo realmente foi gerado antes de tentar ler
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "rb") as f:
                conteudo_bytes = f.read()

            # Garante que o nome do arquivo enviado tenha a extensão correta que o yt-dlp baixou
            extensao = os.path.splitext(caminho_arquivo)[1]  # Pega ex: '.mp4' ou '.mkv'
            filename = f"{titulo_video}{extensao}"

            # Dispara para o seu sender genérico
            await send_media(
                chat=chat,
                tipo="video",  # <--- Informa que o tipo é vídeo
                file=conteudo_bytes,
                filename=filename,  # <--- O sender vai ler o .mp4 daqui e definir o mimetype sozinho
            )

            os.remove(caminho_arquivo)
        else:
            await send_text(chat, "❌ Erro: O arquivo de vídeo não foi encontrado.")

    except Exception as e:
        print(f"Erro no processo de download/envio: {e}")
        await send_text(
            chat, "❌ Desculpe, ocorreu um erro ao tentar processar este vídeo."
        )
