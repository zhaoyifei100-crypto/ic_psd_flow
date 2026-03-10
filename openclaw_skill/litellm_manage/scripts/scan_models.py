#!/usr/bin/env python3
"""
扫描 OpenAI 兼容 API 的模型列表并生成 opencode 配置文件
使用方式: python3 scan_models.py --url https://www.gsaisg.top/v1 --key your-api-key
"""

import argparse
import json
import re
import sys
from typing import Optional
from urllib import request, error


def fetch_models(base_url: str, api_key: str) -> list:
    """从 OpenAI 兼容 API 获取模型列表"""
    # 移除末尾的 /v1 如果存在
    base = base_url.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]

    url = f"{base}/v1/models"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    req = request.Request(url, headers=headers)

    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("data", [])
    except error.HTTPError as e:
        print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode("utf-8")
            print(f"Response: {error_body}", file=sys.stderr)
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching models: {e}", file=sys.stderr)
        sys.exit(1)


def infer_model_params(model_id: str) -> dict:
    """根据模型 ID 智能推断模型参数"""
    model_id_lower = model_id.lower()

    # GPT-4 系列
    if "gpt-4.5" in model_id_lower or "gpt-4-5" in model_id_lower:
        return {"context": 256000, "output": 16384}
    if "gpt-4o" in model_id_lower:
        if "mini" in model_id_lower:
            return {"context": 128000, "output": 16384}
        return {"context": 128000, "output": 16384}
    if "gpt-4-turbo" in model_id_lower or "gpt-4-turbo-preview" in model_id_lower:
        return {"context": 128000, "output": 4096}
    if "gpt-4-32k" in model_id_lower:
        return {"context": 32768, "output": 4096}
    if "gpt-4" in model_id_lower:
        return {"context": 8192, "output": 4096}

    # GPT-3.5 系列
    if "gpt-3.5-turbo-16k" in model_id_lower or "gpt-35-turbo-16k" in model_id_lower:
        return {"context": 16384, "output": 4096}
    if "gpt-3.5" in model_id_lower or "gpt-35" in model_id_lower:
        return {"context": 4096, "output": 4096}

    # Claude 系列
    if "claude-3-opus" in model_id_lower:
        return {"context": 200000, "output": 4096}
    if "claude-3-sonnet" in model_id_lower:
        return {"context": 200000, "output": 4096}
    if "claude-3-haiku" in model_id_lower:
        return {"context": 200000, "output": 4096}
    if "claude-3-5" in model_id_lower or "claude-3.5" in model_id_lower:
        return {"context": 200000, "output": 8192}
    if "claude-3" in model_id_lower:
        return {"context": 200000, "output": 4096}
    if "claude-2" in model_id_lower:
        return {"context": 100000, "output": 4096}
    if "claude" in model_id_lower:
        return {"context": 100000, "output": 4096}

    # Llama 系列
    if "llama-3.1" in model_id_lower or "llama3.1" in model_id_lower:
        return {"context": 128000, "output": 4096}
    if "llama-3" in model_id_lower or "llama3" in model_id_lower:
        return {"context": 8192, "output": 4096}
    if "llama-2" in model_id_lower or "llama2" in model_id_lower:
        return {"context": 4096, "output": 4096}
    if "llama" in model_id_lower:
        return {"context": 4096, "output": 4096}

    # Mistral 系列
    if "mistral-large" in model_id_lower:
        return {"context": 128000, "output": 4096}
    if "mistral-medium" in model_id_lower:
        return {"context": 32000, "output": 4096}
    if "mistral-small" in model_id_lower:
        return {"context": 32000, "output": 4096}
    if "mistral" in model_id_lower:
        return {"context": 32000, "output": 4096}

    # Gemini 系列
    if "gemini-1.5" in model_id_lower or "gemini1.5" in model_id_lower:
        if "flash" in model_id_lower:
            return {"context": 1000000, "output": 8192}
        return {"context": 1000000, "output": 8192}
    if (
        "gemini-1.0" in model_id_lower
        or "gemini1.0" in model_id_lower
        or "gemini-pro" in model_id_lower
    ):
        return {"context": 32000, "output": 4096}
    if "gemini" in model_id_lower:
        return {"context": 32000, "output": 4096}

    # Qwen 系列
    if "qwen" in model_id_lower:
        if "max" in model_id_lower or "plus" in model_id_lower:
            return {"context": 32000, "output": 8192}
        if "turbo" in model_id_lower:
            return {"context": 8000, "output": 4096}
        return {"context": 32000, "output": 4096}

    # Yi 系列
    if "yi-" in model_id_lower or model_id_lower.startswith("yi"):
        return {"context": 32000, "output": 4096}

    # Baichuan 系列
    if "baichuan" in model_id_lower:
        return {"context": 32000, "output": 4096}

    # ChatGLM 系列
    if "chatglm" in model_id_lower or "glm-" in model_id_lower:
        return {"context": 32000, "output": 4096}

    # DeepSeek 系列
    if "deepseek" in model_id_lower:
        if "coder" in model_id_lower:
            return {"context": 64000, "output": 4096}
        return {"context": 64000, "output": 4096}

    # Codellama 系列
    if "codellama" in model_id_lower:
        return {"context": 16000, "output": 4096}

    # Mixtral 系列
    if "mixtral" in model_id_lower:
        return {"context": 32000, "output": 4096}

    # CodeQwen
    if "codeqwen" in model_id_lower:
        return {"context": 64000, "output": 4096}

    # 默认通用参数
    return {"context": 128000, "output": 4096}


def infer_capabilities(model_id: str) -> dict:
    """根据模型 ID 推断模型能力"""
    model_id_lower = model_id.lower()

    capabilities = {
        "tool_call": True,
        "vision": False,
        "reasoning": False,
    }

    # Vision 模型检测
    vision_keywords = [
        "vision",
        "4o",
        "claude-3",
        "gemini-1.5",
        "llava",
        "qvq",
        "qwen2.5-vl",
    ]
    for keyword in vision_keywords:
        if keyword in model_id_lower:
            capabilities["vision"] = True
            break

    # Reasoning 模型检测
    reasoning_keywords = ["o1", "o3", "reasoning", "r1", "deepseek-reasoner"]
    for keyword in reasoning_keywords:
        if keyword in model_id_lower:
            capabilities["reasoning"] = True
            break

    # Function calling / Tool calling (大部分现代模型都支持，这里检测明确不支持的)
    no_tool_keywords = ["embedding", "embed", "tts", "whisper", "davinci", "babbage"]
    for keyword in no_tool_keywords:
        if keyword in model_id_lower:
            capabilities["tool_call"] = False
            break

    return capabilities


def generate_opencode_config(base_url: str, api_key: str, models: list) -> dict:
    """生成 opencode 配置文件"""
    # 规范化 baseURL (去掉末尾的 /v1)
    base = base_url.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]

    config = {
        "$schema": "https://opencode.ai/config.json",
        "provider": {
            "gsai": {
                "name": "GSAI",
                "npm": "@ai-sdk/openai-compatible",
                "env": [],
                "models": {},
                "options": {"baseURL": f"{base}/v1", "apiKey": api_key},
            }
        },
    }

    for model in models:
        model_id = model.get("id", "")
        if not model_id:
            continue

        # 跳过 embedding 和图像生成模型
        skip_keywords = ["embedding", "embed", "dall-e", "tts", "whisper", "moderation"]
        if any(keyword in model_id.lower() for keyword in skip_keywords):
            continue

        params = infer_model_params(model_id)
        capabilities = infer_capabilities(model_id)

        # 清理 model_id 中的特殊字符，使其适合作为配置键
        model_key = re.sub(r"[^a-zA-Z0-9_-]", "-", model_id)

        config["provider"]["gsai"]["models"][model_key] = {
            "id": model_id,
            "name": model_id,
            "tool_call": capabilities["tool_call"],
            "reasoning": capabilities["reasoning"],
            "limit": {"context": params["context"], "output": params["output"]},
        }

        # 如果是 vision 模型，添加 attachment 支持
        if capabilities["vision"]:
            config["provider"]["gsai"]["models"][model_key]["attachment"] = True

    return config


DESCRIPTION = """
扫描 OpenAI 兼容 API 的模型列表并生成 opencode 配置文件

功能说明:
  本工具自动调用 /v1/models 接口获取所有可用模型，根据模型 ID 智能推断
  模型参数（context window、output limit、capabilities 等），生成 opencode
  可用的配置文件。支持 liteLLM、vLLM、Ollama 等所有 OpenAI 兼容的 API。

支持的模型类型（自动推断参数）:
  - GPT 系列: gpt-4, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
  - Claude 系列: claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3.5
  - Llama 系列: llama-3, llama-2, llama-3.1
  - Gemini 系列: gemini-1.5, gemini-pro
  - Mistral 系列, Qwen 系列, DeepSeek 等主流模型
  - 未知模型: 使用通用默认值 (128k context, 4k output)

能力检测:
  - Vision: 从模型名识别 (vision, 4o, claude-3, gemini-1.5 等)
  - Reasoning: 识别推理模型 (o1, o3, r1, deepseek-reasoner)
  - Tool Calling: 大多数模型默认开启，embedding/tts 类模型关闭

生成配置说明:
  - Provider ID: gsai (自定义 provider)
  - npm 包: @ai-sdk/openai-compatible
  - 自动过滤: embedding、dall-e、tts、whisper、moderation 等非聊天模型
"""

EPILOG = """
使用示例:
  # 基础用法 - 输出到 stdout
  python3 scan_models.py -u http://10.0.20.41:18443/v1 -k sk-xxxx

  # 直接生成配置文件到 opencode 配置目录
  python3 scan_models.py -u http://10.0.20.41:18443/v1 -k sk-xxxx \\
    -o ~/.config/opencode/opencode.json

  # 生成压缩格式的 JSON
  python3 scan_models.py -u http://10.0.20.41:18443/v1 -k sk-xxxx -c

安全建议 - 使用环境变量存储 API Key:
  如果担心 API key 泄露，可以手动修改生成的配置文件：
  
  1. 设置环境变量: export GSAI_API_KEY=your-api-key
  2. 编辑 ~/.config/opencode/opencode.json
  3. 将 "apiKey": "xxx" 改为: "apiKey": "{env:GSAI_API_KEY}"

配置文件位置:
  Linux/macOS: ~/.config/opencode/opencode.json
  Windows: %APPDATA%/opencode/opencode.json

opencode 启动后:
  运行 opencode，在模型选择界面可以看到 gsai/<模型名> 格式的选项
"""


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--url",
        "-u",
        required=True,
        help="API Base URL (例如: http://10.0.20.41:18443/v1)",
    )
    parser.add_argument(
        "--key", "-k", required=True, help="API Key (用于扫描和写入配置)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="-",
        metavar="FILE",
        help="输出文件路径 (默认: - 表示 stdout)",
    )
    parser.add_argument(
        "--pretty",
        "-p",
        action="store_true",
        default=True,
        help="格式化 JSON 输出，带缩进 (默认开启)",
    )
    parser.add_argument(
        "--compact",
        "-c",
        action="store_true",
        help="压缩 JSON 输出，无缩进 (覆盖 --pretty)",
    )

    args = parser.parse_args()

    print(f"正在扫描模型列表: {args.url}", file=sys.stderr)

    models = fetch_models(args.url, args.key)

    if not models:
        print("未找到任何模型", file=sys.stderr)
        sys.exit(1)

    print(f"找到 {len(models)} 个模型", file=sys.stderr)

    # 过滤掉 embedding 等模型后计数
    chat_models = [
        m
        for m in models
        if not any(
            keyword in m.get("id", "").lower()
            for keyword in [
                "embedding",
                "embed",
                "dall-e",
                "tts",
                "whisper",
                "moderation",
            ]
        )
    ]
    print(f"其中 {len(chat_models)} 个聊天模型将被添加", file=sys.stderr)

    config = generate_opencode_config(args.url, args.key, models)

    # 生成 JSON
    indent = 2 if args.pretty and not args.compact else None
    json_output = json.dumps(config, indent=indent, ensure_ascii=False)

    # 输出
    if args.output == "-":
        print(json_output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"配置已保存到: {args.output}", file=sys.stderr)

        # 提示如何复制到 opencode 配置目录
        import os

        opencode_config_dir = os.path.expanduser("~/.config/opencode")
        print(f"\n提示: 复制到 opencode 配置目录:", file=sys.stderr)
        print(
            f"  cp {args.output} {opencode_config_dir}/opencode.json", file=sys.stderr
        )


if __name__ == "__main__":
    main()
