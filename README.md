# AI自媒体剪辑助手

v0.1.0，面向小红书AI自媒体船员的ChatCut云端剪辑Skill。

检查并协助连通ChatCut → 选择主题色 → 沿用主口播尺寸 → 清理气口、停顿、口误和重复 → 按参考或内置风格完成剪辑 → 验收可编辑工程，按要求导出。

## Codex安装

在Codex中发送：

```text
请使用skill-installer安装「AI自媒体剪辑助手」：
https://github.com/wangguoqing123/ai-media-chatcut-editor

Skill在仓库根目录，安装名称为ai-media-chatcut-editor。
请保留SKILL.md及全部references、assets、scripts和agents文件。
安装后检查8份参考说明、6组色板、配色预览和尺寸探测脚本齐全。
如果已有旧版，先检查并备份，只更新此Skill，保留我的素材、偏好与剪辑工程。
```

安装后在下一轮对话调用。需要离线安装时，下载[通用安装包](https://github.com/wangguoqing123/ai-media-chatcut-editor/raw/refs/heads/main/dist/ai-media-chatcut-editor-bundle.zip)，解压后按包内README运行`install.py --check`，检查通过再安装。安装器校验SHA-256，默认拒绝覆盖同名Skill。

## WorkBuddy安装

下载[WorkBuddy安装包](https://github.com/wangguoqing123/ai-media-chatcut-editor/raw/refs/heads/main/dist/ai-media-chatcut-editor-workbuddy.zip)，在技能页面选择“添加技能→上传技能”，导入ZIP并确认启用。使用自定义技能的上传入口，不把通用离线包当成原生Skill上传。

技能安装入口参照[WorkBuddy官方说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。ChatCut连接另按[官方WorkBuddy指南](https://chatcut.io/workbuddy)由助手协助配置；密码、验证码和最终授权在官方页面完成。

## 第一次使用

```text
使用AI自媒体剪辑助手。
请先检查ChatCut云端连接；没有安装或未授权时，带我完成必要步骤并验证到能读取项目列表。
然后让我选择喜欢的色系；我没有偏好时，请按视频类型推荐。
我的主口播：[素材文件或实际项目]
```

只有安装、授权、当前会话工具检查都成功，才表示能开始剪辑。当前会话不能加载新工具时，助手保留已完成步骤并给出续接提示。已有可用连接直接复用，不反复重装。

## 严格参考模式

```text
使用AI自媒体剪辑助手，严格参考模式。
参考视频：[文件]
我的主口播：[文件]
我的素材：[录屏、图片和效果素材]
最终文案：[粘贴]

默认按我的主口播实际显示尺寸和画幅剪，保留原声与自然节奏。
先清理气口、无意义停顿、口误和重复表达。
实际查看参考画面并试听，逐段还原动效、素材出退场、字幕、转场、音效和BGM。
配色策略：[保留参考色／使用已选主题色]
使用我的内容与素材；缺少原曲或工具无法还原的部分，具体说明差异。
请完成完整第一版，交付可编辑ChatCut工程和可观看预览。
```

参考以可观察的表现逐项还原，不只换标题或配色。自己的口播长度与素材决定本片节拍，画幅默认跟随主片。只有实际核验的项目才标完成，缺原音源、未试听或工具能力差异如实列出。

## 常规模式

```text
使用AI自媒体剪辑助手，常规模式。
主口播：[文件]
录屏与效果素材：[文件]
最终文案：[粘贴]
主题色：[P1—P6、自定义颜色或请推荐]
风格：[工具演示、清爽知识、作品展示、轻杂志或请推荐]
按主口播尺寸清理口播，再完成字幕、重点动效、素材效果和声音包装。
```

内置6组色系：电光蓝紫、青绿青柠、奶油珊瑚、暖白琥珀、淡紫莓色、黑白朱红。可下载[配色预览HTML](https://github.com/wangguoqing123/ai-media-chatcut-editor/raw/refs/heads/main/assets/palette-preview.html)后在浏览器打开，多选并复制结果；安装后也可让助手展示色板。

严格参考与个人色板不一致时先明确保留参考色还是替色；不默默混用。常规模式从场景动作库选择有助理解的动作，不机械每隔几秒加特效。不默认加速、变调或强力增强人声。

## 工程与导出

默认给真实可编辑ChatCut云端工程。需要视频文件时发送“请导出成片，并保留可编辑工程”。浏览器渲染与云渲染按[当前官方规则](https://chatcut.io/docs/web-export-limits)处理，完成后核对实际文件，不把预览或完成提示当下载交付。

原片、录屏、字幕、MG动画、音效和背景音乐保留可修改层。不在本地先合成扁平MP4，再上传冒充可编辑工程；本地尺寸探测与验收不属于替代剪辑。

## 文件

- `SKILL.md`：流程与范围。
- `references/`：8份安装、配色、口播清理、参考模式、常规模式、动作库、工具路由、验收交付说明。
- `assets/`：色板、偏好空白示例和离线配色预览。
- `scripts/probe_media.py`：只读核对本地素材显示尺寸、旋转、帧率和时长；需ffprobe，云端素材已有可靠元数据时不用另装。
- `dist/`：通用及WorkBuddy安装包与SHA-256校验值。

## 验证范围

已检查文件完整性、相对引用、安装、拒绝覆盖、篡改检测、色板可读性、配色多选交互，以及真实横屏、竖屏和旋转元数据的尺寸探测。当前作者环境的ChatCut Hosted只读连接已验证。

尚未使用真实口播和参考视频做完整剪辑复刻实测，也未验证接收者新账号OAuth、Windows或Linux实际设备、付费生成与视频导出。本包不含账号凭据、登录状态、私人素材或第三方插件缓存；使用者需要自己的ChatCut账号及授权。
