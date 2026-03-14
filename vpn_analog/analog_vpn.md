# 阿里云跳板机 VPN 方案

## 架构概述

```
外包人员 (全球任意地点)
    ↓ WireGuard VPN
阿里云北京 BGP (<your_server_ip>)
    ↓ 直接访问
目标服务 <target_service_ip> (看到阿里云IP自动放行)
    ↓
公司内网
```

**关键点**：至安盾配置了阿里云IP白名单，阿里云BGP出口到移动内网质量最优。

---

## 1. 阿里云配置（一键脚本）

```bash
#!/bin/bash
# 阿里云VPN跳板机 - 北京BGP推荐机型：ecs.g7ne.large 或更高

# 基础配置
apt update && apt install -y wireguard wireguard-tools qrencode

# 开启IP转发
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# 生成服务器密钥
cd /etc/wireguard
umask 077
wg genkey | tee privatekey | wg pubkey > publickey

SERVER_PRIV=$(cat privatekey)
SERVER_PUB=$(cat publickey)
SERVER_IP=$(curl -s ifconfig.me)

# 创建配置 - 关键点：PostUp/PostDown 做SNAT，让目标服务只看到阿里云IP
cat > wg0.conf << EOF
[Interface]
PrivateKey = $SERVER_PRIV
Address = 10.254.0.1/16
ListenPort = 51820

# SNAT所有出站流量，源IP变成阿里云内网IP（目标服务白名单生效）
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -s 10.254.0.0/16 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -s 10.254.0.0/16 -j MASQUERADE

# 预留外包人员槽位，按需添加
EOF

chmod 600 wg0.conf

# 启动
wg-quick up wg0
systemctl enable wg-quick@wg0

# 防火墙放行
iptables -I INPUT -p udp --dport 51820 -j ACCEPT
iptables -I INPUT -p tcp --dport 51820 -j ACCEPT

echo "=== 阿里云公钥（给外包人员）==="
echo "$SERVER_PUB"
echo ""
echo "=== 阿里云公网IP ==="
echo "$SERVER_IP"
```

---

## 2. 添加外包人员（交互式）

```bash
#!/bin/bash
# add-peer.sh

cd /etc/wireguard
read -p "外包人员姓名: " name
read -p "分配IP (如 10.254.1.10): " ip

# 生成密钥
wg genkey | tee "clients/${name}_priv" | wg pubkey > "clients/${name}_pub"
PRIV=$(cat "clients/${name}_priv")
PUB=$(cat "clients/${name}_pub")
SERVER_PUB=$(cat publickey)
SERVER_IP=$(curl -s ifconfig.me)  # 你的阿里云服务器IP

# 添加到服务器
cat >> wg0.conf << EOF

# $name
[Peer]
PublicKey = $PUB
AllowedIPs = $ip/32
EOF

# 生成客户端配置
mkdir -p /etc/wireguard/clients
cat > "clients/${name}.conf" << EOF
[Interface]
PrivateKey = $PRIV
Address = $ip/16
DNS = 223.5.5.5, 114.114.114.114

[Peer]
PublicKey = $SERVER_PUB
AllowedIPs = 0.0.0.0/0, ::/0  # 全流量走VPN（享受阿里云BGP）
Endpoint = \$SERVER_IP:51820
PersistentKeepalive = 25
EOF

# 重载配置
wg syncconf wg0 <(wg-quick strip wg0)

echo "=== $name 配置文件 ==="
cat "clients/${name}.conf"
echo ""
echo "=== 二维码（手机扫描）==="
qrencode -t ansiutf8 < "clients/${name}.conf"

echo ""
echo "文件已保存至: /etc/wireguard/clients/${name}.conf"
```

---

## 3. 外包人员 Windows 配置

### 方式一：WireGuard 官方客户端（推荐）

1. 下载安装：https://download.wireguard.com/windows-client/wireguard-installer.exe
2. 新建隧道 → 粘贴配置：

```ini
[Interface]
PrivateKey = <your_private_key>
Address = 10.254.1.10/16
DNS = 223.5.5.5

[Peer]
PublicKey = <server_public_key>
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <your_server_ip>:51820  # 阿里云北京BGP IP
PersistentKeepalive = 25
```

3. 点击连接，状态栏显示绿色即成功

### 方式二：TunSafe（第三方GUI，对小白更友好）

界面更直观，配置格式相同。

---

## 4. 关键验证

外包连接后，验证流量路径：

```bash
# 外包人员Windows CMD执行
tracert 117.133.41.170

# 应该看到：
# 1    <1ms  10.254.0.1       <- VPN网关
# 2     2ms  <aliyun_internal_ip>  <- 阿里云内网
# 3     5ms  <backbone_ip>    <- 移动骨干
# 4     7ms  <target_service_ip>  <- 目标服务（阿里云BGP优化路由）
```

对比之前直接连的卡顿路径：
```
# 原来外包直连（假设外包在电信）
# 1    50ms  电信省出口
# 2   200ms  电信-移动互联互通瓶颈 <- 卡顿点！
# 3   250ms  移动骨干
# 4   260ms  <target_service_ip>
```

---

## 5. 阿里云选型建议

| 场景 | 推荐配置 | 月成本 |
|------|---------|--------|
| 5人以下轻量使用 | 轻量应用服务器 2C2G 北京 | ~60元 |
| 10人常规办公 | ECS共享标准型 s6 2C4G 北京 | ~150元 |
| 20人+或大量传输 | ECS计算型 c7 4C8G 北京 + 固定带宽 | ~300元+ |

**关键：必须选「北京」节点**，物理距离至安盾最近，移动内网一跳直达。

---

## 6. 目标服务侧确认

请确认目标服务管理员已配置：
- **源IP白名单**：阿里云北京网段（如 `47.52.0.0/16`, `47.88.0.0/16`, `47.95.0.0/16`, `8.130.0.0/16` 等）
- 或更精确：你购买的阿里云ECS具体IP

如果不确定白名单范围，可以先买阿里云按量付费ECS测试，确认连通后再转包年包月。
