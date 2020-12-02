# Getting Started

# Usage
## How to run the proxy
The proxy was designed to run on Linux system and to proxy for an application running on a windows system.
The proxy must be started with the information of the target server.

## Route traffic from Windows 10 to the linux system instead to your main router
The windows system must be configured to route the traffic to the linux system with the proxy running.  
The following command must be run as administrator.
```
ROUTE ADD "server ip" MASK 255.255.255.255 "proxy ip"
```
server ip = the ip of the server your windows application connects to  
proxy ip = the ip of the system, which runs the proxy

Now every packets to the server will be routed through the linux system instead of being routed to your main router.

## Pass routing traffic to proxy on Linux system
The windows system uses the linux system now as the router for packets, which should go to the server. We can use iptables to intercept this routing and send the packets instead to the linux system itself.

```
iptables-legacy -t nat -A PREROUTING -p tcp -j REDIRECT --to-ports 30000
```
-t nat specifies the nat table as target  
-A PREROUTING appends a rule to the prerouting entries  
-p tcp do this only for tcp packets  
-j REDIRECT --to ports 30000 redirect all packets to be routed to the machine itself  

# Examples
## WSL2
### Prequesites
1. Windows Pro or higher (Hyper-V Manager must be accessible) https://stackoverflow.com/a/62438375
2. Kali Linux in WSL 2

# Troubleshooting
Check iptables rules https://www.cyberciti.biz/faq/linux-iptables-delete-prerouting-rule-command/