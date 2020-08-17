#安装与测试

下载Mod放置于Mod文件夹内

选择一个皮肤站，推荐使用https://littleskin.cn/user或者http://www.skinme.cc/skinme/index/closet

根据皮肤站教程对D:\Minecraft\.minecraft\CustomSkinLoader下CustomSkinLoader.json进行修改（skime不需要修改）

前往各个皮肤站选购皮肤，角色名称需要与登录游戏时候使用的人物名称保持一致

进入游戏检查皮肤效果

#显示不成功debug

皮肤加载的原理是通过

'''
 "loadlist": [
    {
      "name": "LittleSkin",
      "type": "CustomSkinAPI",
      "root": "https://mcskin.littleservice.cn/csl/"
    },
    {
      "name": "Mojang",
      "type": "MojangAPI"
    },
    {
      "name": "BlessingSkin",
      "type": "CustomSkinAPI",
      "root": "https://skin.prinzeugen.net/csl/"
    },
    {
      "name": "OneSkin",
      "type": "CustomSkinAPI",
      "root": "http://fleey.org/skin/skin_user/skin_json.php/"
    },
    {
      "name": "SkinMe",
      "type": "UniSkinAPI",
      "root": "http://www.skinme.cc/uniskin/"
    },
    {
      "name": "McSkin",
      "type": "CustomSkinAPI",
      "root": "http://www.mcskin.cc/"
    }
  ],
'''
