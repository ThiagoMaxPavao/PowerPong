# Power Pong

Este repositório contém o projeto final da disciplina Laboratório de Sistemas Embarcados da Unicamp, realizado no segundo semestre de 2024.
O projeto foi originalmente desenvolvido para ser executado em conjunto com a [BitDogLab](https://github.com/BitDogLab/BitDogLab), um projeto educacional do professor Fabiano.

Autores:

- Luciano Cardoso Ferreira Filho
- Thiago Maximo Pavão

Professor: Doutor Fabiano Fruett

## Sobre o Projeto

O projeto consiste na implementação do clássico jogo de fliperama Pong, desenvolvido originalmente pela [Atari](https://pt.wikipedia.org/wiki/Pong), para a plataforma BitDogLab.

![Pong original](https://github.com/user-attachments/assets/ebbd3af1-7076-4723-a534-e733d2d77743)

O jogo original era controlado por dois controles rotacionais mecânicos (um para cada jogador), e o objetivo era simplesmente rebater a bola para o campo adversário.
No entanto, o objetivo deste projeto foi manter os principais elementos do jogo clássico, ao mesmo tempo em que adicionamos novas mecânicas para aprimorar a jogabilidade.

A principal inovação em hardware é a forma como os jogadores interagem com o jogo. Foi desenvolvida uma luva equipada com LEDs, buzzer, e sensores de acelerômetro e giroscópio.
Além disso, a ponta de cada dedo contém uma fita de cobre para detectar toques entre o polegar e os outros quatro dedos. Atualmente, a luva é destinada ao uso exclusivo da mão
direita, então uma melhoria seria torná-la adaptável para ambas as mãos, ampliando sua acessibilidade.

Em relação ao software, também foram feitas modificações para tornar a jogabilidade mais divertida: os jogadores agora podem usar poderes especiais para alterar o curso da partida,
mas devem utilizá-los de forma estratégica, pois cada poder tem um custo. Além disso, a bola acelera levemente cada vez que um jogador a rebate com seu controle,
tornando o jogo progressivamente mais desafiador. Parte da estratégia no uso dos poderes está relacionada a essa velocidade crescente — alguns poderes se tornam muito mais
eficazes quando usados no momento certo.

## Sobre o Jogo

Regras básicas do jogo
Lógica de sets
Lógica de vai a 2
Explicação de início, quando os dois estão prontos (ready)
Inversão dos controles (esquerda/direita), dependendo da disposição dos jogadores
Explicação dos poderes, as cargas
Explicação de cada poder individualmente
Aviso quando os poderes estão cheios, para lembrar de gastar 

## Documentação de Hardware

### Componentes utilizados

Componentes da bitdog e externos que foram utilizados, incluindo a raspberry pi pico

### Tabelas de conexão

Display com a raspberry, luvas com I2C
Inserir ou indicar referência para conexão dos periféricos da bitdoglab

### Esquemático do circuito da luva

Projeto do circuito da luva, com breve explicação sobre os circuitos, por exemplo pull down, conexão com negativo no PCF, pq não fornece corrente suficiente se ligado ao contrário
Falar também da ligação que fizemos no PCF, curtando VCC e VDD para fornecer diretamente a mesma alimentação ligada ao módulo para os dispositivos controlador em suas portas

### Projeto da placa de circuito impresso desenvolvido

Imagem da PCB

### Construção mecânica

Fotos da luva pronta

## Documentação de Software

Biblioteca utilizada
Explicação do firmware gerado

### Maquina de estados

### Lógica do sensor

### Velocidade da bolinha

### Organização dos Arquivos

Os arquivos podem ser encontrados nesta [pasta](/code)

