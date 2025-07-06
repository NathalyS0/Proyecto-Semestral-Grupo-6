# Proyecto: Automatización de Configuración EIGRP con NETCONF

## 🎯 Objetivo Específico

Desarrollar un script en Python que aplique configuraciones de EIGRP para IPv4 utilizando el protocolo NETCONF y valide los resultados en dispositivos Cisco IOS XE.

---

## 🛠️ Tecnologías y Herramientas Utilizadas

| Tecnología       | Descripción                                                                 |
|------------------|------------------------------------------------------------------------------|
| **Python**       | Lenguaje principal para el desarrollo del script                            |
| **ncclient**     | Biblioteca para gestionar conexiones NETCONF                                |
| **PyYAML**       | Biblioteca para leer archivos YAML de inventario                            |
| **logging**      | Registro de eventos y errores del script                                    |
| **NETCONF**      | Protocolo de configuración de red basado en XML                             |
| **Cisco IOS XE** | Sistema operativo de red compatible con NETCONF/YANG                        |
| **Modelos YANG** | Uso del modelo `Cisco-IOS-XE-eigrp` para configuración de EIGRP             |
| **YAML**         | Formato utilizado para definir el inventario de dispositivos                |
| **Git/GitHub**   | Control de versiones y colaboración en el desarrollo                        |

🔗 Repositorio del proyecto: [Proyecto-Semestral-Grupo-6](https://github.com/NathalyS0/Proyecto-Semestral-Grupo-6.git)

---

## ⚙️ Instrucciones de Ejecución

### 1. Preparación del Entorno

```bash
# Instalar Python (versión 3.8 o superior)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
