import discord
client = discord.Client()

SERVER_NAME = "pybottest"
SERVER_ID = "252561414940655618"
tableDict = {}

class Table: #each table is a class :D
    def __init__(self, tableNumber):
        self.tableNumber = tableNumber
        
    async def create(self,host):
        self.tableHost = host
        
        self.tableHostRole = await client.create_role(client.get_server(SERVER_ID), name = ("table_"+str(self.tableNumber)+" Host"), permissions = discord.Permissions.none(), colour = discord.Colour(0x00FFEB), hoist = False, mentionable = False)       
        await client.add_roles(host, self.tableHostRole)

        self.tablePlayerRole = await client.create_role(client.get_server(SERVER_ID), name = ("table_"+str(self.tableNumber)+" Player"), permissions = discord.Permissions.none(), colour = discord.Colour(0x87FF05), hoist = False, mentionable = False)       

        defaultPermissions = discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=False)
        tableHostPermissions = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
        tablePlayerPermissions = discord.PermissionOverwrite(read_messages=True, send_messages=False, connect=True)
        
        self.textChannel = await client.create_channel(client.get_server(SERVER_ID), "table_"+str(self.tableNumber), (client.get_server(SERVER_ID).default_role, defaultPermissions), (self.tableHostRole, tableHostPermissions), (self.tablePlayerRole, tablePlayerPermissions))
        self.voiceChannel = await client.create_channel(client.get_server(SERVER_ID), "table_"+str(self.tableNumber), (client.get_server(SERVER_ID).default_role, defaultPermissions), (self.tableHostRole, discord.PermissionOverwrite(connect=True)), (self.tablePlayerRole, discord.PermissionOverwrite(connect=True)), type = discord.ChannelType(2))

    async def invite(self, player):
        if player.name not in(self.tableHost.name, "pybot"):
            await client.add_roles(player, self.tablePlayerRole)
        else:
            await client.send_message(self.textChannel, "You cannot invite user.")
        
    async def remove(self):
        await client.delete_channel(self.textChannel)
        await client.delete_channel(self.voiceChannel)
        await client.delete_role(client.get_server(SERVER_ID), self.tableHostRole)
        await client.delete_role(client.get_server(SERVER_ID), self.tablePlayerRole)
        
async def createTable(host):
    nextTable=1
    while nextTable in tableDict:
        nextTable+=1
    tableDict[nextTable] = Table(nextTable)
    await tableDict[nextTable].create(host)

def removeTableDict(currenttable):
    del tableDict[currenttable]

def checkMessage(command, channel, message):
    return message.author.name!="pybot" and message.content.startswith(command) and message.channel.name.startswith(channel)
        
        
@client.event
async def on_message(message):
    if checkMessage("create new table", "lobby", message):
        await createTable(message.author)

    if checkMessage("leave table", "table", message):
        tableNumber = int(message.channel.name.split("_")[-1])
        await tableDict[tableNumber].remove()
        removeTableDict(tableNumber)

    if checkMessage("invite", "table", message):
        try:
            tableNumber = int(message.channel.name.split("_")[-1])
            await tableDict[tableNumber].invite(client.get_server(SERVER_ID).get_member_named(message.content.split()[-1]))
        except:
            await client.send_message(message.channel, message.content.split()[-1]+" was not found.")
        
@client.event
async def on_ready():
    print("stated")

client.run("MjUyNTYxMDU5ODY3NjU2MTkz.CxzvZA.PzIk2JMF0AoMmQ5k-JzyIvBxF9Y")

