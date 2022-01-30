import discord
from discord.ext import commands 
import requests
import shutil
import asyncio
from pathlib import Path
from PIL import Image
import os
outputpath = ''

def imgtoascii():
    image_path = outputpath +  'img_user.jpg'
    img = Image.open(image_path)

    # resize the image
    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img = img.convert('L')

    pixels = img.getdata()


    chars1 = [",","$","@","%","8","&","/","|","(",")","1","[","]","?","-","_","+","~","<",">","i","!",";",":",",","^","`","'","."," ","0"]
    chars2 = [".","-","=","+","*","%","@","$"," ",".","-"]
    new_pixels = [chars2[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)


    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    with open(outputpath +"ascii_image.txt", "w") as f:
        f.write(ascii_image)    

class toolsimgtotxt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = 'timgtotxt')
    async def imgtotxt(self, ctx):
        if len(os.listdir(outputpath)) != 0:
            for files in os.listdir(outputpath):
                os.remove(outputpath + files)
        #pegar imagem da mensagem
        try:
            url = ctx.message.attachments[0].url
        except:
            print("Erro")
            await ctx.send("Nenhum arquivo anexado")
        else:
            if url[0:26] == "https://cdn.discordapp.com":
                r = requests.get(url, stream = True)
                imageName = outputpath + 'img_user.jpg'
                with open(imageName, 'wb') as output:
                    shutil.copyfileobj(r.raw, output)
                #transformar em ascii
                imgtoascii()
        async def react_and_wait(reply):
            await reply.add_reaction("\U0001F44D")  #emoji dedão pra cima(top) 
            def check(reaction, user):
                return str(reaction.emoji) == "\U0001F44D" and user == ctx.author
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=60.0
                )
            except asyncio.TimeoutError:
                await reply.remove_reaction("\U0001F44D", self.bot.user)
            else:
                await reply.delete()
        [outfilepath] = Path(outputpath).rglob("ascii_image.txt")
        nome_usuario = ctx.message.author.name
        async with ctx.typing():
            reply_args = {f"content": "Aí está, " + str(nome_usuario),
                    "file": discord.File(outfilepath),}
            reply = await ctx.reply(**reply_args)
        await react_and_wait(reply)

        return

def setup(bot):
    bot.add_cog(toolsimgtotxt(bot))