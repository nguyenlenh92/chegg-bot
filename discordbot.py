import os
import sys
import psutil
import logging
import discord
from chegg_v1 import main
from chegg_v1 import openDriver
from chegg_v1 import closeDriver
from chegg_v1 import get_answers

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    openDriver()
    
    


@client.event
async def on_message(message):
    #if message.author == client.user:
        #return
    if message.content.startswith('>find '):
        args = message.content.split(" ")
        #url = args[1].split('/')
        url = args[1]
        if('www.chegg.com' in url):
            #ans_arr = []
            #main(args[1],ans_arr)
            await message.channel.send("loading")
            ans_arr = (get_answers(url, []))
            if(ans_arr == -1):
                
                await message.channel.send('<@117828594025103369>'+ " fix me bitch")
            
            elif (len(ans_arr) == 0):
                apol = '{0.author.mention} Sorry,the answer could not be found'.format(message)
                await message.channel.send(apol)
            else:
                mention = '{0.author.mention}'.format(message)
                await message.channel.send(mention)
                for i in ans_arr:
                    await message.channel.send(i)
            
        else:
            msg = '{0.author.mention} send a chegg link monkey'.format(message)
            await message.channel.send(msg)
    if message.content.startswith('>clean '):
        del_args = message.content.split(" ")
        n = (int)(del_args[1])
        await message.channel.purge(limit = n)
    if message.content.startswith('>reboot'):
        await message.channel.send("rebooting")
        try:
            closeDriver()
            p = psutil.Process(os.getpid())
            for handler in p.open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)

        python = sys.executable
        os.execl(python, python, *sys.argv)
     


client.run('NzM4NTg5NDE1NTIxMjU1NTE1.XyOG_g.k02eSPsgYV0YQFSsb_9MgM4w8Y4')