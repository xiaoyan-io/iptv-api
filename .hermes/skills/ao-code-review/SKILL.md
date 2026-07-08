---
name: ao-code-review
description: 调用 agency-orchestrator (ao) 执行多智能体代码审查、需求拆解、内容审校等复杂工作流
license: MIT
metadata:
  source: ai-lab
  workflow: multi-agent
---

# ao — 多智能体工作流（agency-orchestrator）

## When to Use

| 场景 | 触发词 |
|------|--------|
| 复杂代码审查（安全+性能+规范） | "ao 审查"、"多智能体审查" |
| 一句话生成工作流并执行 | "ao compose" |
| 多轮内容审校流水线 | 写文档/文章，需要多角色协作 |
| 需求拆解 -> 任务分配 | 复杂需求需要 AI 团队协作分析 |
| 复用已有工作流跑任务 | "用上次的流程跑一遍" |

## 不要用 ao 的场景
- 改一个变量、加一个函数 —— OpenCode 自己干更快
- 简单的文件读写 —— 直接操作

## Quick Reference

```bash
# 一句话出结果（生成+运行）
ao compose "审查当前代码，覆盖安全、性能和代码规范" --run

# 只看执行计划再决定
ao compose "审查代码" --provider claude-code
ao plan ao-output/latest/workflow.yaml

# 运行已有工作流
ao run workflow.yaml --watch

# 用已保存的团队跑任务
ao run --team code-review "审查这个 PR"

# 恢复中断的工作流
ao run workflow.yaml --resume last
```

## Procedure

### 代码审查场景
1. 用户说"审查代码"时，先判断任务复杂度
2. 简单修改（<50行改动）—— OpenCode 直接审查
3. 复杂修改（跨文件、安全相关、性能敏感）—— 调 `ao`：
   ```bash
   ao compose "审查 ${files}，检查：1.安全漏洞 2.性能问题 3.代码规范 4.错误处理" --run
   ```
4. 把 ao 的输出结果展示给用户

### 需求拆解场景
```bash
ao compose "分析这个需求，拆成具体的开发任务清单" --run
```

### 内容审校场景
```bash
ao compose "多轮审校这篇文章：编辑→技术审查→终校" --run
```

## Pitfalls
- `ao` 的工作流需要时间（30秒~几分钟），告诉用户"正在用多智能体分析..."
- 确保在项目根目录执行，否则 `ao` 可能找不到工作流文件
- 如果 `ao` 命令不存在，提醒用户安装：`npm install -g agency-orchestrator`

## Verification
- `ao compose` 成功会输出 `✅ 工作流已保存到 ao-output/`
- `ao run` 成功会在 `ao-output/` 下生成完整结果
