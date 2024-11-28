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

O software foi desenvolvido em MicroPython, utilizando algumas bibliotecas escritas em Python, que estão
inclusas aqui no GitHub também.

Além destas bibliotecas escritas em Python, foi carregada junto ao firmware da placa uma biblioteca escrita
em C, para interação com o display. Isto foi feito devido ao grande número de dados comunicados com o
display, em que utilizar uma biblioteca em Python se mostrou ineficiente.

A biblioteca utilizada foi [st7789_mpy](https://github.com/russhughes/st7789_mpy), no entanto, ao utilizar
o firmware disponibilizado no repositório da biblioteca ocorreram alguns erros, acreditamos que tenha sido
por causa da versão do MicroPython com a que ela tinha sido compilada.

Para contornar este problema, foi gerado firmware com a última versão de MicroPython disponível até o momento
a versão 1.24. O arquivo está disponível na raiz do repositório, e chama-se firmware.uf2. O processo de
geração deste firmware, com a biblioteca carregada, foi obtido de uma resposta de uma Issue colocada no
projeto, que pedia que o firmware atualizado fosse disponibilizado. [PIBSAS](https://github.com/russhughes/st7789_mpy/issues/168#issuecomment-2342353619) descreve o que deve ser feito, e funcionou corretamente.

### Maquina de estados

O fluxo do programa se baseia em uma máquina de estados, que pode ser vista na Figura abaixo

![Máquina de estados do projeto](https://github.com/user-attachments/assets/f45a0cf4-fdf4-40d4-9e5f-160254ea969e)

As tarefas de cada estado são as seguintes:

- MENU: Exibe o nome do jogo e a instrução de início piscando. O programa aguarda até que o botão A seja pressionado para avançar para o próximo estado.

- CHOOSE SETS: Mostra na tela as opções de quantidade de sets (melhor de um, três ou cinco) e monitora o deslocamento horizontal do joystick para alterar a opção selecionada. Ao pressionar o botão A, a opção de número de sets é confirmada, e o jogo avança para o próximo estado.

- GAME BREAK: Aguarda até que ambos os jogadores pressionem seus botões simultaneamente, indicando que estão prontos para o início da partida.

- GAME RUNNING: Monitora os dados do acelerômetro para atualizar a posição dos pads dos jogadores, verifica o uso do poder de escudo e simula a física da bolinha, incluindo colisões com as paredes e com os pads dos jogadores.

- END: Exibe uma animação, toca a música de vitória e mostra na tela o nome do jogador vencedor.

### Lógica do sensor

O sensor retorna valores de aceleração em três eixos, mas utilizamos apenas dois para calcular o ângulo em que o dispositivo está sendo segurado, conforme ilustrado na figura abaixo:

![Acelerometro](https://github.com/user-attachments/assets/1dffd47a-2043-4bf4-8d84-0ea321bc047a)

![Formula do angulo](https://github.com/user-attachments/assets/f623fb4a-ab9a-4e30-9579-c2bebb573e21)

Devido a flutuações nas leituras do sensor, aplicamos um filtro digital passa-baixas para suavizar os valores do ângulo, com compensação para lidar com a descontinuidade angular (que ocorre quando o valor do ângulo salta de -π para π). Após isso, os valores de ângulo são escalados para uma posição linear, correspondente ao y do pad na tela. Essa conversão relaciona o intervalo de -45 a 45 graus com os limites da tela, que vão de PAD_WIDTH//2 até WIDTH - PAD_WIDTH//2. Aqui, WIDTH é o tamanho da tela e PAD_WIDTH é a largura do pad do jogador. Por fim, o programa valida a posição calculada, garantindo que o pad não saia da tela. A figura a seguir ilustra esse processo de forma simplificada.

![Fluxo de dados do sensor](https://github.com/user-attachments/assets/5a8bcb13-34fd-4cb4-85a5-d28a4201f551)

### Velocidade da bolinha

Como comentado no início, a velocidade da bolinha aumenta gradualmente cada vez que ela é rebatida.
Para manter o jogo dinâmico, a velocidade inicial da bola em cada round se ajusta ao desempenho dos
jogadores. Isto é feito configurando uma velocidade mínima que ela pode estar, que é a velocidade
no primeiro round. Em seguida, ao fim de cada round ela perde 30% de sua velocidade, permitindo que
os jogadores retornem de um ponto em que a bola não esteja tão rápida nem lenta demais.

### Organização dos Arquivos

Os arquivos podem ser encontrados nesta [pasta](/code)

