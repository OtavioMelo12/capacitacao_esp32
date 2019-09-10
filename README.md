# Capacitação de ESP32
Capacitação básica para esp32 utilizando [MicroPython](https://micropython.org).
## Preparação de Ambiente

### Utilizando Linux:


### Utilizando WSL (Windows Subsystem for Linux) no Windows 10:
Primeiramente siga esse [tutorial](https://docs.microsoft.com/pt-br/windows/wsl/install-win10) para instalar o WSL no seu computador.
#### 1. Instalação da toolchain
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

#### 2. Instalação da API ESP-IDF
Baixe a API. O `--recursive` garantirá que os submódulos do repositório, que são essenciais para compilação, também sejam baixados

    git clone --recursive https://github.com/espressif/esp-idf.git

#### 3. Rodando exemplo Hello World
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

3.4. Conecte o ESP no seu computador e descubra a porta COM em que ele esta conectado

##### Descobrindo a porta em que o ESP esta conectado

No **Gerenciador de Dispositivos** do Windows, procure por *Portas (COM e LPT)* e verifique a numeração. 
Ex.: (COM 3), 3 é o número da porta COM

3.5. Feito isso, suba o firmware configurado anteriormente para o ESP
```bash
make flash ESPPORT=/dev/ttyS{número_da_porta_COM}
```

3.6. Você pode conferir a saída do esp32
```bash
make monitor ESPPORT=/dev/tty{nome_da_porta_com}
```

Tudo certo até aqui? Prossiga para a instalação do micropython

#### 4. Instalando o Micropython
4.1. Tenha certeza de que você está no diretório esp-idf/ e baixe o micropython
```bash
git clone https://github.com/pfalcon/micropython
```

##### Compilando port do esp32
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