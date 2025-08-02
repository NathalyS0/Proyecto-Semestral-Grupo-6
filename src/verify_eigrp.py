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