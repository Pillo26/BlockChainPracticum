

---

# 📁 Cadena de Evidencia Digital con Blockchain - Proyecto Judicial

Sistema de gestión y trazabilidad de evidencia digital para procesos judiciales, basado en una **blockchain privada**. El proyecto asegura la **cadena de custodia**, reduce el riesgo de manipulaciones y fortalece la **admisión legal de pruebas digitales**.

## 🧩 Características principales

* **Blockchain privada** con control de acceso basado en roles.
* Modelo de **multifirma M-de-N** para validación de bloques.
* Algoritmos criptográficos robustos:

  * **SHA-256** para hashing de archivos y bloques.
  * **ECDSA** para firmas digitales.
* Implementación de **árboles de Merkle** para integridad de evidencias.
* **Consenso Proof of Authority (PoA)**: nodos autorizados validan bloques.
* Simulación de procesos judiciales reales en la trazabilidad de evidencias.

---

## 🔐 Tipo de Blockchain

* Se trata de una **blockchain privada**.
* La aplicación **simula el proceso** mediante el cual fiscalías y juzgados manejan y custodian evidencias digitales.

---

## 📦 Estructura del bloque

Cada bloque contiene los siguientes campos:

* **Entidad**: Fiscalía o Juzgado responsable.
* **Firmante(s)**: Usuarios que firman la evidencia (M-de-N).
* **Validador(es)**: Nodos con autoridad que verifican la validez del bloque.
* **Merkle Root**: Raíz de árbol Merkle generado a partir de las evidencias.
* **Hash del bloque anterior**
* **Timestamp**
* **ID de caso**
* **Firma(s) digitales** con ECDSA
* **Fiscal responsable del caso**

---

## ✍️ Firma Digital y Multifirma

* Las firmas se realizan utilizando el algoritmo **ECDSA**.
* Se emplea un esquema de **multifirma M-de-N**, donde un bloque **solo se mina si se alcanza el umbral mínimo de firmas** requeridas.
* La lógica de validación M-de-N se aplica antes del minado final del bloque.

---

## 🧠 Algoritmos Criptográficos Usados

| Función               | Algoritmo                                |
| --------------------- | ---------------------------------------- |
| Hash de archivos      | SHA-256                                  |
| Hash de bloques       | SHA-256                                  |
| Merkle Root           | SHA-256                                  |
| Firma digital         | ECDSA                                    |
| Validación multifirma | M-de-N lógica                            |
| Consenso de red       | Proof of Authority (PoA) basado en roles |

---

## 🧾 Consenso y Validación

* Se utiliza un consenso **Proof of Authority**, donde solo nodos autorizados (por ejemplo, fiscales o jueces) pueden validar bloques.
* Cada bloque contiene un campo de **ID de caso**, que permite asociar cada bloque con un proceso judicial específico.

---


