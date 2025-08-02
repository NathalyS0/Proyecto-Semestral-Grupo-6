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