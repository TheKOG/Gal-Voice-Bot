from email.headerregistry import Group
from typing import Tuple, Any
from string import Template
import requests
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed,Bot,MessageEvent
import VITS
from VITS import Trans,Trans2
from config import BotSelfConfig

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-atri",
    description="ATRI VITS 模型拟声",
    usage="ATRI\n" +
          "- 说(日语)\n",
    extra={
        "unique_name": "Gal-Voice",
        "example": "说お兄ちゃん大好き",
        "author": "KOG <1458038842@qq.com>",
        "version": "0.0.1",
    },
)

import os
# api for other plugins
def atri_func(msg):
    Trans(msg,'voice.wav')
    voice=f'file:///'+os.getcwd()+'/voice.wav'
    return MessageSegment.record(voice)

yozo_dict = {"宁宁": 0, "爱瑠": 1, "芳乃": 2, "茉子": 3, "丛雨": 4, "小春": 5, "七海": 6, }
def yozo_func(msg,name):
    Trans2(msg,yozo_dict[name],'voice.wav')
    voice=f'file:///'+os.getcwd()+'/voice.wav'
    return MessageSegment.record(voice)

cnapi = Template("http://233366.proxy.nscc-gz.cn:8888?speaker=${id}&text=${text}")
def gs_func(msg, name='派蒙'):
    voice = requests.get(cnapi.substitute(text=msg, id=name)).content
    return MessageSegment.record(voice)

Priority = 5

gp=True
send_id=1458038842
g_p_regex = "^(群聊|私聊)(.+)$"
g_p_cmd = on_regex(g_p_regex, block=True, priority=Priority)

def atoi(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num

@g_p_cmd.handle()
async def _(event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    g_p,id = matched[0],matched[1]
    user_id = event.get_user_id()
    if user_id not in BotSelfConfig.superusers:
        await g_p_cmd.finish('权限不足')
    global gp
    global send_id
    send_id=atoi(id)
    if(g_p=='群聊'):
        gp=True
        # print("切换至群聊对象{0}".format(send_id))
        await g_p_cmd.finish("切换至群聊对象{0}".format(send_id))
    else:
        gp=False
        # print("切换至私聊对象{0}".format(send_id))
        await g_p_cmd.finish("切换至私聊对象{0}".format(send_id))

atri_regex = "^(?:亚托莉|)(发送|说)(.+)$"
yozo_regex = "^(宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海)(发送|说)(.+)$"
gs_regex = "^(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)(发送|说)(.+)$"

atri_cmd = on_regex(atri_regex, block=True, priority=Priority)
gs_cmd = on_regex(gs_regex, block=True, priority=Priority)
yozo_cmd = on_regex(yozo_regex, block=True, priority=Priority)


@atri_cmd.handle()
async def _(bot:Bot,event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    cmd,msg = matched[0],matched[1]
    if(cmd=='发送'):
        user_id = event.get_user_id()
        if user_id not in BotSelfConfig.superusers:
            await atri_cmd.finish('权限不足')
        try:
            if(gp):
                await bot.send_group_msg(group_id=send_id,message=atri_func(msg=msg))
            else:
                await bot.send_private_msg(user_id=send_id,message=atri_func(msg=msg))
            await atri_cmd.finish('发送成功')
        except ActionFailed as e:
            await atri_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
    else:
        try:
            if(gp):
                await atri_cmd.finish(message=atri_func(msg=msg))
            else:
                await atri_cmd.finish(message=atri_func(msg=msg))
        except ActionFailed as e:
            await atri_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')


@yozo_cmd.handle()
async def _(bot:Bot,event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    name,cmd,msg = matched[0],matched[1],matched[2]
    if cmd=='发送':
        user_id = event.get_user_id()
        if user_id not in BotSelfConfig.superusers:
            await yozo_cmd.finish('权限不足')
        try:
            if(gp):
                await bot.send_group_msg(group_id=send_id,message=yozo_func(msg=msg,name=name))
            else:
                await bot.send_private_msg(user_id=send_id,message=yozo_func(msg=msg,name=name))
            await yozo_cmd.finish('发送成功')
        except ActionFailed as e:
            await yozo_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
    else:
        try:
            if(gp):
                await yozo_cmd.finish(message=yozo_func(msg=msg,name=name))
            else:
                await yozo_cmd.finish(message=yozo_func(msg=msg,name=name))
        except ActionFailed as e:
            await yozo_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')


@gs_cmd.handle()
async def _(bot:Bot,event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    name,cmd,msg = matched[0],matched[1],matched[2]
    if cmd=='发送':
        user_id = event.get_user_id()
        if user_id not in BotSelfConfig.superusers:
            await gs_cmd.finish('权限不足')
        try:
            if(gp):
                await bot.send_group_msg(group_id=send_id,message=gs_func(msg=msg, name=name))
            else:
                await bot.send_private_msg(user_id=send_id,message=gs_func(msg=msg, name=name))
            await gs_cmd.finish('发送成功')
        except ActionFailed as e:
            await gs_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
    else:
        try:
            if(gp):
                await gs_cmd.finish(message=gs_func(msg=msg, name=name))
            else:
                await gs_cmd.finish(message=gs_func(msg=msg, name=name))
        except ActionFailed as e:
            await gs_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
