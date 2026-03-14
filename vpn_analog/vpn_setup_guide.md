# WireGuard VPN 部署指南

## 服务器信息
- **IP**: `<your_server_ip>`
- **系统**: Ubuntu 22.04 LTS
- **公钥**: `<server_public_key>`

---

## 部署步骤

### 1. 安装依赖

```bash
apt update
apt install -y wireguard wireguard-tools qrencode iptables-persistent
```

### 2. 开启IP转发

```bash
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

### 3. 创建WireGuard配置

```bash
cd /etc/wireguard
umask 077

# 生成服务器密钥
wg genkey | tee privatekey | wg pubkey > publickey

SERVER_PRIV=$(cat privatekey)
SERVER_PUB=$(cat publickey)
SERVER_IP="39.102.85.50"

# 创建服务器配置
cat > wg0.conf << EOF
[Interface]
PrivateKey = $SERVER_PRIV
Address = 10.254.0.1/16
ListenPort = 51820

# SNAT所有出站流量，源IP变成阿里云IP
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -s 10.254.0.0/16 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -s 10.254.0.0/16 -j MASQUERADE
EOF

chmod 600 wg0.conf
```

### 4. 启动WireGuard

```bash
wg-quick up wg0
systemctl enable wg-quick@wg0

# 防火墙放行
iptables -I INPUT -p udp --dport 51820 -j ACCEPT
iptables -I INPUT -p tcp --dport 51820 -j ACCEPT

# 保存防火墙规则
netfilter-persistent save
```

### 5. 查看服务器状态

```bash
wg show
```

---

## 添加外包人员

### 方法1: 手动添加

```bash
cd /etc/wireguard
mkdir -p clients

# 配置变量
NAME="vendor_name"
IP="10.254.1.10"

# 生成客户端密钥
wg genkey | tee clients/${NAME}_priv | wg pubkey > clients/${NAME}_pub
PRIV=$(cat clients/${NAME}_priv)
PUB=$(cat clients/${NAME}_pub)
SERVER_PUB=$(cat publickey)

# 添加到服务器配置
cat >> wg0.conf << EOF

# $NAME
[Peer]
PublicKey = $PUB
AllowedIPs = $IP/32
EOF

# 生成客户端配置
cat > clients/${NAME}.conf << EOF
[Interface]
PrivateKey = $PRIV
Address = $IP/16
DNS = 223.5.5.5, 114.114.114.114

[Peer]
PublicKey = $SERVER_PUB
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <your_server_ip>:51820
PersistentKeepalive = 25
EOF

# 重载配置
wg syncconf wg0 <(wg-quick strip wg0)

# 显示配置和二维码
cat clients/${NAME}.conf
qrencode -t ansiutf8 < clients/${NAME}.conf
```

### 方法2: 使用交互式脚本

```bash
#!/bin/bash
# /etc/wireguard/add-peer.sh

cd /etc/wireguard
read -p "外包人员姓名: " name
read -p "分配IP (如 10.254.1.10): " ip

wg genkey | tee "clients/${name}_priv" | wg pubkey > "clients/${name}_pub"
PRIV=$(cat "clients/${name}_priv")
PUB=$(cat "clients/${name}_pub")
SERVER_PUB=$(cat publickey)

cat >> wg0.conf << EOF

# $name
[Peer]
PublicKey = $PUB
AllowedIPs = $ip/32
EOF

cat > "clients/${name}.conf" << EOF
[Interface]
PrivateKey = $PRIV
Address = $ip/16
DNS = 223.5.5.5, 114.114.114.114

[Peer]
PublicKey = $SERVER_PUB
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <your_server_ip>:51820
PersistentKeepalive = 25
EOF

wg syncconf wg0 <(wg-quick strip wg0)

echo "=== $name 配置文件 ==="
cat "clients/${name}.conf"
echo ""
echo "=== 二维码 ==="
qrencode -t ansiutf8 < "clients/${name}.conf"
```

---

## 下载客户端配置到本地

```bash
scp -i ~/.ssh/id_rsa root@<your_server_ip>:/etc/wireguard/clients/<vendor_name>.conf ./
```

---

## 外包人员使用指南

### 1. 安装WireGuard客户端

- **Windows**: https://download.wireguard.com/windows-client/wireguard-installer.exe
- **Mac**: App Store搜索 "WireGuard"
- **iOS**: App Store搜索 "WireGuard"
- **Android**: Google Play搜索 "WireGuard"

### 2. 导入配置

**方式1**: 文件导入
- 将 `.conf` 文件发送给外包人员
- WireGuard客户端 → 导入隧道 → 从文件

**方式2**: 二维码导入
- 在服务器上生成二维码：`qrencode -t ansiutf8 < clients/vendor1.conf`
- 手机WireGuard APP扫描二维码

### 3. 连接VPN
- 点击连接按钮
- 状态变绿即连接成功

---

## 防火墙配置

### 服务器端防火墙
```bash
# 已配置iptables规则
iptables -I INPUT -p udp --dport 51820 -j ACCEPT
iptables -I INPUT -p tcp --dport 51820 -j ACCEPT

# 保存规则
netfilter-persistent save
```

### 阿里云安全组（重要！）

必须在阿里云控制台配置安全组：

1. 登录阿里云控制台 → ECS → 实例详情 → 安全组
2. 入方向规则 → 添加规则：
   - 协议类型: **UDP**
   - 端口范围: **51820/51820**
   - 授权对象: **0.0.0.0/0**

---

## 验证连接

### 服务器端查看连接状态
```bash
wg show
```

### 客户端验证
在Windows CMD执行：
```cmd
tracert 117.133.41.170
```

预期结果：
```
1    <1ms  10.254.0.1       <- 阿里云VPN网关
2     2ms  11.x.x.x         <- 阿里云内网
3     5ms  39.156.x.x       <- 移动骨干
4     7ms  117.133.41.170   <- 至安盾
```

---

## 常用命令

```bash
# 重启WireGuard
wg-quick down wg0 && wg-quick up wg0

# 查看连接状态
wg show

# 查看监听端口
ss -ulnp | grep 51820

# 删除客户端
# 编辑 /etc/wireguard/wg0.conf，删除对应[Peer]段，然后重载
wg syncconf wg0 <(wg-quick strip wg0)

# 停止WireGuard
wg-quick down wg0
```

---

## 客户端IP分配表

| 外包人员 | 分配IP | 公钥 |
|---------|--------|------|
| (示例) vendor_name | 10.254.1.x | `<vendor_public_key>` |

---

## 架构图

```
外包人员 (全球任意地点)
    ↓ WireGuard VPN
阿里云北京 (<your_server_ip>)
    ↓ SNAT转发
目标服务 <target_service_ip> (阿里云IP白名单)
    ↓
公司内网
```
