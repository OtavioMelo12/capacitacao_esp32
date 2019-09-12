# Capacitação de ESP32
Capacitação básica para esp32 utilizando [MicroPython](https://micropython.org).

## Tabela de Coteúdo

- [Configurando Esp32](#Configurando-o-esp32-em-seu-computador)
	 - [Instalação Toolchain](#1.Instalação-da-toolchain)
	 - [Instalação ESP-IDF](#2.Instalação-da-API-ESP_IDF)
	 - [Hello World](#3.Rodando-exemplo-Hello-World)
	 - [Instalação MicroPython](#4.Instalando-o-Micropython)
- [Controlando Esp32](#Controlando-o-esp32)
	 - [Instalação rshell](#Instalação)
	 - [Principais Comandos](#Principais-comandos)
- [Links](#Links-úteis)

## Preparação de Ambiente

*Caso o esp32 já esteja com o micropython instalado e configurado em seu sistema, pule pare essa [etapa](#Controlando o esp32). Se não, siga o passo a passso abaixo.*

## Configurando o esp32 em seu computador

### Utilizando Linux:

### 1.Instalação da toolchain
1.1. No seu terminal, navegue`$ cd`até a pasta raiz do seu linux, liste`$ ls -a`os arquivos ocultos desse diretório e localize um chamado `~/.bashrc`.

1.2. Edite o arquivo acima adicionando o seguinte trecho no final

    export PATH=$PATH:$HOME/esp/xtensa-esp32-elf/bin
    alias get_esp32="export PATH=$PATH:$HOME/esp/xtensa-esp32-elf/bin"
    export IDF_PATH=~/esp/esp-idf

1.3. Instale as dependências 

`sudo apt-get install git wget make libncurses-dev flex bison gperf python python-serial`

1.4. Baixe a toolchain, siga esse passo a passo em seu terminal
```bash
mkdir ~/esp && cd ~/esp
wget -c https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-61-gab8375a-5.2.0.tar.gz
tar zxvf xtensa-esp32-elf-linux64-1.22.0-61-gab8375a-5.2.0.tar.gz
```

### 2.Instalação da API ESP-IDF
Baixe a API. O `--recursive` garantirá que os submódulos do repositório, que são essenciais para compilação, também sejam baixados

    git clone --recursive https://github.com/espressif/esp-idf.git

### 3.Rodando exemplo Hello World
3.1. Copie o exemplo Hello World para a pasta `~/esp`
```bash
cp -r ~/esp/esp-idf/examples/get-started/hello_world/ .
```

3.2. **Antes de executar o make , tenha certeza de que possui as permissões necessárias no diretório `~/esp-idf`**
```bash
sudo chmod -R 777 ~/.esp/esp-idf/
```

3.3. Entre na pasta e execute o menu de configurações
```bash
cd hello_world && make menuconfig
```

3.4. Conecte o ESP no seu computador e descubra a porta em que ele está conectado. No linux, geralmente é a porta ´USB0´

3.5. Feito isso, suba o firmware configurado anteriormente para o ESP
```bash
make flash ESPPORT=/dev/ttyUSB0
```

3.6. Você pode conferir a saída do esp32
```bash
make monitor ESPPORT=/dev/ttyUSB0
```

Tudo certo até aqui? Prossiga para a instalação do micropython

### 4.Instalando o Micropython
4.1. Tenha certeza de que você está no diretório esp-idf/ e baixe o micropython
```bash
git clone https://github.com/pfalcon/micropython
```

Insira o seguinte alias em seu `~/.bashrc`
```bash
    alias xtensa-esp32-elf-gcc="xtensa-esp32-elf"
```

#### Compilando port do esp32
4.2. Entre no diretório baixado e compile o mpy-cross
```bash
make -C mpy-cross
```

4.3. Entre em `ports/esp32` e abra o `Makefile`
```bash
cd ports/esp32 && vim Makefile
```

4.4. Abaixo da linha **("# paths to ESP IDF and its components")** inclua
```bash
ESPIDF ?= $(HOME)/esp/esp-idf
```

4.5. Ainda no arquivo `Makefile` copie a hash armazenada em `ESPIDF_SUPHASH`


4.6. Volte ao diretório `esp-idf` e altere para o commit compatível com o `ESPIDF` baixado
```bash
git checkout <hash_copiado_no_passo_anterior>
```

4.7. Entre no diretório `micropython-esp32` e atualize os submódulos
```bash
git submodule update --init
```

4.8. Entre novamente no `ports/esp32` e execute
```bash
make clean 
make
```

4.9. Caso a compilação falhe, volte no diretório `esp-idf` e atualize os submódulos
```bash
git submodule update --init --force
```

4.10. Ainda no diretório `ports/esp32`, apague o conteúdo da flash do `esp32` e suba o firmware
```bash
make erase && make deploy
```

### Utilizando WSL (Windows Subsystem for Linux) no Windows 10:
Primeiramente siga esse [tutorial](https://docs.microsoft.com/pt-br/windows/wsl/install-win10) para instalar o WSL no seu computador.

Provavelmente o WSL virá sem nada, então é necessário instalar algumas dependencias básicas
```bash
sudo apt-get install python python3 vim
```

Em seguida, siga exatamente a mesma configuração anterior, exceto pelos passos **3.5** e **3.6**, em que será necessário olhar em qual porta o esp32 esta conectado.

#### Descobrindo a porta em que o ESP esta conectado

No **Gerenciador de Dispositivos** do Windows, procure por *Portas (COM e LPT)* e verifique a numeração. 
Ex.: (COM 3). Então a porta será `ttyS3`, localizada em `/dev/ttyS3`.

## Controlando o esp32
Para manipular os arquivos entre o esp32 e o computador, podemos utilizar o `rshell`, com ele é possível enviar arquivos do PC para o microcontrolador e vice-versa, assim como deletar, e listar.
Com esse shell é possível também acessar o terminal interno do esp32 e controlar o mesmo diretamente por aí.

#### Instalação

1.1. O rshell precisa de Python3, e do pip3 para ser instalado. Caso não tenha:

```bash
sudo apt-get install python3-pip
```

1.2. Agora com o pip3 já instalado, rode esse comando para instalar o `rshell`

```bash
sudo pip3 install rshell
```
#### Principais comandos

##### Conectando o esp32
Antes talvez seja necessário dar permissão para ter acesso à porta em que o esp32 esta conectado
```bash
sudo chmod 777 /dev/{nome_da_porta}
```
Primeiramente entre no rshell digitando `rshell` no terminal. 

Em seguida conecte o esp:

No WSL:
```bash
connect serial /dev/ttyS{numero_da_porta_COM}
```
No Linux:
```bash
connect serial /dev/ttyUSB0
```
##### Listando os diretórios e arquivos que estão no esp32

```bash
ls /pyboard
```

##### Copiando arquivos que estão no seu PC para o esp32 e vice-versa

```bash
cp {caminho_do_arquivo} /pyboard
```
```bash
cp /pyboard/{caminho_do_arquivo} /{caminho_desejado_no_PC}
```

##### Removendo arquivos que estão no esp32

```bash
rm /pyboard/{caminho_do_arquivo}
```

##### Entrando no terminal interno do esp32

```bash
repl
```
Com isso é possível controlar e programar o esp32 linha por linha utilizando micropython diretamente por esse terminal.

EX: 
```bash
>> from machine import Pin
>> led = Pin(2, Pin.OUT)
>> led.on()
```
#### Links úteis
- [Guia de programação do ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/) (Espressif IoT development framework)
- [Getting started do ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/get-started/)
- [Toolchain no Linux](https://docs.espressif.com/projects/esp-idf/en/latest/get-started/linux-setup.html)
- [Getting started Micropython com ESP32](http://docs.micropython.org/en/latest/esp32/tutorial/intro.html#esp32-intro)
- [Bibliotecas para MicroPython](https://github.com/micropython/micropython-lib)