import time
import asyncio
import yt_dlp
import discord
from bot_exceptions import NotInSameVoiceChannelError
voice_clients = {}
is_on_loop=False


song_list = []

# YTDL setup
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_opts)
has_played:bool=False
# ffmpeg setup
ffmpeg_options = {"options": "-vn"}
voice_client: discord.VoiceClient

async def play_music(msg: discord.Message):
    global voice_client
    global song_list
    global has_played
    global is_first_song

    if not has_played:
        voice_client = await msg.author.voice.channel.connect()  # Creating VoiceClient object

    if (msg.content.startswith("$play")):
        try:
            if voice_client.is_playing():
                if not msg.content[6:] in song_list:
                    song_list.append(msg.content[6:])
                    await msg.channel.send("The song has been added to the queue")

                time.sleep(5)
                return
            else:
                if len(song_list)==0:
                    url = msg.content[6:]
                else:
                    url=song_list[0]
                voice_clients[voice_client.guild.id] = voice_client  # NOQA
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")
                voice_client.play(player,after=lambda e:prepare_player(player))
                has_played=True
                await play_music(msg)

        except discord.ClientException as err:
            print(err)
        except Exception as err:
            print(err)

    if (msg.content.startswith("$pause")):
        try:
            await msg.channel.send("The song has been paused")
            voice_client.pause()

        except Exception as err:
            print(err)
    if (msg.content.startswith("$resume")):
        try:
            if voice_client is not None:
                if voice_client.channel == msg.author.voice.channel:
                    if not voice_client.is_playing():
                        voice_client.resume()
                        await msg.channel.send("The song has been resumed.")
                    else:
                        raise RuntimeError("The song has already been resumed.")
                else:
                    raise NotInSameVoiceChannelError()
            else:
                    raise ValueError(f"{msg.author} is not in a voice channel")




        except NotInSameVoiceChannelError as nisvce:
            await msg.channel.send("User has to be in the same channel as the music player")
            print(nisvce)
        except NameError as voice_client_not_defined:
            await msg.channel.send("Not currently playing a song.")
            print(voice_client_not_defined)


        except ValueError as user_not_in_voice_channel:
            await msg.channel.send("You are not in a voice channel")
            print(user_not_in_voice_channel)

        except RuntimeError as already_playing:
            await msg.channel.send("The song has been already resumed.")
            print(already_playing)

        except Exception as unknown_err:
            await msg.channel.send(str(unknown_err))
            print(unknown_err)


async def disconnect(msg: discord.Message):
    try:
        await voice_client.disconnect()
        await msg.channel.send("I have disconnected from your channel.")
    except Exception as e:
        print(e)



def prepare_player(player:discord.FFmpegPCMAudio):
    global song_list
    global voice_client
    if len(song_list)!=0:
        song_list.pop(0)
    player.cleanup()
    time.sleep(10)
    if voice_client.is_playing():
        prepare_player(player)

async def toggle_loop(msg:discord.Message):
    global is_on_loop
    is_on_loop=True
    try:
        if voice_client is None:
            raise NotInSameVoiceChannelError
    except NotInSameVoiceChannelError as nisvce:
        await msg.channel.send("You have to be in a voice channel to loop the song")
        print(nisvce)
    except NameError as ne:
        await msg.channel.send("The music bot has to be playing in order to loop.")
        print(ne)

    else:
        await msg.channel.send("Looping current song.")
    return
