# 安装、授权和可用性验证

适用ChatCut官方Hosted云端连接。安装成功后还要完成授权，并在实际执行剪辑的会话调用`list_projects`成功；这三个状态分别核对。当前连接已可用时不重装，不强制升级。

## 官方身份与资料

- 插件仓库：<https://github.com/ChatCut-Inc/agent-plugin>
- Hosted MCP：`https://api.chatcut.io/api/external-mcp/mcp`，服务名通常是`chatcut`。
- 安装说明：<https://chatcut.io/docs/agent-plugin>
- Codex安装入口：<https://chatcut.io/chatgpt>
- WorkBuddy安装入口：<https://chatcut.io/workbuddy>

首次处理新客户端，先读取相应官方页面及宿主CLI帮助，确认当前参数。不要照搬安装网页中自动建新聊天、创建“第一个视频”等演示流程；本Skill保留用户真正的项目和素材。

## Codex：助手主动执行

1. 查找当前会话的Hosted ChatCut工具，调用`list_projects`。成功就结束安装检查，不重新登录。
2. 缺工具时检查实际宿主的Codex CLI和现有`chatcut`注册。使用当前桌面应用提供的CLI，核实版本与`plugin`、`mcp`帮助；不要盲信另一个同名CLI。无法控制用户电脑的远程执行环境，不冒充本机安装。
3. 本Skill实际剪辑请求包含必要的官方插件安装与同连接的定向配置。优先复用已存在的Hosted注册或已安装插件，不重复注册，不覆盖其他MCP服务，不把Desktop服务当成云端。
4. 缺官方插件时，用CLI当前支持的方式添加官方市场，再按返回的真实市场名安装启用插件。常见命令形态如下，执行前核对帮助：

```text
codex plugin marketplace list
codex plugin list --json
codex mcp get chatcut
codex plugin marketplace add https://github.com/ChatCut-Inc/agent-plugin.git --ref main
codex plugin add chatcut@实际返回的市场名
```

5. 需要登录时主动发起`codex mcp login chatcut`，让用户在官方页面登录并允许访问。只保留一个授权进程，跟踪它实际返回的结果。密码、验证码和最终授权由用户完成，不让用户贴到聊天里。
6. 如果宿主只能呈现安装按钮，就带用户完成必要点击，回读实际状态；不能把展示安装入口说成已安装。已有直接Hosted注册可用时也可以继续，不为追求插件形式而重装。
7. 插件无法注册且确实缺失时，按当前官方Hosted基础说明注册同一MCP地址、OAuth resource与所需表面标识header，保留其他配置；不在配置或命令中写入OAuth令牌。不同地址的现有同名服务先说明冲突，不直接改指向。

## WorkBuddy：使用独立的官方接入流程

不要给WorkBuddy运行Codex的登录命令。读取`chatcut.io/workbuddy`的当前完整指南，助手执行配置，用户只在官方授权页登录和确认。

截至2026-10-27，官方WorkBuddy流程使用动态OAuth客户端、PKCE、本机回调以及MCP静态认证header。按官方实际步骤完成注册、发起授权、回调、令牌交换、配置和验证；不能假设WorkBuddy已有`mcp login`。

执行时把PKCE verifier、授权码、access token、refresh token留在受限进程或本机受限凭据文件中，不放命令行参数、日志、剪辑偏好、安装包或聊天输出。官方示例会打印部分中间值，自动执行时改为内部传递；安全校验随机state、PKCE和回调对应关系。只绑定回环地址，结束后关闭回调服务。

配置路径按官方指南核实，目前是`~/.workbuddy/mcp.json`，不是带前导点的另一种文件名。先备份并合并对应`mcpServers.chatcut`项，保留其他服务；有凭据的文件限制为当前用户可读。官方需要静态header时仅写接收者自己的令牌，禁止从作者机器或分享包复制登录状态。检查过期时间，过期时按官方流程安全刷新并更新同一服务。

官方Bash示例在Windows需要按实际Shell适配，不能把复杂Bash原样粘进PowerShell。依赖缺失时具体指出并帮助准备，不把未运行过的路径说成已成功。

## 验证、重开会话与恢复

验证顺序：官方注册正确 → OAuth实际成功 → 当前执行会话出现Hosted工具 → `list_projects`成功。项目列表为空也是成功；能初始化MCP但还不能调用项目工具，只算部分完成。

安装会话可能无法动态加载新工具。先完成能完成的配置检查，再给用户续接提示：

```text
使用AI自媒体剪辑助手继续。
ChatCut安装与授权已完成，请先调用Hosted list_projects验证当前会话可用。
模式：[已选模式]
主题色：[已选颜色或偏好文件位置]
主口播：[用户实际素材位置／项目]
参考视频：[如有]
请保留这些选择，从连接核验后继续剪辑。
```

只有实际成功的步骤才写“已完成”。不自动创建新会话；用户明确要求新任务时再使用对应宿主能力。不把需要新会话误诊为重新安装。

普通网络失败与权限拒绝分开处理。遇到已连接后的请求失败，保存脱敏错误和失败阶段，按官方连接诊断继续；不打印凭据、不反复同时发起登录。同一原因连续失败三次后停止自动重试，给出具体缺口和可执行恢复步骤，保留已完成安装与剪辑状态。用户取消授权就停止相关登录。

只有用户完成必要授权且当前会话通过真实工具检查，才报告“可以开始剪辑”。只编写Skill时最多做只读连接检查，不为验收新建视频项目。
