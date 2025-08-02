# Proyecto 3: Configuración de EIGRP con Python + NETCONF

## Objetivo
Configurar el protocolo EIGRP para IPv4 en un router Catalyst 8000v (R1) mediante un script Python usando NETCONF. Los routers R2 y R3 (vIOS) estarán preconfigurados para formar vecindad con R1 cuando este sea configurado.

---

## Topología GNS3
```
[NAT1] --- [AlpineReal] --- [CiscoC8000v] --- [R2]
                                      \
                                       \--- [R3]
```

---

## Configuración de los routers

### R2
```bash
conf t
hostname R2
interface GigabitEthernet0/0
 ip address 192.168.12.2 255.255.255.0
 no shutdown
!
router eigrp 100
 network 192.168.12.0 0.0.0.255
 no auto-summary
end
write memory
```

### R3
```bash
conf t
hostname R3
interface GigabitEthernet0/0
 ip address 192.168.13.2 255.255.255.0
 no shutdown
!
router eigrp 100
 network 192.168.13.0 0.0.0.255
 no auto-summary
end
write memory
```

### R1 (Catalyst 8000v)
Activar Netconf en R1
```bash
conf t
hostname R1
ip domain-name localdomain
crypto key generate rsa modulus 2048
ip ssh version 2
username cisco privilege 15 secret cisco
netconf-yang
end
write memory

```


Interfaces previas al script:
- Gi0/1: 192.168.100.1 (conectado a Alpine)
- Gi0/2: 192.168.12.1 (a R2)
- Gi0/3: 192.168.13.1 (a R3)

Verifica que las interfaces estén activas:
```bash
conf t
interface GigabitEthernet1
 ip address 192.168.100.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet2
 ip address 192.168.12.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet3
 ip address 192.168.13.1 255.255.255.0
 no shutdown
end

```

---

## Configurar Alpine
```bash
#Interfaz a R1
ip link set eth0 up
ip addr add 192.168.100.2/24 dev eth0

#Configurar NAT en eth3
ip link set eth3 up
udhcpc -i eth3


#Configurar venv (virtual environment) para ejecutar python
mkdir -p /tmp/venv
python3 -m venv /tmp/venv
source /tmp/venv/bin/activate

#Instalar librerias (requiere internet)
apk add python3 py3-pip
pip install --no-cache-dir ncclient
```
---

## Script Python ejecutado desde Alpine

Nombre: `eigrp_netconf.py`
```python
from ncclient import manager
from lxml import etree

router = {
    "host": "192.168.100.1",
    "port": 830,
    "username": "cisco",
    "password": "cisco",
}

config_xml = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <router>
      <router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp">
        <eigrp>
          <named-mode>
            <name>MY-EIGRP</name>
            <address-family>
              <ipv4>
                <af-ipv4>
                  <unicast>unicast</unicast>
                  <autonomous-system>100</autonomous-system>
                  <eigrp>
                    <router-id>1.1.1.1</router-id>
                  </eigrp>
                  <network>
                    <address-wildcard>
                      <ipv4-address>192.168.12.0</ipv4-address>
                      <wildcard>0.0.0.255</wildcard>
                    </address-wildcard>
                    <address-wildcard>
                      <ipv4-address>192.168.13.0</ipv4-address>
                      <wildcard>0.0.0.255</wildcard>
                    </address-wildcard>
                  </network>
                  <topology>
                    <topo-base>
                      <topology-base>base</topology-base>
                    </topo-base>
                  </topology>
                </af-ipv4>
              </ipv4>
            </address-family>
          </named-mode>
        </eigrp>
      </router-eigrp>
    </router>
  </native>
</config>
"""

with manager.connect(
    host=router["host"],
    port=router["port"],
    username=router["username"],
    password=router["password"],
    hostkey_verify=False,
    look_for_keys=False,
    allow_agent=False
) as m:
    print("Conectado al router. Enviando configuración EIGRP...")
    response = m.edit_config(target="running", config=config_xml)
    print("Respuesta:\n", response)
```

---

## Comandos para verificar funcionamiento
En R1 (Catalyst):
```bash
show ip eigrp neighbors
show ip protocols
show running-config | section eigrp
```

En R2 y R3:
```bash
show ip eigrp neighbors
```

---

## Eliminar la configuración EIGRP en R1
```bash
conf t
no router eigrp MY-EIGRP
interface GigabitEthernet2
 shutdown
 no ip address
interface GigabitEthernet3
 shutdown
 no ip address
end
write memory
```

---

## Verificación NETCONF (get-config)
Puedes agregar el siguiente script en Python para verificar la configuración EIGRP:
```python
from ncclient import manager
from lxml import etree

with manager.connect(
    host="192.168.100.1",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False,
    look_for_keys=False,
    allow_agent=False
) as m:
    print("Conectado. Obteniendo configuración EIGRP...")

    filter_xml = etree.fromstring('''
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp"/>
        </router>
      </native>
    </filter>
    ''')

    response = m.get_config(source='running', filter=filter_xml)
    print(response.xml)
```

Respuesta esperada
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply
	xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:91396e95-595f-42a5-b586-4e85950ee6bf"
	xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
	<data>
		<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
			<router>
				<router-eigrp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp">
					<eigrp>
						<named-mode>
							<name>MY-EIGRP</name>
							<address-family>
								<ipv4>
									<af-ipv4>
										<unicast>unicast</unicast>
										<autonomous-system>100</autonomous-system>
										<eigrp>
											<router-id>1.1.1.1</router-id>
										</eigrp>
										<network>
											<address-wildcard>
												<ipv4-address>192.168.12.0</ipv4-address>
												<wildcard>0.0.0.255
												</wildcard>
											</address-wildcard>
											<address-wildcard>
												<ipv4-address>192.168.13.0</ipv4-address>
												<wildcard>0.0.0.255</wildcard>
											</address-wildcard>
										</network>
										<topology>
											<topo-base>
												<topology-base>base
												</topology-base>
											</topo-base>
										</topology>
									</af-ipv4>
								</ipv4>
							</address-family>
						</named-mode>
					</eigrp>
				</router-eigrp>
			</router>
		</native>
	</data>
</rpc-reply>
```

---

## Resultado esperado
- El script se conecta al router Catalyst desde Alpine.
- Se configura EIGRP named-mode en el AS 100 con ambas redes.
- R2 y R3 forman vecindad EIGRP con R1.
- Se valida conectividad y rutas aprendidas.
- Se realiza verificación mediante operación `get-config`.
- Se incluye impresión de logs y respuesta del servidor NETCONF.

