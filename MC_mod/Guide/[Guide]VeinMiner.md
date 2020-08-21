[官方原始教程](https://www.minecraftforum.net/forums/mapping-and-modding-java-edition/minecraft-mods/1292260-1-5-1-11-2-vein-miner-quickly-mine-veins-of-ore#entry25004277)

## 中文某网站翻译：

矿脉矿工有几种模式，根据不同情况启用不同模式来获得更大的效率，可以为每位玩家指定不同的模式。

- ‘Disabled’: 禁用,没有安装Mod的玩家，默认使禁用.
- ‘Auto’: 按下按键，默认是’~`，激活
- ‘Sneak’: 潜行的时候启用，安装Mod的客户端默认设置.
- ‘No Sneak’: 在非潜行状态启用.

你可以使用 ‘/veinminer‘ 命令来改变你的模式.比如输入’/veinminer enable ‘可以替换为 ‘‘ ‘disable;, ‘auto’; ‘sneak’; 或 ‘no_sneak’.使用 ‘/veinminer help enable‘ 查看帮助.

## 英文原贴复制粘贴：

Using
To use Veinminer, you need to have Veinminer installed on the server (for single player games the client and the server are the same). You do not need to have Veinminer installed on the client, however it will provide reduced functionality to the clients that do not have it installed.

In order to get the most out of Veinminer, you should edit the VeinMiner.cfg config file. Add the ids of the blocks to the different block lists to that you wish to be able to mine using Veinminer. Add any tools that you want to be able to use to use with Veinminer. The IDs should be changed on the server.

The default config file has the vanilla ores added for the pickaxes, vanilla wood added for the vanilla axes and clay for the shovel.

VeinMiner has several modes, each of which determine when it is activated. Modes are specific to each player.

- 'Disabled': Don't activate at all. This is the default if you don't have the mod installed in the client.
- 'Auto': Activate when the keyboard shortcut (also called a keybind) is pressed in the client. The keyboard shortcut by default is '~`.
 'Sneak': Activate while you are sneaking. This is the same option as provided by Connected Destruction. This is the default if you have the client.
 'No Sneak': Activate while you are not sneaking.

The client setting in the config file allows you to choose what mode you go into when you join a game. To set the default mod to disabled, set the shortcut to an unused key.You can use the
```
/veinminer
```


command to change the mode that VeinMiner is in for you. This can be done with
```
/veinminer mode 
```


where is one of 'disable;, 'auto'; 'sneak'; or 'no_sneak'. You can use
```
/veinminer help enable
```
