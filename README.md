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

O software foi desenvolvido em MicroPython, utilizando algumas bibliotecas escritas em Python, que estão inclusas neste repositório.

Além dessas bibliotecas em Python, uma biblioteca escrita em C foi incorporada ao firmware da placa para interagir com o display. Essa abordagem foi necessária devido ao alto volume de dados trocados com o display, que tornava uma solução em Python ineficiente.

A biblioteca utilizada para essa interação foi [st7789_mpy](https://github.com/russhughes/st7789_mpy). Contudo, ao utilizar o firmware disponibilizado no repositório original, encontramos erros que acreditamos serem causados pela incompatibilidade entre a versão do MicroPython usada e aquela com a qual o firmware foi compilado.

Para resolver o problema, geramos um firmware com a última versão estável do MicroPython disponível (v1.24), incluindo a biblioteca necessária. Esse firmware está disponível na raiz do repositório, no arquivo firmware.uf2. O processo de geração foi baseado em uma solução detalhada em uma issue do repositório da biblioteca. Você pode consultar a explicação [aqui](https://github.com/russhughes/st7789_mpy/issues/168#issuecomment-2342353619). O procedimento funcionou corretamente.

### Máquina de Estados

O fluxo do programa é baseado em uma máquina de estados, representada na figura abaixo:

![Máquina de estados do projeto](https://github.com/user-attachments/assets/f45a0cf4-fdf4-40d4-9e5f-160254ea969e)

Cada estado executa as seguintes tarefas:

MENU: Exibe o nome do jogo e as instruções iniciais piscando. O programa aguarda que o botão A seja pressionado para avançar ao próximo estado.

CHOOSE SETS: Mostra na tela as opções de quantidade de sets (melhor de 1, 3 ou 5). O joystick horizontal é usado para alternar entre as opções. Pressionar o botão A confirma a escolha e avança para o próximo estado.

GAME BREAK: Aguarda ambos os jogadores pressionarem seus botões simultaneamente, indicando que estão prontos para começar a partida.

GAME RUNNING: Atualiza a posição dos pads dos jogadores com base nos dados do acelerômetro, verifica o uso do poder de escudo e simula a física da bolinha, incluindo colisões com as paredes e pads.

END: Mostra uma animação, toca a música de vitória e exibe na tela o nome do jogador vencedor.

### Lógica do Sensor

O sensor retorna valores de aceleração em três eixos, mas apenas dois são utilizados para calcular o ângulo de inclinação do dispositivo, como ilustrado abaixo:

![Acelerometro](https://github.com/user-attachments/assets/1dffd47a-2043-4bf4-8d84-0ea321bc047a)

![Formula do angulo](https://github.com/user-attachments/assets/f623fb4a-ab9a-4e30-9579-c2bebb573e21)

Devido a flutuações nas leituras do sensor, aplicamos um filtro digital passa-baixas para suavizar os valores do ângulo. Este filtro também compensa descontinuidades angulares (como a transição de -π para π). Após o processamento, os valores são escalados para representar a posição vertical do pad na tela. Essa conversão associa um intervalo de -45° a 45° aos limites da tela, que vão de PAD_WIDTH//2 até WIDTH - PAD_WIDTH//2, onde WIDTH é a largura da tela e PAD_WIDTH é a largura do pad.

Por fim, garantimos que a posição do pad permaneça dentro dos limites da tela. O processo é ilustrado na figura abaixo:

![Fluxo de dados do sensor](https://github.com/user-attachments/assets/5a8bcb13-34fd-4cb4-85a5-d28a4201f551)

### Velocidade da Bolinha

A velocidade da bolinha aumenta gradualmente a cada rebote, tornando o jogo mais dinâmico. No início de cada round, a velocidade inicial é ajustada com base no desempenho dos jogadores. Após cada round, a bolinha perde 30% de sua velocidade final, equilibrando o ritmo do jogo para que a bola não fique nem muito lenta nem muito rápida.

### Organização dos Arquivos

Os arquivos estão disponíveis nesta [pasta](/code).
