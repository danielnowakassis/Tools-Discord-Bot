#Code adapted for windows from : https://github.com/ManimCommunity/DiscordManimator
import asyncio
import os
import re
from pathlib import Path
import discord
from discord.ext import commands
import subprocess


outputpath = ''

class Manimate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="tmanimate", aliases=["m"])
    @commands.guild_only()
    async def manimate(self, ctx, *, arg):
        def construct_reply(arg):
            if arg.startswith("```"):  # empty header
                arg = "\n" + arg
            header, *body = arg.split("\n")

            cli_flags = header.split()
            allowed_flags = [
                "-i",
                "--save_as_gif",
                "-s",
                "--save_last_frame",
                "-t",
                "--transparent",
                "--renderer=opengl",
                "--use_projection_fill_shaders",
                "--use_projection_stroke_shaders"
            ]

            if not all([flag in allowed_flags for flag in cli_flags]):
                reply_args = {
                    "content": "You cannot pass CLI flags other than "
                    "`-i` (`--save_as_gif`), `-s` (`--save_last_frame`), "
                    "`-t` (`--transparent`), `--renderer=opengl`, "
                    "`--use_projection_fill_shaders` or "
                    "`--use_projection_stroke_shaders`."
                }
                return reply_args
            if "--renderer=opengl" in cli_flags:
                cli_flags.append("--write_to_movie")
            cli_flags = " ".join(cli_flags)


            body = "\n".join(body).strip()

            if body.count("```") != 2:
                reply_args = {
                    "content": "Your message is not properly formatted. "
                    "Your code has to be written in a code block, like so:\n"
                    "\\`\\`\\`py\nyour code here\n\\`\\`\\`"
                }
                return reply_args

            script = re.search(
                pattern=r"```(?:py)?(?:thon)?(.*)```",
                string=body,
                flags=re.DOTALL,
            ).group(1)
            script = script.strip()

            # for convenience: allow construct-only:
            if script.startswith("def construct(self):"):
                script = ["class Manimation(Scene):"] + [
                    "    " + line for line in script.split("\n")
                ]
            else:
                script = script.split("\n")

            prescript = ["from manim import *"]
            script = prescript + script

            if len(os.listdir(outputpath)) != 0:
                for root, dirs, files in os.walk(outputpath, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
            scriptfile = Path(outputpath) / "script.py"
            #lugar = 'C:\Users\daniel\Desktop\testemanimce\script.py'
            with open(scriptfile, "w", encoding="utf-8") as f:
                f.write("\n".join(script))

            reply_args = None

                
            proc = subprocess.run(
                f"manim -qh --media_dir {outputpath} -o scriptoutput {cli_flags} {scriptfile}",
                shell=True,
                stderr=subprocess.PIPE,
            )
                
                
            [outfilepath] = Path(outputpath).rglob("scriptoutput.*")
                
                
            reply_args = {
                "content": "Here you go:",
                "file": discord.File(outfilepath),
            }

            return reply_args

        async def react_and_wait(reply):
            await reply.add_reaction("\U0001F5D1")  # Trashcan emoji

            def check(reaction, user):
                return str(reaction.emoji) == "\U0001F5D1" and user == ctx.author

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=60.0
                )
            except asyncio.TimeoutError:
                await reply.remove_reaction("\U0001F5D1", self.bot.user)
            else:
                await reply.delete()

        async with ctx.typing():
            reply_args = construct_reply(arg)
            reply = await ctx.reply(**reply_args)

        await react_and_wait(reply)
        return


def setup(bot):
    bot.add_cog(Manimate(bot))
