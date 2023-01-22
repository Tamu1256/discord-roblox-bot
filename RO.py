from discord import ui,Webhook
import aiohttp
from discord.ext import commands,tasks
import os
import discord
import json
import time
import datetime
import asyncio
import aiomysql
import time
async def dtnow():
    dt = datetime.datetime.now()
    dt = dt.replace(microsecond = 0)
    return dt
class Mybot(commands.Bot):
    print("2")
    def __init__(self):
        print("4")
        intents = discord.Intents.all()
        activity = discord.Activity(type=discord.ActivityType.listening, name="Commands")
        super().__init__(command_prefix="w", intents=intents, activity=activity)
    async def setup_hook(self):
        print("OK")
        bot.pool = await aiomysql.create_pool(host="localhost", port=3306,
        user='root', password='', db="",charset='utf8',autocommit=True)
    


async def timestamp():
    return "<t:"+ str(int(time.time()))+":d>" + "<t:"+ str(int(time.time()))+":T>"

key = ""

ver01 = '1'

intents = discord.Intents.default()

intents.message_content = True
intents.messages = True
intents.members = True
bot = Mybot() #commands.Bot(command_prefix="w",help_command=None,intents=intents)

@bot.listen()
async def on_ready():
    ch = bot.get_channel()
    e = discord.Embed(title='フレンド募集掲示板', description="このフレンド募集掲示板に掲載して、フレンドを作りましょう！" + 
    "\n**UP**：24時間に1回実行できます。あなたの情報を再送信します。"
    "\n**設定**：掲示板にあなたの情報を登録します。"
    "\n**説明**：詳しい使い方を送信します。",color=0x0080ff)
    try:
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM friend WHERE uid = " + str(0)+";")
                r = await cur.fetchall()
                old_msg = await ch.fetch_message(r[0][7])
                await old_msg.delete()
    except:
        pass
    m = await ch.send(embed=e,view = Friendutton())
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("CREATE TABLE if not exists friend(uid BIGINT UNSIGNED,username TEXT,disname TEXT,myself TEXT,games TEXT,time BIGINT,up INT,mid BIGINT UNSIGNED,tid BIGINT UNSIGNED,con TEXT) DEFAULT CHARSET=utf8;")
            d = "0"
            d += "," + str(m.id)
            
            await cur.execute("SELECT EXISTS(SELECT * FROM friend WHERE uid = " + str(0)+ ");")
            r = await cur.fetchall()
            if 0 == r[0][0]:
                await cur.execute("INSERT INTO friend(uid,mid) VALUES (" + d+ ");")
            else:
                await cur.execute("UPDATE friend SET mid = " + str(m.id)+" WHERE uid = " + str(0)+";")
    
class Friendutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Friendutton_2("UP",discord.ButtonStyle.green,"⤴"))
        self.add_item(Friendutton_2("設定",discord.ButtonStyle.blurple,"⚙"))
        self.add_item(Friendutton_2("説明",discord.ButtonStyle.grey,"📔"))

class Friendutton_2(discord.ui.Button):
    def __init__(self,text,c,n, timeout=None):
        super().__init__(label=text,style=c,emoji=discord.PartialEmoji(name=n))

    async def callback(self,interaction:discord.Interaction):
        if self.label == "UP":
            async with bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT EXISTS(SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+ ");")
                    r = await cur.fetchall()
                    if 1 == r[0][0]:
                        await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                        r = await cur.fetchall()
                        if int(time.time()) >= r[0][5]:
                            await cur.execute("UPDATE friend SET time = " + str((time.time()) + 5)+" WHERE uid = " + str(interaction.user.id)+";")
                            embed = discord.Embed(title='フレンド掲示板', description="表示順をアップしたよ！",color=0x00ffff)
                            await interaction.response.send_message(embed=embed,ephemeral=True)
                            async with aiohttp.ClientSession() as session:
                                ch = bot.get_channel()
                                guild = bot.get_guild(interaction.guild.id)
                                member = guild.get_member(interaction.user.id)
                                webhook = Webhook.from_url("https://discord.com/api/webhooks", session=session)
                                c = "**ROBLOXユーザー名**：" + str(r[0][1])
                                c += "\n**ROBLOX表示名**：" + str(r[0][2])
                                c += "\n**自己紹介**：" + str(r[0][3])
                                c += "\n**よく遊ぶ体験**：" + str(r[0][4])
                                c += "\n**申請条件**：" + str(r[0][9])
                                if 0 == r[0][8]:
                                    
                                    th = await ch.create_thread(name=member.display_name)
                                    await cur.execute("UPDATE friend SET tid = " + str(th.id)+" WHERE uid = " + str(interaction.user.id)+";")
                                await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                                r = await cur.fetchall()
                                th = ch.get_thread(r[0][8])
                                thread = discord.Embed(title=None,description="[この人にフレンド申請する](" +str(th.jump_url)+")",color=0x0080ff)
                                await webhook.send(content=c, embed=thread,username=member.display_name,avatar_url=member.display_avatar.url)
                                msg = ch.last_message_id
                                if 0 == r[0][7]:
                                    await cur.execute("UPDATE friend SET mid = " + str(msg)+" WHERE uid = " + str(interaction.user.id)+";")
                                    
                                    
                                else:
                                    await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                                    r = await cur.fetchall()
                                    await cur.execute("UPDATE friend SET mid = " + str(msg)+" WHERE uid = " + str(interaction.user.id)+";")
                                    await webhook.delete_message(int(r[0][7]))
                                
                        else:
                            
                            await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                            r = await cur.fetchall()
                            i = r[0][5] - int(time.time())
                            embed = discord.Embed(title='フレンド掲示板',description= "あと" + str(time.strftime("%H時間%M分%S秒", time.gmtime(i))),color=0xff5050)
                            await interaction.response.send_message(embed=embed,ephemeral=True)
                        async with bot.pool.acquire() as conn:
                            async with conn.cursor() as cur:
                                await cur.execute("SELECT * FROM friend WHERE uid = " + str(0)+";")
                                r = await cur.fetchall()
                                old_msg = await ch.fetch_message(r[0][7])
                                await old_msg.delete()
                                ch = bot.get_channel()
                                e = discord.Embed(title='フレンド募集掲示板', description="このフレンド募集掲示板に掲載して、フレンドを作りましょう！" + 
                                "\n**UP**：24時間に1回実行できます。あなたの情報を再送信します。"
                                "\n**設定**：掲示板にあなたの情報を登録します。"
                                "\n**説明**：詳しい使い方を送信します。",color=0x0080ff)
                                m = await ch.send(embed=e,view = Friendutton())
                                await cur.execute("UPDATE friend SET mid = " + str(m.id)+" WHERE uid = " + str(0)+";")
                    if 0 == r[0][0]:
                        embed = discord.Embed(title='フレンド掲示板[エラー]',description= "あなたの情報は登録されていません。\n「設定」ボタンを押して、あなたの情報を登録してください。",color=0xff5050)
                        await interaction.response.send_message(embed=embed,ephemeral=True)
        if self.label == "設定":
            await interaction.response.send_modal(Friend_Setting_Modal(interaction))
        if self.label == "説明":
            embed = discord.Embed(title='使用方法',description="フレンド募集掲示板は、Robloxのフレンドを募集できるRoblox好きの集い独自の掲示板です。\nここにあなたの情報を掲載して、Robloxのフレンドを募りましょう！",color=0x808080)
            embed.add_field(name="掲載方法",value="①「設定」ボタンを押してください。\n②フォームに記入して、送信してください。\n→掲示板に掲載されます！\n→フレンド申請は、あなた専用のスレッドに届きます！",inline=False)
            embed.add_field(name="UPについて",value="しかし、掲載しただけだと他の人の投稿にすぐ埋もれてしまいます。\nそこで、24時間に1回「UP」をすることで、あなたの情報を再掲載することができます。",inline=False)
            embed.add_field(name="使用ルール",value="・コミュニティルールを守ってください。\n・自分自身のアカウントのみ掲載できます。\n・1アカウントにつき1つのRobloxアカウントを掲載できます。\n・1人につき1アカウント使用できます。サブ垢等で登録するのは禁止です。\n・申請前に必ずスレッドで募集主に一声かけましょう。また、申請条件を確認した上で申請しましょう。",inline=False)
            embed.set_footer(text="Bot制作者：Tamu1256tt",icon_url="https://images-ext-1.discordapp.net/external/HjO8QJoYzVJYh9HzawE-4570h42QgeZV6tVx_oSqcoA/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/831453621732245534/ee9ecb17a093674a56043f2fa2f874fc.png")
            await interaction.response.send_message(embed=embed,ephemeral=True)
class Friend_Setting_Modal(discord.ui.Modal):
    def __init__(self,inter):
        super().__init__(title="設定")
        self.user_name = ui.TextInput(label="ROBLOXユーザー名", style=discord.TextStyle.short,placeholder="例：Roblox")
        self.dis_name = ui.TextInput(label="ROBLOX表示名", style=discord.TextStyle.short,placeholder="例：RobloxPro")
        self.my_self = ui.TextInput(label="自己紹介", style=discord.TextStyle.short,placeholder="例：PvP系の体験をよくやっています。")
        self.games = ui.TextInput(label="よく遊ぶ体験", style=discord.TextStyle.short,placeholder="例1：Arsenal　例2：Arsenalなど、PvP系")
        self.con = ui.TextInput(label="申請条件", style=discord.TextStyle.short,placeholder="例1：誰でもOKです！　例2：PvP系の体験が好きな方 ")
        self.add_item(self.user_name)
        self.add_item(self.dis_name)
        self.add_item(self.my_self)
        self.add_item(self.games)
        self.add_item(self.con)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="設定変更成功", description=
        "ROBLOXユーザー名：" + str(self.user_name.value) +
        "\nROBLOX表示名：" + str(self.dis_name.value) +
        "\n自己紹介：" + str(self.my_self.value) +
        "\nよく遊ぶ体験：" + str(self.games.value) +
        "\n申請条件：" + str(self.con.value)
        ,color=0x00ff00)
        embed.set_footer(text=str(await dtnow()))
        async with bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("CREATE TABLE if not exists friend(uid BIGINT UNSIGNED,username TEXT,disname TEXT,myself TEXT,games TEXT,time BIGINT,up INT,mid BIGINT UNSIGNED,tid BIGINT UNSIGNED,con TEXT) DEFAULT CHARSET=utf8;")
                d = str(interaction.user.id)
                d += ",'" + str(self.user_name.value)
                d += "','" + str(self.dis_name.value)
                d += "','" + str(self.my_self.value)
                d += "','" + str(self.games.value)
                d += "'," + str(int(time.time()))
                d += "," + str(1)
                d += ",0"
                d += ",0" 
                d += ",'" + str(self.con.value) + "'"
                await cur.execute("SELECT EXISTS(SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+ ");")
                r = await cur.fetchall()
                if 0 == r[0][0]:
                    await cur.execute("INSERT INTO friend(uid,username,disname,myself,games,time,up,mid,tid,con) VALUES (" + d+ ");")
                    await cur.execute("UPDATE friend SET time = " + str((time.time()) + 999999)+" WHERE uid = " + str(interaction.user.id)+";")
                    embed = discord.Embed(title='Friend掲示板', description="表示順をアップしたよ！",color=0x00ffff)
                    await interaction.response.send_message(embed=embed,ephemeral=True)
                    async with aiohttp.ClientSession() as session:
                        await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                        r = await cur.fetchall()
                        ch = bot.get_channel()
                        guild = bot.get_guild(interaction.guild.id)
                        member = guild.get_member(interaction.user.id)
                        webhook = Webhook.from_url("https://discord.com/api/webhooks", session=session)
                        c = "**ROBLOXユーザー名**：" + str(r[0][1])
                        c += "\n**ROBLOX表示名**：" + str(r[0][2])
                        c += "\n**自己紹介**：" + str(r[0][3])
                        c += "\n**よく遊ぶ体験**：" + str(r[0][4])
                        c += "\n**申請条件**：" + str(r[0][9])
                        if 0 == r[0][8]:
                            
                            th = await ch.create_thread(name=member.display_name)
                            await cur.execute("UPDATE friend SET tid = " + str(th.id)+" WHERE uid = " + str(interaction.user.id)+";")
                        await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                        r = await cur.fetchall()
                        th = ch.get_thread(r[0][8])
                        thread = discord.Embed(title=None,description="[この人にフレンド申請する](" +str(th.jump_url)+")",color=0x0080ff)
                        await webhook.send(content=c, embed=thread,username=member.display_name,avatar_url=member.display_avatar.url)
                        msg = ch.last_message_id
                        if 0 == r[0][7]:
                            await cur.execute("UPDATE friend SET mid = " + str(msg)+" WHERE uid = " + str(interaction.user.id)+";")
                            
                            
                        else:
                            await cur.execute("SELECT * FROM friend WHERE uid = " + str(interaction.user.id)+";")
                            r = await cur.fetchall()
                            await cur.execute("UPDATE friend SET mid = " + str(msg)+" WHERE uid = " + str(interaction.user.id)+";")
                            await webhook.delete_message(int(r[0][7]))
                        async with bot.pool.acquire() as conn:
                            async with conn.cursor() as cur:
                                await cur.execute("SELECT * FROM friend WHERE uid = " + str(0)+";")
                                r = await cur.fetchall()
                                old_msg = await ch.fetch_message(r[0][7])
                                await old_msg.delete()
                                ch = bot.get_channel()
                                e = discord.Embed(title='フレンド募集掲示板', description="このフレンド募集掲示板に掲載して、フレンドを作りましょう！" + 
                                "\n**UP**：24時間に1回実行できます。あなたの情報を再送信します。"
                                "\n**設定**：掲示板にあなたの情報を登録します。"
                                "\n**説明**：詳しい使い方を送信します。",color=0x0080ff)
                                m = await ch.send(embed=e,view = Friendutton())
                                await cur.execute("UPDATE friend SET mid = " + str(m.id)+" WHERE uid = " + str(0)+";")
                if 1 == r[0][0]:
                    await cur.execute("UPDATE friend SET " + 
                    "username = '" + str(self.user_name.value) +
                    "' ,disname = '" + str(self.dis_name.value) +
                    "' ,myself = '" + str(self.my_self.value) +
                    "' ,games = '" + str(self.games.value) +
                    "' ,up = " + str(0) +
                    ",con = '" + str(self.con.value) + "'" + 
                    " WHERE uid = " + str(interaction.user.id)+";")
                #await cur.execute("UPDATE time SET time = " + str((time.time()))+";")
                #await cur.execute("SELECT * FROM time;")
                
                r = await cur.fetchall()
        await interaction.response.send_message(embed=embed,ephemeral=True)

@bot.listen()
async def on_message(message):
    pass
@bot.command(aliases=['.'])
async def wiki_is_here_url(ctx,st:str):
    await ctx.send("https://" + st)
    pass


bot.run(key)
