
![Logo](https://i.imgur.com/CvGN2TF.png)



## Desafios

1 - Completar o código de uma lista encadeada parcialmente implementada

2 - Fazer webscrapping do site AISWEB para colher informações de cartas disponíveis, os horários de nascer e pôr do sol de hoje e a informação de TAF e METAR disponíveis de um determinado aeródromo
## Como rodar os desafios em minha máquina?


- Clone o repositório
    ```bash
      git pull https://github.com/MarceloJDCB/qipu-challenge.git
    
      cd qipu-challenge
    ```

- Rode os comandos (Usando ubuntu ou wsl):
    ```
    make init
    ```
- Caso deseje rodar o primeiro desafio:
    ```
    make lista_encadeada
    ```
- Caso queira rodar o segundo desafio:
    ```
    make aisweb
    ```
## Comandos Make

- Rebuildar os containers sem cache
    ```
    _rebuild
    ```

- Rebuildar os containers com cache
    ```
    rebuild
    ```

- Iniciar os containers
    ```
    up
    ```

- Rodar o desafio 1
    ```
    lista_encadeada
    ```

- Rodar o desafio 2
    ```
    aisweb
    ```

- Buildar os containers
    ```
    build
    ```

- Lista logs
    ```
    logs
    ```

- Remove containers
    ```
    down
    ```

- Para todos os containers
    ```
    stopall
    ```

- Inicia um .env
    ```
    _cp_env_file
    ```