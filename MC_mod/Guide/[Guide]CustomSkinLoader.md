# 安装与测试

下载Mod放置于Mod文件夹内

选择一个皮肤站，推荐使用https://littleskin.cn/user或者http://www.skinme.cc/skinme/index/closet

根据皮肤站教程对D:\Minecraft\.minecraft\CustomSkinLoader下CustomSkinLoader.json进行修改（skime不需要修改）

前往各个皮肤站选购皮肤，角色名称需要与登录游戏时候使用的人物名称保持一致

进入游戏检查皮肤效果

# 显示不成功debug

## 皮肤加载的原理

- **客户端**按照"loadlist"列表中的顺序将将**用户名称**发给**皮肤服务器**
- **皮肤服务器**通过**用户名称**匹配
- 如果没有成功匹配，**客户端**将发送**用户名称**至列表中下一个**皮肤服务器**
- 如果成功匹配，**皮肤服务器**发送皮肤给各个**客户端**

```
"loadlist": [
   {
     "name": "LittleSkin",
     "type": "CustomSkinAPI",
     "root": "https://mcskin.littleservice.cn/csl/"
   },
   {
     "name": "SkinMe",
     "type": "UniSkinAPI",
     "root": "http://www.skinme.cc/uniskin/"
   },

```
## 皮肤加载原理带来的问题

**问题1：**

如果用户名重名的话， **皮肤服务器**可能发送别人的皮肤给你

**解决方案：**

换一个皮肤服务器注册试试

**问题1：**

如果**皮肤服务器**顺序不对的话，可能前面**皮肤服务器**有人与你重名，于是客户端没有收到对应**皮肤服务器**的皮肤

**解决方案：**

调整CustomSkinLoader.jso文件中的变量顺序

## 其他皮肤服务器

如果上述两个**皮肤服务器都不行**，还可以尝试https://skin.prinzeugen.net,http://fleey.org/,http://www.mcskin.cc/
