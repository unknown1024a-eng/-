import asyncio
import datetime
import json
import os
import random
import string
from googleapiclient.discovery import build
from deep_translator import GoogleTranslator
from threading import Thread
import aiohttp
import time
import discord
from discord.ext import commands
from flask import Flask
from googletrans import Translator

translator = Translator()

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

bot = commands.Bot(command_prefix='!', self_bot=True, help_command=None, reconnect=True)

target_id = None
target_name = ""
gungsung_active = False
gungsung_msg = ""
gungsung_delay = 0.2

spam_active = False
spam_msg = ""
spam_delay = 0.2

spam_channel = None

auto_emoji = False
emoji_type = "🖕"
typing_lock = False
bad_loop = False
zombie_loop = False
god_loop = False
group_loop = False
장애타_루프 = False

mimic_active = False
smart_mimic = False
reaction_active = False
react_emoji = "🖕"
bank_info = "등록된 계좌가 없습니다."

counter_list = [
    "닥쳐 좀 ㅋㅋㅋㅋㅋㅋ",
    "왜 안닥쳐 ㅋㅋㅋㅋ",
    "아니 닥치라니깐?ㅋㅋㅋㅋ",
    "아가리찢어버리기전에닥쳐ㅋㅋㅋ",
    "뭐이리 말이 많아 닥쳐 좀 ㅋㅋ",
    "너 재미없다고 닥치라고 ㅋㅋ"
]

근성_loop = False
근성_seconds = 1.0
근성_text = None
근성_channel = None

도배_loop = False
도배_seconds = 1.0
도배_text = None
도배_channel = None

mention_loop = False
mention_target = None
mention_delay = 1.0
mention_channel = None

typing_loop = False
typing_channel = None

group_seconds = 1.5
group_name_val = None
group_channel = None

jail_speed = 1.0
장애타_channel = None

mention_jail_loop = False
mention_jail_target = None
mention_jail_speed = 1.0
mention_jail_channel = None

VOICE_BACKUP_FILE = "voice_backup.json"

장애타_리스트 = [
    "개새기야시발새기야고아새기야장애새기야버러지새기야개진다새기야개좆같은새기야개자페아새기야",
    "애미애비창녀새끼야미친새끼야미친척하지마개농아새기야종자새기야개스래기새기야애미애비게보지새기야",
    "애미애비갖다가패기전에갖다꺼져니애미애비강형욱블로킹조지니깐낑낑대면서달아나는새끼야",
    "애미갖다가먹어버리기전에닥쳐시발새기야개새기야상그지새기야개드러븐새기야개같은새기야",
    "애미애비벌레새기야하등한새기야자페아새기야개벌레새기야개미친새기야어멍다리뒤진새기야",
    "애미디진새기야시발새기야샹고아새기야미친새기야개벌레새기야샹그지새기야미친새기야",
    "개벌레새기야샹고아새기야시발새기야개미친새기야샹그지새기야개고아새기야개벌레새기야",
    "애미줘터진새기야진다새기야개벌레새기야샹그지새기야개고아새기야개그지새기야개어망구뒤진새기야",
    "개미친새기야시발새기야샹그지새기야개벌레새기야농아새기야미친새기야농아새기야종자새기야",
    "야라이시발새기야대가리아둔한새기야개멍청한진다새기야개벌레새기야애미애비창녀촌에서일하는새기야",
    "미친새기야시발새기야샹그지새기야좆같은새기야멍청한새기야애미애비개창녀새기야개진다새기야",
    "개좆같은농아새기야기형아새기야개벌레새기야좆같은장애인새기야미친새기야시발새기야샹고아새기야", 
    "미친년아시발새기야개장애인새기야고아새기야개벌레새기야개장애인새기야시발새기야미친새기야시발새기야개고아새기야",
    "개좆같은장애인새기야시발새기야개벌레새기야샹고아새기야시발새기야개벌레새기야말뒤지게못하는새기야",
    "느금마보지개보지말봉지십봉지개보지물봉지시발새기야미친새기야느금마보지좆같이딱딱한새기야시발새기야",
    "시발새기야미친새기야개장애인새기야샹그지새기야시발새기야개벌레새기야개하등한새기야개자페아새기야거렁뱅이새기야",
    "샹그지새기야시발좆같은년아개같은새기야대가리갖다가찍어버리기전에꺼져",
    "벌레새기야시발새기야개장애인새기야개병신새기야개비응신새기야거러지새기야",
    "미친년아시발새기야개장애인새기야개거렁뱅이새기야버러지새기야농아새기야",
    "좆같은벌레새기야꿈틀거리지마벌레새기야생각도못하는장애새기야고아새기야",
    "시발새기야미친새기야샹고아새기야상그지새기야개드러븐새기야개스래기새기야",
    "애미창녀새기야디진새기야시발새기야애미애비개창녀새기야개상그지새기야버러지새기야",
    "좆같은새기야씨발년아개장애인새기야애미애비갖다가패기전에꺼져개진다새기야농아새기야",
    "멍청한새기야개벌레새기야타속좆같이느린새기야거러지새기야손가락존나뚱뚱한새기야",
    "애미줘터진새기야진다새기야개벌레새기야개농아새기야개종자새기야개창녀새기야개보지새기야",
    "니뭐해벌레새기야시발새기야아둔한새기야개벌레새기야개거렁뱅이새기야말도못하는개장애새기야",
    "좆같은새기야시발새기야개벌레새기야개스래기새기야개미친새기야스래기새기야드러븐새기야",
    "씨발새기야미친새기야개장애인새기야샹고아새기야패기전에갖다꺼져진다새기야종자새기야",
    "좆장애인새기야벌레새기야시발새기야미친새기야그지새기야버러지거러지새기야",
    "애미디진장애인새기야샹고아새기야애미애비와사바리털어버릴라시발새기야개새기야",
    "벌레새기야시발새기야개장애인년아시발새기야애미창녀새기야애미갖다가먹어버리기전에닥쳐",
    "미친년아장애인새기야시발새기야개장애인새기야샹그지새기야개벌레새기야샹고아새기야미친년아시발새기야개벌레새기야개장애인년아",
    "시발년아장애인새기야대가리아둔한새기야미친새기야스래기새기야드러븐새기야",
    "벌레년아시발새기야개장애인새기야좆같은새기야개진다새기야개기형아새기야",
    "시발새기야미친새기야타속좆같이느린애미줘터진진다새기야시발새기야",
    "애미디진스레기새기야시발새기야개자페아새기야애미개보지새기야개진다새기야",
    "샹그지새기야개벌레새기야샹고아새기야애미애비개씨발새끼야병신새기야",
    "에미디진장애인새기야샹고아새기야말상좆같이못하는새기야개고아새기야",
    "야라이시발새기야개미친새기야농아새기야스레기새기야시발새기야미친새기야",
    "애미창녀새기야진다새기야개벌레새기야개고아새기야거지새기야상그지좆같은새기야",
    "샹고아새기야미친새기야시발새기야미친새기야개장애인새기야샹고아새기야",
    "씨발새기야미친새기야샹그지새기야시발미친새기야개농아새기야외소형새기야장애새기야",
    "미친년아장애인농아버러지새기야개좆븅신새기야개좆만한새기야개거지새기야",
    "개씹좆같은장애인애미기형아새기야개벌레새기야존나만만한새기야말도못하는장애새기야",
    "좆같은자폐아새기야미친새기야샹그지새기야대가리아둔한새기야상그지새기야",
    "미친새기야개벌레새기야샹그지새기야미친새기야개자페아새기야거지새기야",
]

async def background_vote_task():
    while True:
        try:
            if vote_config["is_running"] and vote_config["title"] and vote_config["options"] and vote_config["channel"]:
                rand_num = random.randint(100000, 999999)
                poll_title = f"{vote_config['title']} {rand_num}"

                poll = discord.Poll(question=poll_title, duration=datetime.timedelta(hours=24))
                
                for opt in vote_config["options"]:
                    poll.add_answer(text=opt)

                await vote_config["channel"].send(poll=poll)
                await asyncio.sleep(vote_config["interval"])
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_근성_task():
    global 근성_loop, 근성_seconds, 근성_text, 근성_channel
    while True:
        try:
            if 근성_loop and 근성_text and 근성_channel:
                rand_num = random.randint(100000, 999999)
                msg = f"{근성_text}\n\n`{rand_num}`"
                await 근성_channel.send(msg)
                await asyncio.sleep(근성_seconds)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_도배_task():
    global 도배_loop, 도배_seconds, 도배_text, 도배_channel
    while True:
        try:
            if 도배_loop and 도배_text and 도배_channel:
                rand_num = random.randint(100000, 999999)
                msg = f"{도배_text}\n\n`{rand_num}`"
                await 도배_channel.send(msg)
                await asyncio.sleep(도배_seconds)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_멘션_task():
    global mention_loop, mention_target, mention_delay, mention_channel
    while True:
        try:
            if mention_loop and mention_target and mention_channel:
                random_num = random.randint(100000, 999999)
                msg = f"{mention_target.mention}\n\n`{random_num}`"
                await mention_channel.send(msg)
                await asyncio.sleep(mention_delay)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_입력_task():
    global typing_loop, typing_channel
    while True:
        try:
            if typing_loop and typing_channel:
                async with typing_channel.typing():
                    await asyncio.sleep(9.0)
            else:
                await asyncio.sleep(0.1)
        except Exception:
            await asyncio.sleep(1)

async def background_그룹_task():
    global group_loop, group_seconds, group_name_val, group_channel
    while True:
        try:
            if group_loop and group_name_val and group_channel:
                rand_num = random.randint(100000, 999999)
                random_spaces = " " * random.randint(1, 5)
                new_title = f"{group_name_val} {rand_num}{random_spaces}"
                await group_channel.edit(name=new_title)
                await asyncio.sleep(group_seconds)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_장애타_task():
    global 장애타_루프, 장애타_리스트, jail_speed, 장애타_channel
    while True:
        try:
            if 장애타_루프 and 장애타_리스트 and 장애타_channel:
                for 문장 in 장애타_리스트:
                    if not 장애타_루프:
                        break
                    await 장애타_channel.send(문장)
                    await asyncio.sleep(jail_speed)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

async def background_멘션타_task():
    global mention_jail_loop, mention_jail_target, mention_jail_speed, mention_jail_channel
    while True:
        try:
            if mention_jail_loop and mention_jail_target and mention_jail_channel and 장애타_리스트:
                for 문장 in 장애타_리스트:
                    if not mention_jail_loop:
                        break
                    msg = f"<@{mention_jail_target}> {문장}"
                    await mention_jail_channel.send(msg)
                    await asyncio.sleep(mention_jail_speed)
            else:
                await asyncio.sleep(0.1)
        except discord.HTTPException:
            await asyncio.sleep(2)
        except Exception:
            await asyncio.sleep(1)

def save_voice_backup(guild_id, channel_id):
    data = {}
    if os.path.exists(VOICE_BACKUP_FILE):
        try:
            with open(VOICE_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            pass
    data[str(guild_id)] = channel_id
    with open(VOICE_BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_voice_backup(guild_id):
    if os.path.exists(VOICE_BACKUP_FILE):
        try:
            with open(VOICE_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(str(guild_id))
        except:
            pass
    return None

def remove_voice_backup(guild_id):
    if os.path.exists(VOICE_BACKUP_FILE):
        try:
            with open(VOICE_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if str(guild_id) in data:
                del data[str(guild_id)]
                with open(VOICE_BACKUP_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            pass

def save_global_backup(guild_id, data):
    with open(f"backup_{guild_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_global_backup(guild_id):
    try:
        with open(f"backup_{guild_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@bot.event
async def setup_hook():
    bot.loop.create_task(background_vote_task())
    bot.loop.create_task(background_근성_task())
    bot.loop.create_task(background_도배_task())
    bot.loop.create_task(background_멘션_task())
    bot.loop.create_task(background_입력_task())
    bot.loop.create_task(background_그룹_task())
    bot.loop.create_task(background_장애타_task())
    bot.loop.create_task(background_멘션타_task())

@bot.command(name="서버복사")
async def 서버복사(ctx):
    if not ctx.guild:
        await ctx.send("서버 내에서만 사용할 수 있는 명령어입니다.")
        return
    
    guild = ctx.guild
    
    backup_data = {
        "roles": [],
        "categories": [],
        "channels": []
    }
    
    roles = sorted([r for r in guild.roles if not r.managed and r != guild.default_role], key=lambda r: r.position, reverse=True)
    for role in roles:
        backup_data["roles"].append({
            "name": role.name,
            "permissions": role.permissions.value,
            "color": role.color.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable
        })
        
    def get_channel_overwrites(channel):
        overwrites_data = {}
        for target, overwrite in channel.overwrites.items():
            if isinstance(target, discord.Role):
                target_key = f"role_{target.name}"
            elif isinstance(target, discord.Member):
                continue
            else:
                continue
            
            allow, deny = overwrite.pair()
            overwrites_data[target_key] = {
                "allow": allow.value,
                "deny": deny.value
            }
        return overwrites_data

    for category in guild.categories:
        cat_data = {
            "name": category.name,
            "overwrites": get_channel_overwrites(category),
            "channels": []
        }
        
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                cat_data["channels"].append({
                    "type": "text",
                    "name": channel.name,
                    "topic": channel.topic,
                    "slowmode": channel.slowmode_delay,
                    "overwrites": get_channel_overwrites(channel)
                })
            elif isinstance(channel, discord.VoiceChannel):
                cat_data["channels"].append({
                    "type": "voice",
                    "name": channel.name,
                    "bitrate": channel.bitrate,
                    "user_limit": channel.user_limit,
                    "overwrites": get_channel_overwrites(channel)
                })
        backup_data["categories"].append(cat_data)
        
    for channel in guild.text_channels:
        if channel.category is None:
            backup_data["channels"].append({
                "type": "text",
                "name": channel.name,
                "topic": channel.topic,
                "slowmode": channel.slowmode_delay,
                "overwrites": get_channel_overwrites(channel)
            })
            
    for channel in guild.voice_channels:
        if channel.category is None:
            backup_data["channels"].append({
                "type": "voice",
                "name": channel.name,
                "bitrate": channel.bitrate,
                "user_limit": channel.user_limit,
                "overwrites": get_channel_overwrites(channel)
            })
            
    save_global_backup(guild.id, backup_data)
    await ctx.send("``` ♱ 역할 및 채널 권한을 포함하여 서버를 똑같이 복사했습니다. ♱ ```")

@bot.command(name="서버복구")
async def 서버복구(ctx, source_guild_id: int = None):
    if not ctx.guild:
        await ctx.send("서버 내에서만 사용할 수 있는 명령어입니다.")
        return
    
    guild = ctx.guild
    target_id = source_guild_id if source_guild_id else guild.id
    
    data = load_global_backup(target_id)
    if not data:
        await ctx.send("``` ♱ 저장된 서버 복사본이 없습니다. 먼저 !서버복사 를 진행해주세요. ♱ ```")
        return
    
    try:
        created_roles = {}
        created_roles["role_@everyone"] = guild.default_role

        for r_info in data["roles"]:
            try:
                perm = discord.Permissions(r_info["permissions"])
                col = discord.Color(r_info["color"])
                new_role = await guild.create_role(
                    name=r_info["name"],
                    permissions=perm,
                    color=col,
                    hoist=r_info["hoist"],
                    mentionable=r_info["mentionable"]
                )
                created_roles[f"role_{r_info['name']}"] = new_role
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"역할 생성 실패 ({r_info['name']}): {e}")
                
        def build_overwrites(ov_data):
            overwrites = {}
            for target_key, p_values in ov_data.items():
                if target_key in created_roles:
                    role_obj = created_roles[target_key]
                    allow = discord.Permissions(p_values["allow"])
                    deny = discord.Permissions(p_values["deny"])
                    overwrites[role_obj] = discord.PermissionOverwrite.from_pair(allow, deny)
            return overwrites

        for cat_info in data["categories"]:
            try:
                cat_overwrites = build_overwrites(cat_info.get("overwrites", {}))
                new_cat = await guild.create_category(
                    name=cat_info["name"],
                    overwrites=cat_overwrites
                )
                await asyncio.sleep(0.3)
                
                for ch_info in cat_info["channels"]:
                    ch_overwrites = build_overwrites(ch_info.get("overwrites", {}))
                    if ch_info["type"] == "text":
                        await guild.create_text_channel(
                            name=ch_info["name"],
                            category=new_cat,
                            topic=ch_info["topic"],
                            slowmode_delay=ch_info["slowmode"],
                            overwrites=ch_overwrites
                        )
                    elif ch_info["type"] == "voice":
                        await guild.create_voice_channel(
                            name=ch_info["name"],
                            category=new_cat,
                            bitrate=ch_info["bitrate"],
                            user_limit=ch_info["user_limit"],
                            overwrites=ch_overwrites
                        )
                    await asyncio.sleep(0.3)
            except Exception as e:
                print(f"카테고리 생성 실패 ({cat_info['name']}): {e}")
                
        for ch_info in data["channels"]:
            try:
                ch_overwrites = build_overwrites(ch_info.get("overwrites", {}))
                if ch_info["type"] == "text":
                    await guild.create_text_channel(
                        name=ch_info["name"],
                        topic=ch_info["topic"],
                        slowmode_delay=ch_info["slowmode"],
                        overwrites=ch_overwrites
                    )
                elif ch_info["type"] == "voice":
                    await guild.create_voice_channel(
                        name=ch_info["name"],
                        bitrate=ch_info["bitrate"],
                        user_limit=ch_info["user_limit"],
                        overwrites=ch_overwrites
                    )
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"채널별 채널 생성 실패 ({ch_info['name']}): {e}")
                
        try:
            os.remove(f"backup_{target_id}.json")
        except:
            pass
            
        await ctx.send("``` ♱ 역할 및 권한을 포함하여 정상적으로 서버를 복구(복제) 하였습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 서버 복구 중 오류 발생: {e} ♱ ```")

deleted_cache = {}
edited_cache = {}

def make_message(msg_text):
    lower1 = random.choice(string.ascii_lowercase)
    numbers = ''.join(random.choice(string.digits) for _ in range(4))
    upper = random.choice(string.ascii_uppercase)
    lower2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
    symbol = random.choice("!@#$%^&*")
    suffix = f"{lower1}{numbers}{upper}{lower2}{symbol}"
    return f"{msg_text} {suffix}"


def 우회_난수_부호():
    lower1 = random.choice(string.ascii_lowercase)
    numbers = ''.join(random.choice(string.digits) for _ in range(4))
    upper = random.choice(string.ascii_uppercase)
    lower2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
    symbol = random.choice("!@#$%^&*")
    return f" {lower1}{numbers}{upper}{lower2}{symbol}"


def fix_count(count):
    if count < 1:
        return 1
    if count > 5:
        return 5
    return count

@bot.event
async def on_ready():
    print(f'-> ONLINE: {bot.user.name} Credit: demian2880')
    
    for guild in bot.guilds:
        saved_channel_id = load_voice_backup(guild.id)
        if saved_channel_id:
            channel = guild.get_channel(saved_channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                try:
                    await guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
                    print(f"[{guild.name}] 백업 복구: {channel.name} 채널에 자동 재입장했습니다.")
                except Exception as e:
                    print(f"[{guild.name}] 자동 재입장 실패: {e}")
    
@bot.command()
async def 근성설정(ctx, seconds: float = None):
    global 근성_seconds
    if seconds is None:
        await ctx.send("``` ♱ 사용법: !근성설정 <초> ♱ ```")
        return
    근성_seconds = seconds
    await ctx.send(f"``` ♱ 근성 속도를 {seconds}초(으)로 설정완료 ♱ ```")

@bot.command()
async def 근성시작(ctx, *, text: str = None):
    global 근성_loop, 근성_text, 근성_channel
    if text is None:
        await ctx.send("``` ♱ 사용법: !근성시작 <문구> ♱ ```")
        return
    근성_channel = ctx.channel
    근성_text = text
    근성_loop = True
    await ctx.send(f"``` ♱ 근성 스패밍 시작. (간격: {근성_seconds}초) ♱ ```")

@bot.command()
async def 근성중지(ctx):
    global 근성_loop, 근성_text, 근성_channel
    근성_loop = False
    근성_text = None
    근성_channel = None
    await ctx.send("``` ♱ 근성 스팸을 중지합니다. ♱ ```")

@bot.command()
async def 도배설정(ctx, seconds: float = None):
    global 도배_seconds
    if seconds is None:
        await ctx.send("``` ♱ 사용법: !도배설정 <초> ♱ ```")
        return
    도배_seconds = seconds
    await ctx.send(f"``` ♱ 도배 속도를 {seconds}초(으)로 설정했습니다. ♱ ```")

@bot.command()
async def 도배시작(ctx, *, text: str = None):
    global 도배_loop, 도배_text, 도배_channel
    if text is None:
        await ctx.send("``` ♱ 사용법: !도배시작 <문구> ♱ ```")
        return
    도배_channel = ctx.channel
    도배_text = text
    도배_loop = True
    await ctx.send(f"``` ♱ 도배 스패밍 시작. (간격: {도배_seconds}초) ♱ ```")

@bot.command()
async def 도배중지(ctx):
    global 도배_loop, 도배_text, 도배_channel
    도배_loop = False
    도배_text = None
    도배_channel = None
    await ctx.send("``` ♱ 도배를 중지합니다. ♱ ```")

@bot.command()
async def 멘션시작(ctx, member: discord.Member = None):
    global mention_loop, mention_target, mention_channel
    if member is None:
        await ctx.send("``` ♱ 사용법: !멘션시작 @유저 ♱ ```")
        return
    mention_target = member
    mention_channel = ctx.channel
    mention_loop = True
    await ctx.send(f"``` ♱ {member.name} 멘션도배시작. ♱ ```")

@bot.command()
async def 멘션중지(ctx):
    global mention_loop, mention_target, mention_channel
    target_name = mention_target.name if mention_target else ""
    mention_loop = False
    mention_target = None
    mention_channel = None
    if target_name:
        await ctx.send(f"``` ♱ {target_name} 멘션도배중지. ♱ ```")
    else:
        await ctx.send("``` ♱ 멘션도배중지. ♱ ```")

@bot.command()
async def 멘션설정(ctx, seconds: float = None):
    global mention_delay
    if seconds is None:
        await ctx.send("``` ♱ 사용법: !멘션설정 <초> ♱ ```")
        return
    mention_delay = seconds
    await ctx.send(f"``` ♱ 멘션 속도를 {seconds}초(으)로 맞췄습니다. ♱ ```")

@bot.command()
async def 입력시작(ctx):
    global typing_loop, typing_channel
    typing_channel = ctx.channel
    typing_loop = True
    await ctx.send("``` ♱ 입력 상태를 시작합니다. ♱ ```")

@bot.command()
async def 입력중지(ctx):
    global typing_loop, typing_channel
    typing_loop = False
    typing_channel = None
    await ctx.send("``` ♱ 입력 상태를 중지합니다. ♱ ```")

@bot.command()
async def 그룹설정(ctx, seconds: float = None):
    global group_seconds
    if seconds is None:
        await ctx.send("``` ♱ 사용법: !그룹설정 <초> ♱ ```")
        return
    group_seconds = seconds
    await ctx.send(f"``` ♱ 그룹 변경 속도를 {seconds}초(으)로 설정했습니다. ♱ ```")

@bot.command()
async def 그룹시작(ctx, *, group_name: str = None):
    global group_loop, group_name_val, group_channel
    if not isinstance(ctx.channel, discord.GroupChannel):
        await ctx.send("``` ♱ 이 명령어는 그룹 DM(채팅방) 안에서만 사용할 수 있습니다. ♱ ```")
        return
    if group_name is None:
        await ctx.send("``` ♱ 사용법: !그룹시작 <그룹이름> ♱ ```")
        return
    if group_loop:
        await ctx.send("``` ♱ 이미 그룹 이름 변경 도배가 진행 중입니다. ♱ ```")
        return
    group_name_val = group_name
    group_channel = ctx.channel
    group_loop = True
    await ctx.send(f"``` ♱ '{group_name}'(으)로 그룹 이름 변경을 시작합니다. (간격: {group_seconds}초) ♱ ```")

@bot.command()
async def 그룹중지(ctx):
    global group_loop, group_name_val, group_channel
    group_loop = False
    group_name_val = None
    group_channel = None
    await ctx.send("``` ♱ 그룹 이름 변경 도배를 중지합니다. ♱ ```")

@bot.command()
async def 장애타설정(ctx, speed: float = None):
    global jail_speed
    if speed is None:
        await ctx.send("``` ♱ 사용법: !장애타설정 <초> ♱ ```")
        return
    jail_speed = speed
    await ctx.send(f"``` ♱ 장애타 속도를 {speed}초로 맞췄습니다 ♱ ```")

@bot.command()
async def 장애타시작(ctx):
    global 장애타_루프, 장애타_channel
    장애타_channel = ctx.channel
    장애타_루프 = True
    await ctx.send("``` ♱ 장애타를 시작합니다 ♱ ```")

@bot.command()
async def 장애타중지(ctx):
    global 장애타_루프, 장애타_channel
    장애타_루프 = False
    장애타_channel = None
    await ctx.send("``` ♱ 장애타가 중지 되었습니다 ♱ ```")

@bot.command()
async def 멘션타설정(ctx, seconds: float = None):
    global mention_jail_speed
    if seconds is None:
        await ctx.send("``` ♱ 사용법: !멘션타설정 <초> ♱ ```")
        return
    mention_jail_speed = seconds
    await ctx.send(f"``` ♱ 멘션타 속도를 {seconds}초(으)로 설정완료 ♱ ```")

@bot.command()
async def 멘션타시작(ctx, user_id: int = None):
    global mention_jail_loop, mention_jail_target, mention_jail_channel
    if user_id is None:
        await ctx.send("``` ♱ 사용법: !멘션타시작 <유저ID> ♱ ```")
        return
    
    mention_jail_channel = ctx.channel
    mention_jail_target = user_id
    mention_jail_loop = True
    await ctx.send(f"``` ♱ {user_id} 멘션타 시작 <간격: {mention_jail_speed}초> ♱ ```")

@bot.command()
async def 멘션타중지(ctx):
    global mention_jail_loop, mention_jail_target, mention_jail_channel
    mention_jail_loop = False
    mention_jail_target = None
    mention_jail_channel = None
    await ctx.send("``` ♱ 멘션타를 중지합니다. ♱ ```")

@bot.command()
async def 통방입장(ctx, channel_id: int = None):
    if channel_id is None:
        await ctx.send("``` ♱ 사용법: !통방입장 <음성채널ID> ♱ ```")
        return

    channel = bot.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.VoiceChannel):
        await ctx.send("``` ♱ 올바른 음성 채널 ID가 아닙니다. ♱ ```")
        return

    try:
        if ctx.guild:
            await ctx.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
            save_voice_backup(ctx.guild.id, channel.id)
            await ctx.send(f"``` ♱ [{channel.name}] 채널에 입장 및 백업 완료되었습니다. ♱ ```")
        else:
            await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 입장 중 오류 발생: {e} ♱ ```")

@bot.command()
async def 통방퇴장(ctx):
    try:
        if ctx.guild:
            await ctx.guild.change_voice_state(channel=None)
            remove_voice_backup(ctx.guild.id)
            await ctx.send("``` ♱ 통방에서 퇴장 및 백업이 해제되었습니다. ♱ ```")
        else:
            await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 퇴장 중 오류 발생: {e} ♱ ```")
        
vote_config = {"is_running": False, "tasks": [], "interval": 1.5}

@bot.command(name="투표설정")
async def 투표설정(ctx, interval: float = None):
    if interval is None:
        await ctx.send("``` ♱ 사용법: !투표설정 <초> (예: !투표설정 1.5) ♱ ```")
        return

    vote_config["interval"] = interval
    await ctx.send(f"``` ♱ 투표 생성 간격이 {interval}초로 설정되었습니다. ♱ ```")

@bot.command(name="투표시작")
async def 투표시작(ctx, title: str = None, *options):
    if not title:
        await ctx.send("``` ♱ 사용법: !투표시작 <투표제목> [보기1] [보기2] ... ♱ ```")
        return

    if vote_config["is_running"]:
        await ctx.send("``` ♱ 이미 투표가 진행 중입니다. !투표중지 로 먼저 멈춰주세요. ♱ ```")
        return

    if not options:
        options = (
            "무무 찬양해라 ㅋㅋ",
            "무무 업 ㅋㅋ",
            "심하게까부네 ㅋㅋ",
            "절대쉬지마라 ㅋㅋ",
            "쉬면 지는거야 ㅋㅋ",
        )

    vote_config["is_running"] = True
    vote_config["tasks"] = []

    task = bot.loop.create_task(vote_generator_loop(ctx, title, options))
    vote_config["tasks"].append(task)

    await ctx.send(f"``` ♱ 투표 생성을 시작합니다. (제목: {title}) ♱ ```")

@bot.command(name="투표중지")
async def 투표중지(ctx):
    if not vote_config["is_running"]:
        await ctx.send("``` ♱ 진행 중인 투표가 없습니다. ♱ ```")
        return

    vote_config["is_running"] = False
    for task in vote_config["tasks"]:
        if not task.done():
            task.cancel()
    vote_config["tasks"].clear()

    await ctx.send("``` ♱ 투표 중지됨 ♱ ```")

async def vote_generator_loop(ctx, title, options):
    try:
        while vote_config["is_running"]:
            rand_num = random.randint(100000, 999999)
            poll_title = f"{title} {rand_num}"

            poll = discord.Poll(question=poll_title, duration=datetime.timedelta(hours=24))
            
            for opt in options:
                poll.add_answer(text=opt)

            await ctx.send(poll=poll)

            await asyncio.sleep(vote_config["interval"]) 
            
    except asyncio.CancelledError:
        pass
    except discord.HTTPException as e:
        print(f"디스코드 API 오류: {e}")
        await asyncio.sleep(2)
    except Exception as e:
        print(f"투표 루프 오류 발생: {e}")

@bot.command()
async def 도움말(ctx):
    msg = (
        "```ini\n"
        "♱ ⚡ 리무무 selfbot | 도움말 카테고리 목록 | Prefix: !\n\n"
        "원하시는 카테고리 명령어를 입력해주세요\n\n"
        "[!]타겟명령어      - 타겟 명령어 안내\n\n"
        "[!]근성명령어      - 근성 명령어 안내\n\n"
        "[!]서버관리명령어   - 서버 관리 명령어 안내\n\n"
        "[!]정보명령어      - 정보 명령어 안내\n\n"
        "[!]자동화명령어    - 자동화 명령어 안내\n\n"
        "[!]따라하기명령어   - 따라하기 명령어 안내\n\n"
        "[!]유틸리티명령어1  - 유틸리티 명령어 1 안내\n\n"
        "[!]유틸리티명령어2  - 유틸리티 명령어 2 안내\n\n"
        "[!]상태명령어      - 상태 명령어 안내\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 타겟명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 🎯 기본 설정 및 제어 명령어 목록\n\n"
        "기본 설정 및 제어 명령어:\n"
        "[!]타겟 @유저         — 대상 유저 고정\n"
        "[!]타겟해제           - 대상 유저 고정 해제\n"
        "[!]중단              — 모든 기능 일괄 강제 중지 및 타겟 해제\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 근성명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 💥 근성 명령어 목록\n\n"
        "근성 명령어:\n"
        "[!]근성설정 <초>        - 무한 근성 폭격 속도 설정\n"
        "[!]근성시작 <문구>      — 무한 근성 폭격\n"
        "[!]근성중지             — 무한 근성 폭격 멈춤\n"
        "[!]도배설정 <초>        - 채팅방 무한 도배 속도 설정\n"
        "[!]도배시작 <문구>      — 현재 채팅방 무한 도배 \n"
        "[!]도배중지             — 채널 무한 도배 멈춤\n"
        "[!]멘션시작 <@유저>     - 멘션도배시작\n"
        "[!]멘션중지 <@유저>     - 멘션도배중지\n"
        "[!]멘션설정 <초>        - 멘션속조절\n"
        "[!]그룹설정 <초>        - 그룹 이름 변경 도배 속도 설정\n"
        "[!]그룹시작 <문구>      — 그룹 이름 변경 도배\n"
        "[!]그룹중지             — 그룹 이름 변경 도배중지\n"
        "[!]투표설정 <초>        - 투표 도배 속도 조절\n"
        "[!]투표시작 <제목>       - 투표 도배 시작\n"
        "[!]투표중지             - 투표 도배 중지\n"
        "[!]입력시작             — 채널에서 내가 계속 타이핑 중인 상태 유지\n"
        "[!]입력중지             — 타이핑 중 상태 고정 해제\n"
        "[!]장애타설정 <초>      — 장애타 속도 조정\n" 
        "[!]장애타시작           — 지정한 매운맛장애타 문구 무한 순환 연타\n"
        "[!]장애타중지           — 장애타 무한 연타 중단\n"
        "[!]멘션타설정 <초>       - 멘션타 속도 조절\n"
        "[!]멘션타시작 <유저id>    - 유저에게 멘션 장애타 시작\n"
        "[!]멘션타중지            - 멘션 장애타 중지\n"
        "[!]통방입장 <음성채널id>  - 음성채널통방입장\n"
        "[!]통방퇴장            - 음성채널퇴장\n"
        "[!]시작설정 <초>        - 시작의 속도 조정\n"
        "[!]시작               — 미리 저장된 악성 멘탈 타격 대사 무한 난사\n"
        "[!]멈춤               — 악성 멘탈 타격 도배 중지\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 서버관리명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 🛡️ 서버 관리 명령어 목록\n\n"
        "[!]역할지급 <@유저> <역할이름>   — 자동 역할 지급\n"
        "[!]역할해제 <@유저> <역할이름>   - 자동 역할 해제\n"
        "[!]역할목록                - 서버에 있는 역할 목록 표시\n"
        "[!]역할생성 <이름> <개수>     - 지정한 이름으로 정한 개수만큼 역할생성\n"
        "[!]채널생성 <이름> <개수>     - 지정한 이름으로 정한 개수만큼 채널생성\n"
        "[!]음성채널생성 <이름> <개수> - 지정한 이름으로 정한 개수만큼 음성채널생성\n"
        "[!]닉 <@유저> <변경할 닉>   — 닉네임 변경\n"
        "[!]킥 <@유저>              — 사용자 강퇴\n"
        "[!]밴 <@유저>              — 사용자 차단\n"
        "[!]슬로우모드 <초>           — 슬로우모드 설정\n"
        "[!]슬로우모드해제            - 슬로우모드 설정해제\n"
        "[!]탐아 <분> <@유저>         - 유저를 타임아웃합니다\n"
        "[!]탐아해제 <@유저>          - 유저의 타임아웃을 해제합니다\n"
        "[!]서버복사                - 서버의 채널,카테고리,역할등을 복사합니다\n"
        "[!]서버복구 <서버id>        - 복사해놓았던 서버를 복구(복사)합니다\n"
        "[!]테러                  — 채널 초기화\n"
        "[!]누크                  - 서버 테러\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 정보명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 💡 정보 명령어 목록\n\n"
        "[!]아이피 <아이피>          - 아이피 정말 추적\n"
        "[!]스파이시작 <id>          - 다른 서버의 대화를 채널로 전송\n"
        "[!]스파이중지                - 스파이를 중지\n"
        "[!]번역 <문장>             - 문장을 한국어 <-> 영어 (으)로 번역합니다\n"
        "[!]내정보                   - 서버 수 , 아이디 , 사용자명를 조회합니다\n"
        "[!]시간                   - 날짜 및 시간을 출력합니다\n"
        "[!]핑                     - 디스코드와의 핑을 측정합니다\n"
        "[!]서버정보                — 현재 입장해 있는 서버의 이름과 유저 수 조회\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 자동화명령어(ctx):
    msg = (
        "```ini\n"
        "♱ ⚙️ 자동화 명령어 목록\n\n"
        "[!]답장등록 <단어> <답장>     - 단어 전송 시 자동으로 답장합니다\n"
        "[!]답장켜기                - 답장 기능을 킵니다\n"
        "[!]답장끄기                - 답장 기능을 끕니다\n"
        "[!]잠수 <멘트>             - DM, 멘션, 답장 시 멘트를 전송합니다\n"
        "[!]잠수해제                - 작동 중인 잠수 모드를 해제합니다\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 따라하기명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 🎭 따라하기 명령어 목록\n\n"
        "[!]카운터시작 <유저id>        — 대상을 부르며 즉시 자동 반박 가동\n"
        "[!]카운터중지                — 자동 반박 종료\n"
        "[!]따라하기시작 <유저id>      — 멘션 대상을 부르며 똑같이 카피 시작\n"
        "[!]따라하기중지              — 앵무새 카피 모드 종료\n"
        "[!]스마트따라하기시작 <유저id>  — 대사 사이에 'ㅋ'를 찢어 넣으며 약 올리기\n"
        "[!]스마트따라하기중지          — 스마트 따라하기 종료\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 유틸리티명령어1(ctx):
    msg = (
        "```ini\n"
        "♱ 🛠️ 유틸리티 명령어 1 목록\n\n"
        "[!]유저리액션시작 <@유저>    — 멘션한 타겟 유저의 메시지마다 이모지 추격\n"
        "[!]유저리액션중지            — 지정 이모지 자동 추격 끄기\n"
        "[!]반응변경 <이모지>        — 유저리액션 기능에서 달아줄 이모지 종류 변경\n"
        "[!]청소 <개수>              — 내 개인 DM방에서 내가 쓴 메시지를 적은 개수만큼 강제 삭제\n"
        "[!]그룹정리 <개수>           - 내 개인 DM방에서 가장 옛날에 가입되있는 방들을 순서로 나감\n"
        "[!]채널검색 <이름>          - 검색한 채널에 정보를 보여줍니다\n"
        "[!]고스트핑 <@유저> <회>     — 빛의 속도로 태그하고 지워 알림 테러\n"
        "[!]빈메시지                — 투명 유니코드 공백 메시지 송출\n"
        "[!]채널비우기              — 투명 줄바꿈 벽을 보내 기존 채팅 기록 밀어버리기\n"
        "[!]숨겨진핑                — 스포일러 뒤에 에브리원 핑 숨겨서 전송\n"
        "[!]숨겨진전체핑            — 스포일러 뒤에 히어 핑 숨겨서 전송\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 유틸리티명령어2(ctx):
    msg = (
        "```ini\n"
        "♱ 🛠️ 유틸리티 명령어 2 목록\n\n"
        "[!]상메 <내용>             - 상태메시지를 변경합니다\n"
        "[!]상메삭제                - 상태메시지를 삭제합니다\n"
        "[!]대명사 <문구>           - 원하는 문구로 대명사 변경\n"
        "[!]대명사삭제              - 대명사를 삭제합니다\n"
        "[!]유저정보 <@유저>        — 상대방의 디스코드 닉네임과 고유 ID 조회\n"
        "[!]프사훔치기 <@유저>      — 상대방 프로필 사진의 원본 고화질 링크 탈취\n"
        "[!]pfp <메세지링크>       - 프로필 사진 변경\n"
        "[!]계좌설정 <내용>         — 돈 독촉용 내 계좌번호나 문구 임시 저장\n"
        "[!]계좌                    — 등록해둔 내 계좌 문구를 채팅창에 출력\n"
        "[!]컷 <유저id>              — 상대방을 초를 세서 컷을 냄\n"
        "[!]컷중지                  - 진행중인 컷을 중지합니다\n"
        "[!]접두사 <기호>           — 실시간으로 셀프봇 명령어를 켜는 접두사 변경\n"
        "[!]삭제스나이프            — 타겟이 지워버린 가장 최근 메시지 박제\n"
        "[!]수정스나이프            — 타겟이 수정한 메시지의 수정 전 원본 폭로\n"
        "```"
    )
    await ctx.send(msg)

@bot.command()
async def 상태명령어(ctx):
    msg = (
        "```ini\n"
        "♱ 🛑 상태 명령어 목록\n\n"
        "[!]rpc설정 <초>           - 활동 시간을 사용자 지정으로 설정합니다 (최대 315360000시간)\n"
        "[!]방송 <이름>             - 방송 중으로 상태창을 변경합니다\n"
        "[!]활동 <이름>             - 하는 중으로 상태창을 변경합니다\n"
        "[!]시청 <이름>             - 시청 중으로 상태창을 변경합니다\n"
        "[!]듣기 <이름>             - 듣는 중으로 상태창을 변경합니다\n"
        "[!]상태초기화               - 상태창이 초기화됩니다\n"
        "```"
    )
    await ctx.send(msg)

    await ctx.send(page1_msg)
    await ctx.send(page2_msg)

@bot.command(name="명령어")
async def 명령어(ctx):
    await 도움말(ctx)

@bot.command()
async def 타겟(ctx, member: discord.Member = None):
    global target_id, mimic_target_id, reaction_target_id, counter_target_id
    if member is None:
        await ctx.send("``` ♱ 타겟으로 지정할 유저를 멘션해주세요. ♱ ```")
        return
    
    target_id = member.id
    mimic_target_id = str(member.id)
    reaction_target_id = str(member.id)
    counter_target_id = str(member.id)
    await ctx.send(f"``` ♱ {member.name} ({target_id}) 전면 조지기 시작. ♱ ```")

@bot.command()
async def 타겟해제(ctx):
    global target_id, mimic_target_id, reaction_target_id, counter_target_id
    global mimic_target_name, reaction_target_name, counter_target_name

    target_id = None
    mimic_target_id = None
    reaction_target_id = None
    counter_target_id = None
    mimic_target_name = None
    reaction_target_name = None
    counter_target_name = None

    await ctx.send("``` ♱ 지정된 타겟이 해제되었습니다. ♱ ```")


@bot.command()
async def 중단(ctx):
    global group_loop, 근성_loop, 도배_loop
    global mimic_strict_active, smart_mimic_active, is_reaction_running
    global mimic_target_id, reaction_target_id, vote_loop
    global mimic_active, smart_mimic, reaction_active, auto_emoji
    global typing_active, mentall_loop, zomb_loop, best_loop, group_create_loop, counter_loop, user_reaction_loop
    global target_id, counter_target_id, mimic_target_name, reaction_target_name, counter_target_name

    group_loop = False
    근성_loop = False
    도배_loop = False
    mimic_strict_active = False
    smart_mimic_active = False
    is_reaction_running = False
    vote_loop = False
    mimic_active = False
    smart_mimic = False
    reaction_active = False
    auto_emoji = False
    typing_active = False
    mentall_loop = False
    zomb_loop = False
    best_loop = False
    group_create_loop = False
    counter_loop = False
    user_reaction_loop = False

    target_id = None
    mimic_target_id = None
    reaction_target_id = None
    counter_target_id = None
    mimic_target_name = None
    reaction_target_name = None
    counter_target_name = None

    await ctx.send("``` ♱ 모든 기능이 일괄 강제로 중지 되었으며 타겟이 해제되었습니다. ♱ ```")


YOUTUBE_API_KEY = "AIzaSyDZtUh-PsZX7vBx31J_hXyr0LEumy4O23o"

@bot.command()
async def 채널검색(ctx, *, query: str):
    await ctx.send(f"``` ♱ 🔍 '{query}' 채널 정보 검색 중... ♱ ```")
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            type='channel',
            maxResults=1
        ).execute()
        
        if not search_response.get('items'):
            await ctx.send("``` ♱ 검색된 채널이 없습니다. ♱ ```")
            return
            
        channel_item = search_response['items'][0]
        channel_id = channel_item['snippet']['channelId']
        channel_name = channel_item['snippet']['title']
        thumbnail = channel_item['snippet']['thumbnails']['high']['url']
        channel_url = f"https://www.youtube.com/channel/{channel_id}"
        
        playlist_response = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()
        
        uploads_playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        playlist_items = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=1
        ).execute()
        
        latest_video = playlist_items['items'][0]['snippet']
        latest_video_title = latest_video['title']
        video_id = latest_video['resourceId']['videoId']
        latest_video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        embed_text = (
            f"📺 **[채널 정보: {channel_name}]({channel_url})**\n"
            f"• **가장 최근 영상:** {latest_video_title}\n"
            f"• **영상 바로가기:** {latest_video_url}\n"
            f"• **채널 썸네일:** {thumbnail}"
        )
        
        await ctx.send(embed_text)
        
    except Exception as e:
        await ctx.send(f"``` ♱ 정보를 가져오지 못했습니다: {e} ♱ ```")

@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user}')

@bot.command(name='서버나가기')
async def leave_guild(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("``` ♱ 이 명령어는 서버 안에서만 사용할 수 있습니다. ♱ ```")
        return
    
    try:
        await ctx.send(f"``` ♱ '{guild.name}' 서버 퇴장. ♱ ```")
        await guild.leave()
    except Exception as e:
        await ctx.send(f"``` ♱ 오류 발생: {e} ♱ ```")

@bot.command(name='그룹나가기')
async def leave_group(ctx):
    channel = ctx.channel
    
    try:
        if isinstance(channel, discord.GroupChannel):
            await ctx.send("``` ♱ 그룹 채팅방 퇴장. ♱ ```")
            await channel.leave()
        elif isinstance(channel, discord.DMChannel):
            await ctx.send("``` ♱ DM 채널은 나갈 수 없습니다. ♱ ```")
        else:
            await ctx.send("``` ♱ 그룹 채팅방에서만 사용할 수 있는 명령어입니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 오류 발생: {e} ♱ ```")

@bot.command(name="아이피")
async def 아이피(ctx, ip_address: str = None):
    if ip_address is None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.ipify.org?format=json") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        ip_address = data.get("ip")
        except:
            pass
            
    if ip_address is None:
        await ctx.send("``` ♱ Usage: !아이피 <IP> (또는 봇의 공인 IP 조회 실패) ♱ ```")
        return
    
    data = None
    
    try:
        fields = "status,message,query,country,regionName,city,zip,isp,as,timezone,hosting,mobile,proxy,lat,lon"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com/json/{ip_address}?fields={fields}") as resp:
                if resp.status == 200:
                    res_data = await resp.json()
                    if res_data.get("status") == "success":
                        data = res_data
    except:
        pass
        
    if not data:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ipapi.co/{ip_address}/json/") as resp:
                    if resp.status == 200:
                        res_data = await resp.json()
                        if "error" not in res_data:
                            data = {
                                "query": res_data.get("ip", ip_address),
                                "country": res_data.get("country_name", "Unknown"),
                                "regionName": res_data.get("region", "Unknown"),
                                "city": res_data.get("city", "Unknown"),
                                "zip": res_data.get("postal", "Unknown"),
                                "isp": res_data.get("org", "Unknown"),
                                "as": res_data.get("asn", "Unknown"),
                                "timezone": res_data.get("timezone", "Unknown"),
                                "hosting": False,
                                "mobile": False,
                                "proxy": False,
                                "lat": res_data.get("latitude", 0.0),
                                "lon": res_data.get("longitude", 0.0)
                            }
        except:
            pass

    if data:
        try:
            ip = data.get("query", ip_address)
            country = data.get("country", "Unknown")
            region = data.get("regionName", "Unknown")
            city = data.get("city", "Unknown")
            postal = data.get("zip", "Unknown")
            isp = data.get("isp", "Unknown")
            asn = data.get("as", "Unknown")
            timezone = data.get("timezone", "Unknown")
            lat = data.get("lat", 0.0)
            lon = data.get("lon", 0.0)
            
            is_hosting = data.get("hosting", False)
            is_mobile = data.get("mobile", False)
            is_proxy = data.get("proxy", False)
            
            if is_proxy:
                connection_type = "프록시 / VPN"
            elif is_hosting:
                connection_type = "데이터센터 / 서버"
            elif is_mobile:
                connection_type = "모바일 네트워크"
            else:
                connection_type = "일반 가정용 / 브로드밴드"
                
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            
            result_msg = f"""```ansi
[1;32m[ ✔ ] IP 추적 성공 ({ip})[0m

IP Address       : {ip}
City             : {city}
State or Region  : {region}
Postal Code      : {postal}
Country          : {country}
ISP / Telecom    : {isp}
ASN Info         : {asn}
UTC Time Zone    : {timezone}
Connection Type  : {connection_type}
Latitude         : {lat}
Longitude        : {lon}
Google Maps      : {maps_url}
```"""
            await ctx.send(result_msg)
        except Exception as e:
            await ctx.send(f"``` ♱ Error occurred: {e} ```")
    else:
        await ctx.send("``` ♱ Invalid or untrackable IP address. ♱ ```")

@bot.command(name="대명사")
async def change_pronouns(ctx, *, pronouns: str):

  url = "https://discord.com/api/v9/users/@me/profile"
  headers = {"Authorization": bot.http.token, "Content-Type": "application/json"}
  payload = {"pronouns": pronouns}

  try:
    async with aiohttp.ClientSession() as session:
      async with session.patch(url, json=payload, headers=headers) as resp:
        if resp.status == 200:
          await ctx.send(f"``` ♱ 대명사가 **'{pronouns}'**(으)로 변경되었습니다! ♱ ```")
        else:
          await ctx.send(f"``` ♱ 변경 실패 (상태 코드: {resp.status}) ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 오류 발생: {e} ♱ ```")

@bot.command(name="대명사삭제")
async def delete_pronouns(ctx):

  url = "https://discord.com/api/v9/users/@me/profile"
  headers = {"Authorization": bot.http.token, "Content-Type": "application/json"}
  payload = {"pronouns": ""}

  try:
    async with aiohttp.ClientSession() as session:
      async with session.patch(url, json=payload, headers=headers) as resp:
        if resp.status == 200:
          await ctx.send("``` ♱ 대명사 설정이 초기화되었습니다. ♱ ```")
        else:
          await ctx.send(f"``` ♱ 삭제 실패 (상태 코드: {resp.status}) ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 오류 발생: {e} ♱ ```")


@bot.command(name="pfp")
async def change_pfp(ctx, message_link: str):

  try:
    parts = message_link.split("/")
    channel_id = int(parts[-2])
    message_id = int(parts[-1])

    channel = bot.get_channel(channel_id)
    if not channel:
      channel = await bot.fetch_channel(channel_id)

    msg = await channel.fetch_message(message_id)

    image_url = None
    if msg.attachments:
      image_url = msg.attachments[0].url
    elif msg.embeds:
      embed = msg.embeds[0]
      if embed.image and embed.image.url:
        image_url = embed.image.url
      elif embed.thumbnail and embed.thumbnail.url:
        image_url = embed.thumbnail.url

    if not image_url:
      await ctx.send("``` ♱ 해당 메시지에서 이미지를 찾을 수 없습니다. ♱ ```")
      return

    async with aiohttp.ClientSession() as session:
      async with session.get(image_url) as resp:
        if resp.status == 200:
          image_bytes = await resp.read()
          await bot.user.edit(avatar=image_bytes)
          await ctx.send("``` ♱ 프로필 사진이 변경되었습니다! ♱ ```")
        else:
          await ctx.send("``` ♱ 이미지 다운로드에 실패했습니다. ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 오류 발생: {e} ♱ ```")

@bot.command()
async def 역할지급(ctx, member: discord.Member = None, role: discord.Role = None):
    if member is None or role is None:
        await ctx.send("``` ♱ 역할을 지급할 유저와 역할을 올바르게 입력해주세요. ♱ ```")
        return
    try:
        await member.add_roles(role)
        await ctx.send(f"``` ♱ {member.mention}님에게 {role.name} 역할을 지급했습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 역할 지급 실패: {e} ♱ ```")

@bot.command()
async def 역할해제(ctx, member: discord.Member = None, role: discord.Role = None):
    if member is None or role is None:
        await ctx.send("``` ♱ 역할을 해제할 유저와 역할을 올바르게 입력해주세요. ♱ ```")
        return
    try:
        await member.remove_roles(role)
        await ctx.send(f"``` ♱ {member.mention}님의 {role.name} 역할을 해제했습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 역할 해제 실패: {e} ♱ ```")

@bot.command()
async def 역할목록(ctx):
    if not ctx.guild:
        await ctx.send("``` ♱ 서버에서만 사용할 수 있는 명령어입니다. ♱ ```")
        return
    roles = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    await ctx.send(f"``` ♱ 서버 역할 목록:\n" + ", ".join(roles) + " ♱ ```")

@bot.command()
async def 닉(ctx, member: discord.Member = None, *, new_nick: str = None):
    if member is None or new_nick is None:
        await ctx.send("``` ♱ 대상 유저와 변경할 닉네임을 입력해주세요. (예: 닉 @유저 새닉네임) ♱ ```")
        return
    try:
        await member.edit(nick=new_nick)
        await ctx.send(f"``` ♱ {member.mention}님의 닉네임이 `{new_nick}`(으)로 변경되었습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 닉네임 변경 실패: {e} ♱ ```")

@bot.command()
async def 킥(ctx, member: discord.Member = None, *, reason: str = "사유 없음"):
    if member is None:
        await ctx.send("``` ♱ 강퇴할 유저를 멘션해주세요. ♱ ```")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"``` ♱ {member.mention}님을 강퇴했습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 강퇴 실패: {e} ♱ ```")

@bot.command()
async def 밴(ctx, member: discord.Member = None, *, reason: str = "사유 없음"):
    if member is None:
        await ctx.send("``` ♱ 차단할 유저를 멘션해주세요. ♱ ```")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"``` ♱ {member.mention}님을 차단했습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 차단 실패: {e} ♱ ```")

@bot.command()
async def 슬로우모드(ctx, seconds: int = 0):
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("``` ♱ 슬로우모드가 해제되었습니다. ♱ ```")
        else:
            await ctx.send(f"``` ♱ 채널 슬로우모드가 {seconds}초로 설정되었습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 슬로우모드 설정 실패: {e} ♱ ```")

@bot.command()
async def 슬로우모드해제(ctx):
    try:
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send("``` ♱ 채널 슬로우모드가 해제되었습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 슬로우모드 해제 실패: {e} ♱ ```")

@bot.command()
async def 테러(ctx):
    if not ctx.channel:
        return
    try:
        position = ctx.channel.position
        new_channel = await ctx.channel.clone(reason="채널 초기화(누크)")
        await ctx.channel.delete()
        await new_channel.edit(position=position)
        await new_channel.send("``` ♱ 채널이 성공적으로 초기화되었습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 누크 실패: {e} ♱ ```")

@bot.command(name='탐아')
async def timeout_user(ctx, minutes: int, member: discord.Member):
    """
    사용법: !탐아 <분> <@유저>
    입력한 분(minute)만큼 유저를 타임아웃 처리합니다.
    """
    try:
        duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        
        await member.edit(timed_out_until=duration)
        
        response = f'{member.name} 유저를 {minutes}분 동안 타임아웃 처리했습니다.'
        await ctx.send(f'```\n ♱ {response} ♱ \n```')
        
    except discord.Forbidden:
        await ctx.send('```\n ♱ 권한이 부족하여 타임아웃을 실행할 수 없습니다. ♱ \n```')
    except Exception as e:
        await ctx.send(f'```\n ♱ 오류가 발생했습니다: {e} ♱ \n```')

@bot.command(name="누크")
async def 누크(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
        return

    await ctx.send("``` ♱ 서버 누크(전체 삭제)를 시작합니다... ♱ ```")

    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"채널 삭제 오류 ({channel.name}): {e}")

    for role in guild.roles:
        if role != guild.default_role and role != guild.me.top_role:
            try:
                await role.delete()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"역할 삭제 오류 ({role.name}): {e}")

@bot.command(name="역할생성")
async def 역할생성(ctx, name: str = None, count: int = 1):
    if not ctx.guild:
        await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
        return
    
    if not name:
        await ctx.send("``` ♱ 사용법: !역할생성 <이름> <개수> ♱ ```")
        return
    
    guild = ctx.guild
    
    if count < 1:
        count = 1
    elif count > 50:
        count = 50
        
    try:
        for _ in range(count):
            await guild.create_role(name=name)
            await asyncio.sleep(0.3)
            
        await ctx.send(f"``` ♱ 역할생성 {count}개 생성완료. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 역할 생성 중 오류 발생: {e} ♱ ```")

@bot.command(name="채널생성")
async def 채널생성(ctx, name: str = None, count: int = 1):
    if not ctx.guild:
        await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
        return
    
    if not name:
        await ctx.send("``` ♱ 사용법: !채널생성 <이름> <개수> ♱ ```")
        return
    
    guild = ctx.guild
    
    if count < 1:
        count = 1
    elif count > 50:
        count = 50
        
    try:
        for _ in range(count):
            await guild.create_text_channel(name=name)
            await asyncio.sleep(0.3)
            
        await ctx.send(f"``` ♱ 채널생성 {count}개 생성완료. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 채널 생성 중 오류 발생: {e} ♱ ```")

@bot.command(name="음성채널생성")
async def 음성채널생성(ctx, name: str = None, count: int = 1):
    if not ctx.guild:
        await ctx.send("``` ♱ 서버 내에서만 사용할 수 있는 명령어입니다. ♱ ```")
        return
    
    if not name:
        await ctx.send("``` ♱ 사용법: !음성채널생성 <이름> <개수> ♱ ```")
        return
    
    guild = ctx.guild
    
    if count < 1:
        count = 1
    elif count > 50:
        count = 50
        
    try:
        for _ in range(count):
            await guild.create_voice_channel(name=name)
            await asyncio.sleep(0.3)
            
        await ctx.send(f"``` ♱ 음성채널생성 {count}개 생성완료. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 음성채널 생성 중 오류 발생: {e} ♱ ```")

@bot.command()
async def 탐아해제(ctx, member: discord.Member = None):
    if member:
        try:
            await member.timeout(None)
            await ctx.send(f"``` ♱ {member.name} 탐아해제 완료. ♱ ```")
        except Exception:
            pass
    else:
        await ctx.send("``` ♱ 사용법: !탐아해제 <@유저> ♱ ```")

bad_loop = False
bad_loop_delay = 0.25

@bot.command()
async def 시작설정(ctx, seconds: float = None):
    global bad_loop_delay
    if seconds is not None:
        bad_loop_delay = seconds
        await ctx.send(f"``` ♱ 시작 속도를 {seconds}초(으)로 맞췄습니다. ♱ ```")
    else:
        await ctx.send("``` ♱ 사용법: !시작설정 <초> ♱ ```")

@bot.command()
async def 시작(ctx):
    global bad_loop, bad_loop_delay
    bad_loop = True
    lines = ["응 너 개바르죠?ㅋ", "말 한마디도 정교하게 못 하죠?", "근성 존나 딸리네 진짜ㅋ", "키보드에서 손 떼라 그냥ㅋ"]
    while bad_loop:
        try:
            await ctx.send(f"{random.choice(lines)}{우회_난수_부호()}")
            await asyncio.sleep(bad_loop_delay)
        except:
            pass

@bot.command()
async def 멈춤(ctx):
    global bad_loop
    bad_loop = False

edited_messages = {}
counter_list = []
god_loop = False

mimic_target_id = None
mimic_target_name = None
mimic_strict_active = False
smart_mimic_active = False
is_reaction_running = False
reaction_target_id = None
reaction_target_name = None
reaction_emoji = "👍"

counter_loop = False
counter_target_id = None
counter_target_name = None
counter_phrases = [
    "ㅋㅋ 또 아가리여네 좆같이 약한 버러지가",
    "또 오면 엄마 보지에 미사일 꽂는다 했지ㅋㅋ",
    "이 씨발련 자꾸 말 안듣네 애미 병신련이",
    "ㅋㅋ 말못하는 찌끄레기새끼야 좀 꺼지라니까",
    "너같은 버러지는 상대 안한다니까ㅋㅋ",
    "저 구석가서 혼자 놀아 찐따새끼야ㅋㅋ",
    "별 볼거없는 거지농종자새끼야 절로 꺼지라니까ㅋㅋ"
]

auto_reply_enabled = False
auto_responses = {}
is_afk = False
afk_reason = "현재 잠수 중입니다."

cut_tasks = {}

spy_active = False
spy_target_channel_id = None
spy_destination_channel = None

@bot.event
async def on_message(message):
  global target_id, mimic_active, smart_mimic, reaction_active, auto_emoji, emoji_type
  global is_reaction_running, reaction_target_id, reaction_emoji, mimic_target_id, mimic_strict_active, smart_mimic_active
  global counter_loop, counter_target_id
  global auto_reply_enabled, auto_responses, is_afk, afk_reason
  global cut_tasks
  global spy_active, spy_target_channel_id, spy_destination_channel참

  if not message.author.bot:
    if message.author.id in cut_tasks:
      cut_tasks[message.author.id].cancel()

      async def restart_countdown():
        await asyncio.sleep(2)
        try:
          current_count = 10
          while current_count > 0:
            await message.channel.send(f"<@{message.author.id}> {current_count}")
            await asyncio.sleep(1)
            current_count -= 1

          await message.channel.send(f"<@{message.author.id}> 컷 ㅋㅋ")
          if message.author.id in cut_tasks:
            del cut_tasks[message.author.id]
        except asyncio.CancelledError:
          pass

      cut_tasks[message.author.id] = asyncio.create_task(restart_countdown())

  try:
    if (
        is_reaction_running
        and reaction_target_id
        and str(message.author.id) == str(reaction_target_id)
    ):
      await message.add_reaction(reaction_emoji)
  except Exception as e:
    print(f"리액션 오류: {e}")

  if spy_active and spy_target_channel_id and spy_destination_channel:
    if (
        message.channel.id == int(spy_target_channel_id)
        and message.author != bot.user
    ):
      try:
        await spy_destination_channel.send(
            f"[{message.guild.name if message.guild else 'DM'} /"
            f" {message.channel.name}] **{message.author.name}**:"
            f" {message.content}"
        )
      except Exception as e:
        print(f"스파이 전송 오류: {e}")

  if message.author == bot.user:
    await bot.process_commands(message)
    return

  if auto_reply_enabled:
    for trigger, response in auto_responses.items():
      if trigger in message.content:
        await message.channel.send(response)
        break

  if is_afk:
    is_triggered = False

    if isinstance(message.channel, discord.DMChannel):
      is_triggered = True
    elif not message.mention_everyone and bot.user in message.mentions:
      is_triggered = True
    elif message.reference and message.reference.cached_message:
      if message.reference.cached_message.author.id == bot.user.id:
        is_triggered = True

    if is_triggered:
      await message.reply(afk_reason)

  if (
      counter_loop
      and counter_target_id
      and str(message.author.id) == str(counter_target_id)
  ):
    try:
      selected_phrase = random.choice(counter_phrases)
      await message.channel.send(selected_phrase)
    except Exception as e:
      print(f"카운터 오류: {e}")

  if (
      mimic_active
      and target_id
      and str(message.author.id) == str(target_id)
  ):
    try:
      await message.channel.send(message.content)
    except:
      pass

  if mimic_strict_active and mimic_target_id and str(message.author.id) == str(mimic_target_id):
    await message.channel.send(message.content)

  if smart_mimic and target_id and str(message.author.id) == str(target_id):
    try:
      smart_text = " ㅋ ".join(message.content.split())
      await message.channel.send(smart_text)
    except:
      pass

  if smart_mimic_active and mimic_target_id and str(message.author.id) == str(mimic_target_id):
    await message.channel.send(message.content + "ㅋ")

  await bot.process_commands(message)


@bot.command()
async def 컷(ctx, user_id: str = None):
  global cut_tasks
  if user_id is None:
    await ctx.send("``` ♱ 사용법: !컷 <유저ID> ♱ ```")
    return

  try:
    uid = int(user_id)
    user = bot.get_user(uid) or await bot.fetch_user(uid)
    name = user.name
  except Exception:
    uid = int(user_id)
    name = user_id

  if uid in cut_tasks:
    cut_tasks[uid].cancel()

  async def run_countdown():
    try:
      current_count = 10
      while current_count > 0:
        await ctx.send(f"<@{uid}> {current_count}")
        await asyncio.sleep(1)
        current_count -= 1

      await ctx.send(f"<@{uid}> 컷 ㅋㅋ")
      if uid in cut_tasks:
        del cut_tasks[uid]
    except asyncio.CancelledError:
      pass

  cut_tasks[uid] = asyncio.create_task(run_countdown())
  await ctx.send(f"``` ♱ {name} 컷 시작 ♱ ```")


@bot.command()
async def 컷중지(ctx):
  global cut_tasks
  if not cut_tasks:
    await ctx.send("``` ♱ 현재 작동 중인 컷이 없습니다. ♱ ```")
    return

  for task in cut_tasks.values():
    task.cancel()
  cut_tasks.clear()
  await ctx.send("``` ♱ 모든 컷이 중지되었습니다. ♱ ```")


@bot.command()
async def 답장등록(ctx, trigger: str = None, *, response: str = None):
  global auto_responses
  if trigger and response:
    auto_responses[trigger] = response
    await ctx.send(f"``` ♱ 답장등록이 {response}(으)로 되었습니다. ♱ ```")
  else:
    await ctx.send("``` ♱ 사용법: !답장등록 <단어> <답장> ♱ ```")


@bot.command()
async def 답장켜기(ctx):
  global auto_reply_enabled
  auto_reply_enabled = True
  await ctx.send("``` ♱ 답장이 켜졌습니다. ♱ ```")


@bot.command()
async def 답장끄기(ctx):
  global auto_reply_enabled
  auto_reply_enabled = False
  await ctx.send("``` ♱ 답장이 꺼졌습니다. ♱ ```")


@bot.command()
async def 잠수(ctx, *, reason: str = "현재 잠수 중입니다."):
  global is_afk, afk_reason
  is_afk = True
  afk_reason = reason
  await ctx.send(f"``` ♱ 잠수 모드가 되었습니다. (사유: {reason}) ♱ ```")


@bot.command()
async def 잠수해제(ctx):
  global is_afk
  if not is_afk:
    await ctx.send("``` ♱ 현재 잠수 상태가 아닙니다. ♱ ```")
    return
  is_afk = False
  await ctx.send("``` ♱ 잠수가 해제되었습니다. ♱ ```")


@bot.command()
async def 따라하기시작(ctx, user_id: str = None):
  global mimic_target_id, mimic_strict_active, smart_mimic_active, mimic_target_name
  if user_id is None:
    await ctx.send("``` ♱ 사용법: !따라하기시작 <유저ID> ♱ ```")
    return

  try:
    uid = int(user_id)
    user = bot.get_user(uid) or await bot.fetch_user(uid)
    name = user.name
  except:
    name = user_id

  mimic_target_id = str(user_id)
  mimic_target_name = name
  mimic_strict_active = True
  smart_mimic_active = False
  await ctx.send(f"``` ♱ {name} 따라하기시작. ♱ ```")


@bot.command()
async def 따라하기중지(ctx):
  global mimic_strict_active, mimic_target_id, mimic_target_name
  mimic_strict_active = False
  mimic_target_id = None
  mimic_target_name = None
  await ctx.send("``` ♱ 따라하기중지. ♱ ```")


@bot.command()
async def 스마트따라하기시작(ctx, user_id: str = None):
  global mimic_target_id, smart_mimic_active, mimic_strict_active, mimic_target_name
  if user_id is None:
    await ctx.send("``` ♱ 사용법: !스마트따라하기시작 <유저ID> ♱ ```")
    return

  try:
    uid = int(user_id)
    user = bot.get_user(uid) or await bot.fetch_user(uid)
    name = user.name
  except:
    name = user_id

  mimic_target_id = str(user_id)
  mimic_target_name = name
  smart_mimic_active = True
  mimic_strict_active = False
  await ctx.send(f"``` ♱ {name} 스마트따라하기시작. ♱ ```")


@bot.command()
async def 스마트따라하기중지(ctx):
  global smart_mimic_active, mimic_target_id, mimic_target_name
  smart_mimic_active = False
  mimic_target_id = None
  mimic_target_name = None
  await ctx.send("``` ♱ 스마트따라하기중지. ♱ ```")


@bot.command()
async def 유저리액션시작(ctx, user_id: str = None):
  global is_reaction_running, reaction_target_id, reaction_target_name
  if user_id is None:
    await ctx.send("``` ♱ 사용법: !유저리액션시작 <유저ID> ♱ ```")
    return

  try:
    uid = int(user_id)
    user = bot.get_user(uid) or await bot.fetch_user(uid)
    name = user.name
  except:
    name = user_id

  reaction_target_id = str(user_id)
  reaction_target_name = name
  is_reaction_running = True
  await ctx.send(f"``` ♱ {name} 유저리액션시작. ♱ ```")


@bot.command()
async def 유저리액션중지(ctx):
  global is_reaction_running, reaction_target_id, reaction_target_name
  is_reaction_running = False
  reaction_target_id = None
  reaction_target_name = None
  await ctx.send("``` ♱ 유저리액션중지. ♱ ```")


@bot.command()
async def 반응변경(ctx, emoji=None):
  global reaction_emoji
  if emoji:
    reaction_emoji = emoji
    await ctx.send(f"``` ♱ 반응변경 {emoji}(으)로 설정완료. ♱ ```")
  else:
    await ctx.send("``` ♱ 사용법: !반응변경 <이모지> ♱ ```")


@bot.command()
async def 카운터시작(ctx, user_id: str = None):
  global counter_loop, counter_target_id, counter_target_name
  if user_id is None:
    await ctx.send("``` ♱ 사용법: !카운터시작 <유저ID> ♱ ```")
    return

  try:
    uid = int(user_id)
    user = bot.get_user(uid) or await bot.fetch_user(uid)
    name = user.name
  except:
    name = user_id

  counter_target_id = str(user_id)
  counter_target_name = name
  counter_loop = True
  await ctx.send(f"``` ♱ {name} 카운터시작. ♱ ```")


@bot.command()
async def 카운터중지(ctx):
  global counter_loop, counter_target_id, counter_target_name
  counter_target_id = None
  counter_target_name = None
  counter_loop = False
  await ctx.send("``` ♱ 카운터중지. ♱ ```")


@bot.command(name="스파이시작")
async def 스파이시작(ctx, channel_id: int = None):
  global spy_active, spy_target_channel_id, spy_destination_channel
  if channel_id is None:
    await ctx.send("``` ♱ 사용법: !스파이시작 <채널ID> ♱ ```")
    return

  spy_target_channel_id = channel_id
  spy_destination_channel = ctx.channel
  spy_active = True
  await ctx.send(
      f"``` ♱ 채널 ID {channel_id}번 스파이를 시작합니다. 이 채널로 대화가"
      " 전송됩니다. ♱ ```"
  )


@bot.command(name="스파이중지")
async def 스파이중지(ctx):
  global spy_active, spy_target_channel_id, spy_destination_channel
  spy_active = False
  spy_target_channel_id = None
  spy_destination_channel = None
  await ctx.send("``` ♱ 스파이가 중지되었습니다. ♱ ```")


@bot.command()
async def 청소(ctx, limit: int):
    deleted_count = 0
    
    async for message in ctx.channel.history(limit=100):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
                if deleted_count >= limit:
                    break
            except Exception as e:
                print(e)
                
    await ctx.send(f"``` ♱ {limit}개의 메시지를 삭제했습니다. ♱ ```")

@bot.command(name="그룹정리")
async def 그룹정리(ctx, count: int = None):
    if count is None:
        return
    
    left_count = 0
    for channel in list(bot.private_channels):
        if isinstance(channel, discord.GroupChannel) and left_count < count:
            try:
                await channel.leave()
                left_count += 1
            except Exception as e:
                print(f"그룹 나가기 오류: {e}")
                
    await ctx.send(f"``` ♱ {left_count}개 그룹정리 완료. ♱ ```")

@bot.command()
async def 고스트핑(ctx, user: discord.User, number: int):
    
    for _ in range(number):
        msg = await ctx.send(user.mention)
        await msg.delete()
        await asyncio.sleep(0.15)

@bot.command()
async def 빈메시지(ctx):
    await ctx.send("‌")

@bot.command()
async def 채널비우기(ctx):
    
    for _ in range(12): await ctx.send("‌\n" * 25)

@bot.command()
async def 숨겨진핑(ctx):
    await ctx.send("||||" * 25 + "@everyone")

@bot.command()
async def 숨겨진전체핑(ctx):
    await ctx.send("||||" * 25 + "@here")

@bot.command(name="번역")
async def 번역(ctx, *, text: str = None):
    if text is None:
        await ctx.send("♱ 사용법: !번역 <문장> ♱")
        return
    
    try:
        has_korean = any(ord('가') <= ord(c) <= ord('힣') for c in text)
        
        if has_korean:
            translated_text = GoogleTranslator(source='ko', target='en').translate(text)
        else:
            translated_text = GoogleTranslator(source='en', target='ko').translate(text)
            
        msg = f"```ansi\n\u001b[34m[번역 결과]\u001b[0m\n{translated_text}\n```"
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"♱ 번역 중 오류가 발생했습니다: {e} ♱")

@bot.command()
async def 내정보(ctx):
    user = ctx.author
    guild = ctx.guild
    guild_name = guild.name if guild else "DM 채널"
    
    created_at = user.created_at.strftime("%Y-%m-%d")
    
    await ctx.send(f"```ansi\n\u001b[36m[ 사용자 정보 ]\u001b[0m\n- 서버: {guild_name}\n- 사용자명: {user.name}\n- 아이디: {user.id}\n- 계정생성일: {created_at}\n```")

@bot.command()
async def 시간(ctx):
    kst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(kst)
    time_string = now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    await ctx.send(f"``` ♱ {time_string} ♱ ```")

@bot.command()
async def 상메(ctx, *, content: str = None):
    if content:
        try:
            await bot.change_presence(activity=discord.CustomActivity(name=content))
            await ctx.send(f"``` ♱ 상태메시지가 '{content}'(으)로 변경되었습니다. ♱ ```")
        except Exception as e:
            await ctx.send(f"``` ♱ 상태메시지 변경 실패: {e} ♱ ```")
    else:
        await ctx.send("``` ♱ 사용법: !상메 <내용> ♱ ```")

@bot.command()
async def 상메삭제(ctx):
    try:
        await bot.change_presence(activity=None)
        await ctx.send("``` ♱ 상태메시지가 삭제되었습니다. ♱ ```")
    except Exception as e:
        await ctx.send(f"``` ♱ 상태메시지 삭제 실패: {e} ♱ ```")

@bot.command()
async def 핑(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"``` ♱ 퐁! 핑은 {latency}ms 입니다. ♱ ```")

@bot.command()
async def 서버정보(ctx):
    guild = ctx.guild
    
    owner_name = guild.owner.name if guild.owner else "알 수 없음"
    
    role_count = len(guild.roles)
    
    icon_url = guild.icon.url if guild.icon else "없음"
    
    embed_text = (
        f"```md\n"
        f"# 서버 정보\n"
        f"서버명: {guild.name} | "
        f"서버장: {owner_name} | "
        f"역할개수: {role_count}개 | "
        f"인원수: {guild.member_count}명 | "
        f"아이콘: {icon_url}\n"
        f"```"
    )
    await ctx.send(embed_text)

@bot.command()
async def 유저정보(ctx, user: discord.Member = None):
    
    if user is None:
        await ctx.send("``` ♱ 사용법: !유저정보 <@유저멘션> ♱ ```")
        return

    created_at = user.created_at.strftime("%Y-%m-%d")
    
    embed_text = (
        f"```md\n"
        f"# 유저 정보\n"
        f"닉네임: {user.display_name} | "
        f"사용자명: {user.name} | "
        f"ID: {user.id} | "
        f"계정생성일: {created_at}\n"
        f"```"
    )
    await ctx.send(embed_text)

@bot.command()
async def 프사훔치기(ctx, user: discord.User):
    await ctx.send(user.avatar.url if user.avatar else "``` ♱ 기본 프로필입니다. ♱ ```")

@bot.command()
async def 계좌설정(ctx, *, text: str): 
    global bank_info; bank_info = text;
    await ctx.send("``` ♱ 계좌가 등록되었습니다. ♱ ```")

@bot.command()
async def 계좌(ctx):
    await ctx.send(f"``` ♱ 등록정보: {bank_info} ♱ ```")

@bot.command()
async def 접두사(ctx, new_prefix: str):
    global bot
    bot.command_prefix = new_prefix
    await ctx.send(f"``` ♱ 접두사가 {new_prefix}(으)로 바꼈습니다 ♱ ```")
    
deleted_messages = {}
edited_messages = {}

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    deleted_messages[message.author.id] = message.content

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content != after.content:
        edited_messages[before.author.id] = (before.content, after.content)

@bot.command()
async def 삭제스나이프(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("``` ♱ 확인할 유저를 멘션해주세요. (예: !삭제스나이프 @유저) ♱ ```")
        return
    
    content = deleted_messages.get(member.id)
    if content:
        await ctx.send(f"``` ♱ {member.name}: {content} ♱ ```")
    else:
        await ctx.send(f"``` ♱ {member.mention}님의 삭제된 메시지를 찾을 수 없습니다. ♱ ```")

@bot.command()
async def 수정스나이프(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("``` ♱ 확인할 유저를 멘션해주세요. (예: !수정스나이프 @유저) ♱ ```")
        return
    
    edit_data = edited_messages.get(member.id)
    if edit_data:
        before, after = edit_data
        await ctx.send(f"``` ♱ {member.name}: {before} ♱ ```")
    else:
        await ctx.send(f"``` ♱ {member.mention}님의 수정된 메시지를 찾을 수 없습니다. ♱ ```")

current_status = {"type": None, "name": None, "url": None}

@bot.command(name="rpc설정")
async def rpc설정(ctx, seconds: int = None):
  global current_status
  if seconds is None:
    await ctx.send("``` ♱ 변경할 초를 입력해주세요 (예: !rpc설정 120) ♱ ```")
    return

  if seconds < 0:
    await ctx.send("``` ♱ 시간은 0 이상으로 설정해주세요. ♱ ```")
    return

  max_seconds = 31536000
  if seconds > max_seconds:
    await ctx.send(
        "``` ♱ 31536000초를 넘어가므로 31536000초 안으로 설정해주세요. ♱ ```"
    )
    return

  if not current_status["name"]:
    await ctx.send(
        "``` ♱ 먼저 상태 명령어(!활동, !방송 등)를 사용해 주세요. ♱ ```"
    )
    return

  try:
    current_time_ms = int(time.time() * 1000)
    start_time = current_time_ms - (seconds * 1000) if seconds > 0 else None

    if current_status["type"] == "streaming":
      activity = discord.Streaming(
          name=current_status["name"],
          url=current_status["url"],
          timestamps={"start": start_time},
      )
    else:
      activity = discord.Activity(
          type=current_status["type"],
          name=current_status["name"],
          timestamps={"start": start_time},
      )

    await bot.change_presence(activity=activity)
    await ctx.send(f"``` ♱ 경과 시간이 {seconds}초 전으로 설정되었습니다. ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 변경 실패: {e} ♱ ```")

@bot.command(name="방송")
async def 방송(ctx, *, name: str = None):
  global current_status
  if not name:
    await ctx.send("``` ♱ 상태창에 표시할 내용을 입력해주세요. ♱ ```")
    return
  try:
    current_status["type"] = "streaming"
    current_status["name"] = name
    current_status["url"] = "https://www.twitch.tv/twitch"

    activity = discord.Streaming(name=name, url=current_status["url"])
    await bot.change_presence(activity=activity)
    await ctx.send(f"``` ♱ 방송 중 상태로 변경되었습니다: {name} ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 변경 실패: {e} ♱ ```")

@bot.command(name="활동")
async def 활동(ctx, *, name: str = None):
  global current_status
  if not name:
    await ctx.send("``` ♱ 상태창에 표시할 내용을 입력해주세요. ♱ ```")
    return
  try:
    current_status["type"] = discord.ActivityType.playing
    current_status["name"] = name
    current_status["url"] = None

    activity = discord.Activity(type=current_status["type"], name=name)
    await bot.change_presence(activity=activity)
    await ctx.send(f"``` ♱ 하는 중 상태로 변경되었습니다: {name} ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 변경 실패: {e} ♱ ```")

@bot.command(name="시청")
async def 시청(ctx, *, name: str = None):
  global current_status
  if not name:
    await ctx.send("``` ♱ 상태창에 표시할 내용을 입력해주세요. ♱ ```")
    return
  try:
    current_status["type"] = discord.ActivityType.watching
    current_status["name"] = name
    current_status["url"] = None

    activity = discord.Activity(type=current_status["type"], name=name)
    await bot.change_presence(activity=activity)
    await ctx.send(f"``` ♱ 시청 중 상태로 변경되었습니다: {name} ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 변경 실패: {e} ♱ ```")

@bot.command(name="듣기")
async def 듣기(ctx, *, name: str = None):
  global current_status
  if not name:
    await ctx.send("``` ♱ 상태창에 표시할 내용을 입력해주세요. ♱ ```")
    return
  try:
    current_status["type"] = discord.ActivityType.listening
    current_status["name"] = name
    current_status["url"] = None

    activity = discord.Activity(type=current_status["type"], name=name)
    await bot.change_presence(activity=activity)
    await ctx.send(f"``` ♱ 듣는 중 상태로 변경되었습니다: {name} ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 변경 실패: {e} ♱ ```")

@bot.command(name="상태초기화")
async def 상태초기화(ctx):
  global current_status
  try:
    current_status = {"type": None, "name": None, "url": None}
    await bot.change_presence(activity=None)
    await ctx.send("``` ♱ 상태가 초기화되었습니다. ♱ ```")
  except Exception as e:
    await ctx.send(f"``` ♱ 상태 초기화 실패: {e} ♱ ```")

bot.run('MTUxNzU4MDE2Mzk1NTgyMjYxNg.GAS6OL.N78KdwSrBbjkawY8-mABdNRjx8lO2A6FBNBdGs')