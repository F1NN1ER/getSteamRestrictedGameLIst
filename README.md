# Steam物品类型数据库
每日自动更新Steam中所有个人资料受限游戏数据，北京时间早晚八点半更新一次

## 说明

全类型数据 `data/fulllist.json`

被下架游戏 `data/banlist.json`

了解中游戏 `data/learninglist.json`

个人资料受限游戏(包含被下架游戏) `data/restrictedlist.json`

受限+了解中游戏(均不计入统计) `data/restrictedandlearninglist.json`


## 预览 data/fulllist.json
`状态码 0:正常 1:了解中 2:受限 3:无效`

    [
        {
            "appid": 5,
            "status": 3
        },
        {
            "appid": 7,
            "status": 3
        },
        {
            "appid": 8,
            "status": 3
        },
        {
            "appid": 10,
            "status": 0
        }
    ]

喜欢的话可以订阅一下我的脚本 [Better SteamPY](https://greasyfork.org/zh-CN/scripts/503737-better-steampy)

>数据来源于`https://store.steampowered.com/`
