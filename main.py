import discord
import json
from discord.ext import commands

# Remplacez 'votre_token' par votre token Discord
TOKEN = 'MTI5OTAzMDA0MDAwNDI2NDA2OA.Go100E.m5EBQHjYGP789fsJYIWrILxLaW-aXqumyfqpCc'

# Nom du fichier JSON
JSON_FILE = 'membres.json'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Fonction pour charger les données du fichier JSON
def load_data():
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Attention : Fichier JSON corrompu ou vide. Chargement d'un dictionnaire vide.")
        return {}

# Fonction pour enregistrer les données dans le fichier JSON
def save_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Dictionnaire pour stocker les données des membres (initialisé à partir du fichier JSON)
members_data = load_data()

@bot.event
async def on_ready():
    print(f'Le bot {bot.user} est connecté !')
    # Vérifier tous les membres au démarrage
    for guild in bot.guilds:
        for member in guild.members:
            if not member.guild_permissions.administrator:
                highest_role = max(member.roles, key=lambda r: r.position)
                members_data[str(member.id)] = str(highest_role.id)

    save_data(members_data)

@bot.event
async def on_member_join(member):
    # Ajouter le membre au fichier JSON avec son rôle le plus haut, sauf si c'est un admin
    if not member.guild_permissions.administrator:
        highest_role = max(member.roles, key=lambda r: r.position)
        members_data[str(member.id)] = str(highest_role.id)
        save_data(members_data)

@bot.event
async def on_member_update(before, after):
    # Vérifier si les rôles ont changé et que le membre n'est pas un admin
    if before.roles != after.roles and not after.guild_permissions.administrator:
        # Mettre à jour le rôle le plus haut dans le fichier JSON
        highest_role = max(after.roles, key=lambda r: r.position)
        members_data[str(after.id)] = str(highest_role.id)
        save_data(members_data)

        # Mettre à jour le pseudo du membre
        new_nickname = f"[{highest_role.name}] {after.name}"
        await after.edit(nick=new_nickname)

@bot.event
async def on_member_remove(member):
    # Supprimer le membre du fichier JSON
    members_data.pop(str(member.id), None)
    save_data(members_data)

bot.run(TOKEN)
