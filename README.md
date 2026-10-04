# Estação Meteorológica IoT (Meteoro Station)

Sistema embebido de monitorização meteorológica desenvolvido em \*\*MicroPython\*\* para o microcontrolador \*\*ESP32\*\*, com arquitetura assíncrona, persistência em buffer circular (RAM) e ficheiros físicos (CSV), além de uma interface web leve servida através do framework \*\*Microdot\*\*.

---

## Estrutura do Projeto

meteoro\_station/

├── src/

│   ├── core/              # Módulos centrais (aquisição, buffer, máquina de estados, CSV)

│   ├── sensors/           # Sensores virtuais e reais (BME280, MQ-135)

│   ├── web/               # Servidor Microdot e interface estática (HTML/CSS/JS)

│   ├── boot.py            # Script de inicialização (Modo AP/Rede)

│   └── main.py            # Ponto de entrada e orquestrador assíncrono

├── tests/

│   ├── acceptance/        # Testes de aceitação (Endpoints e rotas HTTP)

│   ├── integration/       # Testes de integração (Aquisição e armazenamento)

│   └── unit/              # Testes unitários (Buffer, avaliadores, sensores)

├── venv/                  # Ambiente virtual Python

└── README.md

---

## Guia de Instalação e Execução

Siga os passos abaixo para configurar o ambiente de desenvolvimento, instalar as dependências, executar os testes e iniciar o projeto.

### Criar e Ativar o Ambiente Virtual (venv)

Abra o terminal na raiz do projeto e crie o ambiente virtual:

Bash

python -m venv venv

### Ative o ambiente virtual conforme o seu sistema operativo:

Windows (PowerShell):

PowerShell

.\venv\Scripts\Activate.ps1

Windows (CMD):

DOS

venv\Scripts\activate.bat

Linux / macOS:

Bash

source venv/bin/activate

### Instalar as Dependências

Com o ambiente virtual ativo, instale as bibliotecas necessárias para o funcionamento do servidor e da suite de testes:

Bash

pip install microdot pytest pytest-asyncio

pip install -r requirements.txt

### Executar os Testes Automatizados

O projeto possui uma suite completa de testes unitários, de integração e de aceitação gerida pelo pytest. Para validar todos os módulos, execute:

Bash

python -m pytest

### Executar o Projeto

O sistema opera nativamente na porta 80 para o ambiente final no ESP32. Para iniciar o servidor e simular a recolha de dados dos sensores:

Bash

python -m src.main

Após iniciar o servidor, aceda através do seu navegador:

Painel Web: http://localhost (ou o IP correspondente no ESP32)

Exportação CSV: http://localhost/api/exportar.csv

Para interromper a execução do servidor no terminal, prima Ctrl + C.
