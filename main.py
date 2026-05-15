# =========================================================
# COMO ADICIONAR NOVOS COMANDOS
# =========================================================
#
# Copie este modelo:
#
# @bot.tree.command(name="nome", description="Descrição")
# async def nome_comando(interaction: discord.Interaction):
#     await interaction.response.send_message("Resposta")
#
# Exemplo:
#
# @bot.tree.command(name="oi", description="Diz oi")
# async def oi(interaction: discord.Interaction):
#     await interaction.response.send_message("Olá!")
#
# Depois de adicionar:
# 1. Salve o arquivo
# 2. Pare o bot com CTRL + C
# 3. Rode novamente:
#    py main.py
#
# =========================================================


# =========================================================
# IMPORTAÇÕES
# =========================================================

import discord
import os

from discord import app_commands
from discord.ext import commands


# =========================================================
# TOKEN DO BOT
# =========================================================

TOKEN = os.getenv("TOKEN")


# =========================================================
# CONFIGURAÇÃO DOS INTENTS
# =========================================================

intents = discord.Intents.default()
intents.message_content = True


# =========================================================
# CRIAÇÃO DO BOT
# =========================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================================================
# EVENTO DE INICIALIZAÇÃO
# =========================================================
# Executa quando o bot conecta ao Discord

@bot.event
async def on_ready():

    print(f"Bot conectado como {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")

    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")


# =========================================================
# COMANDO /ajuda
# =========================================================
# Mostra todos os comandos disponíveis

@bot.tree.command(
    name="ajuda",
    description="Lista os comandos disponíveis"
)
async def ajuda_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "**Comandos disponíveis:**\n\n"
        "/ajuda - Lista os comandos\n"
        "/links - Mostra links importantes\n"
        "/professor - Mostra orientações gerais\n"
        "/clear - Apaga mensagens do canal"
    )


# =========================================================
# COMANDO /links
# =========================================================
# Mostra links importantes da sala

@bot.tree.command(
    name="links",
    description="Mostra links importantes"
)
async def links_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "**Links importantes:**\n\n"
        "Drive: https://drive.google.com/\n"
        "GitHub: https://github.com/\n"
        "FIAP: https://www.fiap.com.br/"
    )


# =========================================================
# COMANDO /professor
# =========================================================
# Mostra orientações gerais

@bot.tree.command(
    name="professor",
    description="Mostra orientações dos professores"
)
async def professor_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "**Orientações gerais:**\n\n"
        "- Verifique entregas no portal\n"
        "- Organize tarefas por matéria\n"
        "- Leia os critérios da sprint antes de entregar"
    )


# =========================================================
# COMANDO /clear
# =========================================================
# Apaga mensagens do canal

@bot.tree.command(
    name="clear",
    description="Apaga mensagens do canal"
)
@app_commands.describe(
    quantidade="Quantidade de mensagens para apagar"
)
async def clear(
    interaction: main.Interaction,
    quantidade: int
):

    # Verifica permissão
    if not interaction.user.guild_permissions.manage_messages:

        await interaction.response.send_message(
            "Você não tem permissão para usar este comando.",
            ephemeral=True
        )

        return

    # Limite de segurança
    if quantidade < 1 or quantidade > 100:

        await interaction.response.send_message(
            "Escolha uma quantidade entre 1 e 100.",
            ephemeral=True
        )

        return

    # Mensagem inicial
    await interaction.response.send_message(
        f"Apagando {quantidade} mensagens...",
        ephemeral=True
    )

    # Apaga mensagens
    apagadas = await interaction.channel.purge(
        limit=quantidade
    )

    # Mensagem final
    await interaction.followup.send(
        f"{len(apagadas)} mensagens apagadas.",
        ephemeral=True
    )


# =========================================================
# INICIALIZAÇÃO DO BOT
# =========================================================

bot.run(TOKEN)