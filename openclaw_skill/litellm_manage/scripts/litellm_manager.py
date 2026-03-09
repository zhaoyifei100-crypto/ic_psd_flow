#!/usr/bin/env python3
"""
LiteLLM Management CLI - Official API Implementation

Docs: https://docs.litellm.ai/docs/proxy/management_cli

Usage:
    python litellm_manager.py --help
    python litellm_manager.py status
    python litellm_manager.py key list
    python litellm_manager.py key generate --alias "员工" --budget 20
    python litellm_manager.py key delete --key "sk-xxx"
    python litellm_manager.py key info --key "sk-xxx"
    python litellm_manager.py key regenerate --key "sk-xxx"
    python litellm_manager.py user list
    python litellm_manager.py user new --username "员工" --budget 20
    python litellm_manager.py team list
    python litellm_manager.py team new --name "研发组"
    python litellm_manager.py test --model qwen3.5-plus
    python litellm_manager.py config openai --output ~/.openai.json
    python litellm_manager.py restart
"""

import os
import sys
import json
import argparse
import subprocess
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

# Configuration
LITELLM_HOST = os.getenv("LITELLM_HOST", "8.216.45.80")
LITELLM_PORT = os.getenv("LITELLM_PORT", "4000")
LITELLM_SSH_PORT = os.getenv("LITELLM_SSH_PORT", "2222")
LITELLM_SSH_KEY = os.getenv("LITELLM_SSH_KEY", "~/.ssh/ecs_key")
SSH_USER = os.getenv("SSH_USER", "root")

LITELLM_SSH_KEY = os.path.expanduser(LITELLM_SSH_KEY)
BASE_URL = f"http://{LITELLM_HOST}:{LITELLM_PORT}"
SSH_BASE = f"ssh -i {LITELLM_SSH_KEY} -p {LITELLM_SSH_PORT} -o ConnectTimeout=10 {SSH_USER}@{LITELLM_HOST}"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def get_master_key() -> str:
    """Get LiteLLM master key."""
    key = os.getenv("LITELLM_MASTER_KEY")
    if not key:
        result = subprocess.run(
            f"{SSH_BASE} \"grep LITELLM_MASTER_KEY /opt/litellm/.env | cut -d= -f2\"",
            shell=True, capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            key = result.stdout.strip()
    return key or "sk-litellm-admin-key-change-me"


def ssh_exec(command: str) -> str:
    """Execute command on LiteLLM VPS."""
    full_cmd = f'{SSH_BASE} "{command}"'
    result = subprocess.run(
        full_cmd, shell=True, capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"SSH error: {result.stderr}")
    return result.stdout.strip()


def api_call(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make API call via SSH tunnel."""
    import base64
    
    master_key = get_master_key()
    
    if data:
        # Write payload to temp file using base64
        payload_b64 = base64.b64encode(json.dumps(data).encode()).decode()
        ssh_exec(f"echo '{payload_b64}' | base64 -d > /tmp/litellm_req.json")
        json_file = "-d @/tmp/litellm_req.json"
    else:
        json_file = ""
    
    cmd = f'{SSH_BASE} "curl -s -X {method} -H \\"Authorization: Bearer {master_key}\\" -H \\"Content-Type: application/json\\" {json_file} \'http://localhost:4000{endpoint}\'"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
    
    if data:
        ssh_exec("rm -f /tmp/litellm_req.json")
    
    if result.returncode != 0:
        raise RuntimeError(f"API error: {result.stderr}")
    
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout}


def print_status(healthy: bool, msg: str = ""):
    """Print colored status."""
    if healthy:
        print(f"{GREEN}✓{RESET} {msg}")
    else:
        print(f"{RED}✗{RESET} {msg}")


# ==================== Status ====================

def cmd_status():
    """Check overall status."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}LiteLLM Gateway Status{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Health check
    try:
        health = api_call("GET", "/health")
        healthy_endpoints = health.get("healthy_endpoints", [])
        unhealthy_endpoints = health.get("unhealthy_endpoints", [])
        
        print_status(True, f"Service Running")
        print(f"  Healthy endpoints: {len(healthy_endpoints)}")
        print(f"  Unhealthy endpoints: {len(unhealthy_endpoints)}")
        
        if healthy_endpoints:
            print(f"\n{BLUE}Available Models:{RESET}")
            for ep in healthy_endpoints[:15]:
                model = ep.get("model", "unknown")
                print(f"  • {model}")
            if len(healthy_endpoints) > 15:
                print(f"  ... and {len(healthy_endpoints) - 15} more")
    except Exception as e:
        print_status(False, f"Service Error: {e}")
    
    # Key count
    try:
        result = api_call("GET", "/key/list", {"limit": 100})
        key_strings = result.get("keys", [])
        
        # Get spend info
        total_spend = 0
        active = 0
        for key_str in key_strings[:10]:  # Just check first 10 for performance
            try:
                info = api_call("GET", "/key/info", {"key": key_str})
                if "info" in info:
                    total_spend += info["info"].get("spend", 0)
                    if info["info"].get("last_active"):
                        active += 1
            except:
                pass
        
        print(f"\n{BLUE}API Keys:{RESET}")
        print(f"  Total: {len(key_strings)}")
        print(f"  Total Spend: ${total_spend:.2f}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Team count
    try:
        teams = api_call("GET", "/team/list")
        team_list = teams.get("teams", [])
        print(f"\n{BLUE}Teams:{RESET}")
        print(f"  Total: {len(team_list)}")
    except:
        pass
    
    print()


# ==================== Key Management ====================

def cmd_key_list():
    """List all API keys."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}API Keys{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Get key list (returns only key strings)
    result = api_call("GET", "/key/list", {"limit": 100})
    key_strings = result.get("keys", [])
    
    if not key_strings:
        print("No keys found.")
        return
    
    print(f"Total: {len(key_strings)} keys\n")
    print("Key Strings:")
    for i, k in enumerate(key_strings, 1):
        print(f"  {i}. {k}")


def cmd_key_generate(args):
    """Generate new API key."""
    print(f"\nGenerating new API key...")
    
    data = {
        "key_alias": args.alias,
        "max_budget": args.budget,
    }
    
    if args.duration:
        data["duration"] = args.duration
    
    if args.models:
        data["models"] = [m.strip() for m in args.models.split(",")]
    
    if args.rpm:
        data["rpm_limit"] = args.rpm
    
    if args.tpm:
        data["tpm_limit"] = args.tpm
    
    if args.expires:
        data["expires"] = args.expires
    
    result = api_call("POST", "/key/generate", data)
    
    new_key = result.get("key") or result.get("token")
    
    if new_key:
        print_status(True, f"API Key created!")
        print(f"  Alias: {args.alias}")
        print(f"  Key: {new_key}")
        print(f"  Budget: ${args.budget}/month")
        print(f"  Models: {args.models or 'All'}")
        
        if args.save:
            save_path = os.path.expanduser(args.save)
            with open(save_path, "w") as f:
                json.dump({"api_key": new_key, "alias": args.alias, "budget": args.budget}, f, indent=2)
            print(f"  Saved to: {save_path}")
    else:
        print_status(False, f"Failed: {result}")


def cmd_key_delete(args):
    """Delete API key."""
    key = args.key
    
    # First get key info
    result = api_call("GET", "/key/list", {"limit": 100})
    keys = result.get("keys", [])
    
    # Find key
    key_to_delete = None
    for k in keys:
        if key in (k.get("key") or ""):
            key_to_delete = k.get("key")
            break
        if key in (k.get("token") or ""):
            key_to_delete = k.get("token")
            break
        if key == k.get("key_alias"):
            key_to_delete = k.get("key")
            break
    
    if not key_to_delete:
        print_status(False, f"Key not found: {key}")
        return
    
    # Delete via API
    delete_result = api_call("POST", "/key/delete", {"keys": [key_to_delete]})
    
    if "error" not in str(delete_result).lower():
        print_status(True, f"Key deleted: {key_to_delete[:12]}...")
    else:
        print_status(False, f"Delete failed: {delete_result}")


def cmd_key_info(args):
    """Get key info."""
    key = args.key
    
    # Find key
    result = api_call("GET", "/key/list", {"limit": 100})
    keys = result.get("keys", [])
    
    for k in keys:
        if key in (k.get("key") or "") or key in (k.get("token") or "") or key == k.get("key_alias"):
            print(f"\n{BLUE}Key Info:{RESET}")
            print(f"  Alias: {k.get('key_alias') or k.get('key_name')}")
            print(f"  Key: {k.get('key') or k.get('token')}")
            print(f"  Spend: ${k.get('spend', 0):.2f}")
            print(f"  Budget: ${k.get('max_budget', 0):.2f}")
            print(f"  Budget Reset: {k.get('budget_reset_at') or 'N/A'}")
            print(f"  Expires: {k.get('expires') or 'Never'}")
            print(f"  Created: {k.get('created_at')}")
            print(f"  Last Active: {k.get('last_active') or 'Never'}")
            print(f"  Models: {', '.join(k.get('models', [])) or 'All'}")
            
            spend = k.get("spend", 0)
            budget = k.get("max_budget", 1)
            percent = spend / budget * 100 if budget > 0 else 0
            
            print(f"\n  Usage: {percent:.1f}%")
            if percent > 80:
                print_status(False, "  ⚠️ Budget warning!")
            return
    
    print_status(False, f"Key not found: {key}")


def cmd_key_regenerate(args):
    """Regenerate (rotate) API key."""
    key = args.key
    
    # Find key
    result = api_call("GET", "/key/list", {"limit": 100})
    keys = result.get("keys", [])
    
    old_key = None
    for k in keys:
        if key in (k.get("key") or "") or key in (k.get("token") or "") or key == k.get("key_alias"):
            old_key = k.get("key")
            break
    
    if not old_key:
        print_status(False, f"Key not found: {key}")
        return
    
    # Regenerate
    regen_result = api_call("POST", "/key/regenerate", {"key": old_key})
    
    new_key = regen_result.get("key") or regen_result.get("token")
    
    if new_key:
        print_status(True, "Key regenerated!")
        print(f"  Old: {old_key[:12]}...")
        print(f"  New: {new_key}")
    else:
        print_status(False, f"Failed: {regen_result}")


# ==================== User Management ====================

def cmd_user_list():
    """List all users."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Users{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    result = api_call("GET", "/user/list")
    users = result.get("users", [])
    
    if not users:
        print("No users found.")
        return
    
    print(f"{'User ID':<30} {'Email':<30} {'Created'}")
    print("-" * 90)
    
    for u in users:
        user_id = u.get("user_id", "N/A")[:28]
        email = u.get("user_email") or "N/A"
        created = u.get("created_at", "")[:19] if u.get("created_at") else "N/A"
        
        print(f"{user_id:<30} {email:<30} {created}")
    
    print(f"\nTotal: {len(users)} users")


def cmd_user_new(args):
    """Create new user."""
    print(f"\nCreating user...")
    
    data = {
        "user_alias": args.username,
    }
    
    if args.email:
        data["user_email"] = args.email
    
    if args.budget:
        data["max_budget"] = args.budget
    
    result = api_call("POST", "/user/new", data)
    
    if result.get("user_id"):
        print_status(True, f"User created!")
        print(f"  Alias: {args.username}")
        print(f"  User ID: {result.get('user_id')}")
    else:
        print_status(False, f"Failed: {result}")


def cmd_user_delete(args):
    """Delete user."""
    result = api_call("POST", "/user/delete", {"user_ids": [args.user_id]})
    
    if "error" not in str(result).lower():
        print_status(True, f"User deleted: {args.user_id}")
    else:
        print_status(False, f"Failed: {result}")


# ==================== Team Management ====================

def cmd_team_list():
    """List all teams."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Teams{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    result = api_call("GET", "/team/list")
    
    # Handle different response formats
    if isinstance(result, list):
        teams = result
    else:
        teams = result.get("teams", [])
    
    if not teams:
        print("No teams found.")
        return
    
    print(f"{'Team ID':<25} {'Alias':<20} {'Spend':<12} {'Budget':<12} {'Members'}")
    print("-" * 90)
    
    for t in teams:
        team_id = str(t.get("team_id", ""))[:23]
        alias = t.get("team_alias") or "N/A"
        spend = f"${t.get('team_spend', 0):.2f}"
        budget = f"${t.get('team_max_budget', 0):.2f}"
        members = str(t.get("team_members", []))[:20]
        
        print(f"{team_id:<25} {alias:<20} {spend:<12} {budget:<12} {members}")
    
    print(f"\nTotal: {len(teams)} teams")


def cmd_team_new(args):
    """Create new team."""
    print(f"\nCreating team...")
    
    data = {
        "team_alias": args.name,
    }
    
    if args.budget:
        data["team_max_budget"] = args.budget
    
    result = api_call("POST", "/team/new", data)
    
    if result.get("team_id"):
        print_status(True, f"Team created!")
        print(f"  Name: {args.name}")
        print(f"  Team ID: {result.get('team_id')}")
    else:
        print_status(False, f"Failed: {result}")


def cmd_team_delete(args):
    """Delete team."""
    result = api_call("POST", "/team/delete", {"team_ids": [args.team_id]})
    
    if "error" not in str(result).lower():
        print_status(True, f"Team deleted: {args.team_id}")
    else:
        print_status(False, f"Failed: {result}")


# ==================== Model Testing ====================

def cmd_test(args):
    """Test model connectivity."""
    model = args.model or "qwen3.5-plus"
    api_key = args.key or get_master_key()
    
    print(f"\n{BLUE}Testing Model:{RESET} {model}")
    print(f"API Key: {api_key[:12]}...\n")
    
    import base64
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say 'OK' in one word."}],
        "max_tokens": 10
    }
    
    # Write payload via SSH
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()
    ssh_exec(f"echo '{payload_b64}' | base64 -d > /tmp/litellm_test.json")
    
    cmd = f'{SSH_BASE} "curl -s -X POST -H \\"Authorization: Bearer {api_key}\\" -H \\"Content-Type: application/json\\" -d @/tmp/litellm_test.json \'http://localhost:4000/v1/chat/completions\'"'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
    ssh_exec("rm -f /tmp/litellm_test.json")
    
    if result.returncode != 0:
        print_status(False, f"Error: {result.stderr}")
        return
    
    try:
        data = json.loads(result.stdout)
        
        if "choices" in data:
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = data.get("usage", {})
            
            print_status(True, "Success!")
            print(f"  Response: {content}")
            print(f"  Usage: {usage}")
        elif "error" in data:
            print_status(False, f"API Error: {data['error']}")
        else:
            print(f"Result: {data}")
            
    except json.JSONDecodeError:
        print_status(False, f"Invalid response: {result.stdout[:200]}")


# ==================== Config Generation ====================

def cmd_config_openai(args):
    """Generate OpenAI compatible config."""
    output_path = os.path.expanduser(args.output)
    
    # Get keys
    keys = api_call("GET", "/key/list", {"limit": 1})
    key_list = keys.get("keys", [])
    
    if not key_list:
        print_status(False, "No API keys found")
        return
    
    # Get models
    health = api_call("GET", "/health")
    models = [ep.get("model") for ep in health.get("healthy_endpoints", [])]
    
    config = {
        "base_url": BASE_URL,
        "api_key": key_list[0].get("key") or key_list[0].get("token"),
        "models": models,
    }
    
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print_status(True, f"Config saved to: {output_path}")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Models: {len(models)}")


# ==================== Service Control ====================

def cmd_restart():
    """Restart LiteLLM service."""
    print(f"\n{YELLOW}Restarting LiteLLM service...{RESET}")
    
    try:
        ssh_exec("cd /opt/litellm && docker-compose restart litellm")
        print_status(True, "Service restarted!")
        
        import time
        print("Waiting for service to start...")
        time.sleep(5)
        
        cmd_status()
    except Exception as e:
        print_status(False, f"Failed: {e}")


def cmd_logs(args):
    """Get logs."""
    lines = args.lines or 50
    
    try:
        output = ssh_exec(f"docker logs litellm --tail {lines} 2>&1")
        print(output)
    except Exception as e:
        print_status(False, f"Failed: {e}")


# ==================== Main ====================

def main():
    parser = argparse.ArgumentParser(
        description="LiteLLM Management CLI (Official API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Status
  %(prog)s status
  
  # Key management
  %(prog)s key list
  %(prog)s key generate --alias "员工" --budget 20
  %(prog)s key generate --alias "研发" --budget 10 --models "qwen3.5-plus,kimi-k2.5"
  %(prog)s key info --key sk-xxx
  %(prog)s key delete --key sk-xxx
  %(prog)s key regenerate --key sk-xxx
  
  # User management
  %(prog)s user list
  %(prog)s user new --username "员工" --budget 20
  %(prog)s user delete --user-id xxx
  
  # Team management
  %(prog)s team list
  %(prog)s team new --name "研发组" --budget 100
  
  # Test
  %(prog)s test --model qwen3.5-plus
  
  # Config
  %(prog)s config openai --output ~/.openai.json
  
  # Service
  %(prog)s restart
  %(prog)s logs --lines 100
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status
    subparsers.add_parser("status", help="Check status")
    
    # Key
    key_parser = subparsers.add_parser("key", help="Key management")
    key_sub = key_parser.add_subparsers(dest="key_command")
    
    key_sub.add_parser("list", help="List keys")
    
    key_gen = key_sub.add_parser("generate", help="Generate key")
    key_gen.add_argument("--alias", required=True, help="Key alias")
    key_gen.add_argument("--budget", type=float, default=20, help="Monthly budget")
    key_gen.add_argument("--duration", help="Duration (e.g., 1month)")
    key_gen.add_argument("--models", help="Comma-separated models")
    key_gen.add_argument("--rpm", type=int, help="RPM limit")
    key_gen.add_argument("--tpm", type=int, help="TPM limit")
    key_gen.add_argument("--expires", help="Expiration date")
    key_gen.add_argument("--save", help="Save to file")
    
    key_del = key_sub.add_parser("delete", help="Delete key")
    key_del.add_argument("--key", required=True, help="Key or alias")
    
    key_info = key_sub.add_parser("info", help="Get key info")
    key_info.add_argument("--key", required=True, help="Key or alias")
    
    key_regen = key_sub.add_parser("regenerate", help="Regenerate key")
    key_regen.add_argument("--key", required=True, help="Key or alias")
    
    # User
    user_parser = subparsers.add_parser("user", help="User management")
    user_sub = user_parser.add_subparsers(dest="user_command")
    
    user_sub.add_parser("list", help="List users")
    
    user_new = user_sub.add_parser("new", help="Create user")
    user_new.add_argument("--username", required=True, help="Username")
    user_new.add_argument("--email", help="Email")
    user_new.add_argument("--budget", type=float, help="Budget")
    
    user_del = user_sub.add_parser("delete", help="Delete user")
    user_del.add_argument("--user-id", required=True, help="User ID")
    
    # Team
    team_parser = subparsers.add_parser("team", help="Team management")
    team_sub = team_parser.add_subparsers(dest="team_command")
    
    team_sub.add_parser("list", help="List teams")
    
    team_new = team_sub.add_parser("new", help="Create team")
    team_new.add_argument("--name", required=True, help="Team name")
    team_new.add_argument("--budget", type=float, help="Team budget")
    
    team_del = team_sub.add_parser("delete", help="Delete team")
    team_del.add_argument("--team-id", required=True, help="Team ID")
    
    # Test
    test_parser = subparsers.add_parser("test", help="Test model")
    test_parser.add_argument("--model", default="qwen3.5-plus", help="Model name")
    test_parser.add_argument("--key", help="API key (optional)")
    
    # Config
    config_parser = subparsers.add_parser("config", help="Generate config")
    config_sub = config_parser.add_subparsers(dest="config_command")
    
    config_openai = config_sub.add_parser("openai", help="OpenAI config")
    config_openai.add_argument("--output", default="~/litellm_config.json", help="Output path")
    
    # Service
    subparsers.add_parser("restart", help="Restart service")
    
    logs_parser = subparsers.add_parser("logs", help="Get logs")
    logs_parser.add_argument("--lines", type=int, default=50, help="Lines")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute
    try:
        if args.command == "status":
            cmd_status()
        elif args.command == "key":
            if args.key_command == "list":
                cmd_key_list()
            elif args.key_command == "generate":
                cmd_key_generate(args)
            elif args.key_command == "delete":
                cmd_key_delete(args)
            elif args.key_command == "info":
                cmd_key_info(args)
            elif args.key_command == "regenerate":
                cmd_key_regenerate(args)
        elif args.command == "user":
            if args.user_command == "list":
                cmd_user_list()
            elif args.user_command == "new":
                cmd_user_new(args)
            elif args.user_command == "delete":
                cmd_user_delete(args)
        elif args.command == "team":
            if args.team_command == "list":
                cmd_team_list()
            elif args.team_command == "new":
                cmd_team_new(args)
            elif args.team_command == "delete":
                cmd_team_delete(args)
        elif args.command == "test":
            cmd_test(args)
        elif args.command == "config":
            if args.config_command == "openai":
                cmd_config_openai(args)
        elif args.command == "restart":
            cmd_restart()
        elif args.command == "logs":
            cmd_logs(args)
    except Exception as e:
        print_status(False, f"Error: {e}")


if __name__ == "__main__":
    main()
