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

Este projeto é inspirado no clássico jogo *Pong*, mas com algumas mecânicas inovadoras para torná-lo ainda mais desafiador e interativo. 

### Regras Básicas

- **Objetivo**: O jogador deve defender sua base enquanto tenta ultrapassar a base adversária, movimentando seu pad com os gestos das mãos.
- **Pontuação**: O jogador que conseguir ultrapassar a base do oponente marca 1 ponto. 
- **Cargas**: Após cada ponto, os jogadores recebem "cargas" que podem ser utilizadas para ativar habilidades especiais (detalhadas abaixo).
- **Sets**: A cada 5 pontos acumulados, o jogador vence 1 set. O primeiro a alcançar o número de sets definidos no início do jogo será o vencedor.
- **Desempate**: Caso ambos os jogadores empatem em 4 pontos a 4, entra em vigor a regra "vai a 2": o jogador precisa ganhar dois pontos consecutivos para vencer o set.

### Controles e Configurações

1. **Menu Inicial**: 
   - No início do jogo, é exibido um menu. Pressione o botão **A** para acessar as configurações de número de sets (1, 3 ou 5).
   - Após selecionar o número de sets, os jogadores podem iniciar a partida.

2. **Movimentação dos Pads**:
   - Os pads são controlados pela rotação das mãos.
   - É possível inverter os controles pressionando o dedão contra o dedo médio, permitindo maior personalização para o jogador.

3. **Início do Jogo**:
   - Para começar, ambos os jogadores devem pressionar o dedão contra o dedo indicador simultaneamente. Quando isso acontecer, a bola será lançada e o jogo começará.

### Habilidades Especiais

As cargas acumuladas ao longo da partida podem ser gastas em habilidades estratégicas. Cada habilidade possui um custo específico:

1. **Invisibilidade**  
   - **Custo**: 1 carga  
   - O adversário do jogador que ativar esta habilidade ficará invisível, dificultando a visualização do pad. A invisibilidade dura por 3 rebatidas e pode ser acumulada por ativações consecutivas.

2. **Escudo**  
   - **Custo**: 2 cargas  
   - O jogador ganha um escudo que protege sua base. O escudo dura até a próxima rebatida ou até que o jogador marque um ponto.

3. **Atemporal**  
   - **Custo**: 3 cargas  
   - Reduz a velocidade da bola temporariamente, facilitando sua rebatida. A habilidade dura apenas uma rebatida.

4. **Power Pong**  
   - **Custo**: 4 cargas  
   - Ativa o buff máximo no pad do jogador. Independente do ponto onde a bola atingir o pad, ela será rebatida com a velocidade lateral máxima, tornando difícil para o adversário reagir.

### Limite de Cargas

- A capacidade máxima de cargas é 4.  
- Caso o jogador atinja o limite e tente receber uma carga extra, será alertado por meio do buzzer e LEDs piscando na luva.

## Documentação de Hardware

## Componentes utilizados

Os componentes utilizados neste projeto estão organizados em dois grupos: **componentes inclusos no kit da placa BitDogLabs** e **componentes externos**.

### Componentes da BitDogLabs

- **Joystick**  
  Utilizado para selecionar a quantidade de sets (partidas) do jogo.

- **Botão A**  
  Serve para inicializar o jogo e confirmar a quantidade de sets.

- **Buzzer**  
  Emite sons para tornar a partida mais dinâmica, sinalizando colisões com os pads dos jogadores, início e término do jogo, e pontuações.

- **Matriz de LEDs**  
  Exibe a pontuação de cada jogador, o set atual, e os sets vencidos por cada jogador.

- **Display OLED**  
  Indica o set atual e o número total de sets selecionados.

- **Raspberry Pi Pico**  
  Microcontrolador responsável pela programação e controle dos periféricos.

### Componentes Externos

- **2 Expansores IO I2C (PCF8575)**  
  Expandem a porta I2C para conectar os botões de habilidades, LEDs de sinalização de carga de poder, buzzer de alerta de carga cheia e LED RGB para identificar o jogador.  
  - [Comprar no Aliexpress](https://pt.aliexpress.com/item/1005007080964232.html)

- **2 MPU-6050**  
  Sensores utilizados para controlar os pads de cada jogador através da rotação da mão.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-1922679879-modulo-mpu6050-gy-521-sensor-acelermetro-giroscopio-3-eixos-_JM)

- **Display LCD TFT 128x160**  
  Exibe o jogo, o menu, e as partidas.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-5125731078-modulo-de-tela-lcd-tft-de-18-128x160-spi-color-st7735-_JM)

- **7 Resistores de 200Ω**  
  Controlam a intensidade da luz dos LEDs de carga e protegem o LED RGB contra sobrecorrente.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-1624979305-resistor-200-ohm-5-10pecas-_JM)

- **4 Resistores de 5kΩ (ou valor próximo)**  
  Usados como lógica pull-down para os botões de habilidades.
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-1722095500-kit-10-x-resistor-47k-ohm-14w-5-projeto-arduino-raspberry-_JM?matt_tool=14213447&matt_word=&matt_source=bing&matt_campaign=MLB_ML_BING_AO_CE-ALL-ALL_X_PLA_ALLB_TXS_ALL&matt_campaign_id=382858295&matt_ad_group=CE&matt_match_type=e&matt_network=o&matt_device=c&matt_keyword=default&msclkid=34bebad5f9b4163fa580dd9956da3a71&utm_source=bing&utm_medium=cpc&utm_campaign=MLB_ML_BING_AO_CE-ALL-ALL_X_PLA_ALLB_TXS_ALL&utm_term=4581596253419739&utm_content=CE)


- **4 LEDs (brancos ou azuis)**  
  Indicadores de carga de poder armazenada.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-2015068823-50x-led-5mm-azul-difuso-_JM)

- **1 Buzzer Passivo 5V**  
  Sinaliza que as cargas de poder estão cheias.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-2664375798-buzzer-passivo-5v-continuo-arduino-raspberry-pic-arm-_JM)

- **1 LED RGB (ânodo comum)**  
  Identifica o jogador através da cor do pad.  
  - [Comprar no Mercado Livre](https://produto.mercadolivre.com.br/MLB-3914705318-kit-10-leds-rgb-5mm-nodo-comum-_JM)

## Esquemático do Circuito da Luva

O esquemático do circuito da luva foi dividido em partes para facilitar o entendimento de cada seção do projeto.

### Conexões Principais

![Esquemático 1](https://github.com/user-attachments/assets/1f3aed6b-559a-4ec5-8188-8d86bfb70359)

Nesta parte do esquemático, são exibidas as conexões entre o **PCF8575**, **MPU6050** e o soquete que conecta a placa desenvolvida com a **BitDogLab**. Ambos os componentes estão conectados à mesma porta **I2C**. Como a BitDogLab possui duas portas I2C disponíveis, cada porta será utilizada por um jogador.

- **PCF8575**: Recebe alimentação pelo pino **VCC** e fornece saída pelo **VDD**. Como a alimentação é de 3.3V, é necessário realizar um curto entre **VCC** e **VDD** na parte traseira da placa para garantir a mesma tensão em ambos. Isso permite alimentar outros componentes pelo VDD.
- As portas do **PCF8575** estão conectadas a diversos periféricos, como botões, LEDs, LED RGB e buzzer.

### Lógica dos Botões

![Esquemático 2](https://github.com/user-attachments/assets/85e2cc81-4d0f-46b3-ab4a-cd1da1f87177)

Nesta seção, é apresentada a lógica para os botões:

- **D1 (dedão)**: Conectado ao **VDD**, com tensão de 3.3V.
- **D2, D3, D4 e D5 (outros dedos)**: Conectados a resistores de 5kΩ configurados em uma lógica **Pull-Down**, ligados ao **GND**.

Quando o dedão toca outro dedo, o circuito se fecha, funcionando de maneira similar ao pressionar um botão. O nível lógico resultante é lido pelas portas do **PCF8575**.

### LEDs Indicadores de Carga

![Esquemático 3](https://github.com/user-attachments/assets/5104c6df-90e2-4829-a48e-689d9fcdef14)

Esta parte do circuito controla os LEDs que indicam a quantidade de carga:

- Os LEDs estão conectados ao **VDD** e ao **GND** através das portas do **PCF8575**.
- Como o **PCF8575** não fornece corrente suficiente para acionar os LEDs diretamente quando configurado como saída de **VDD**, foi utilizada a ligação mostrada no esquemático, permitindo o funcionamento correto.

### LED RGB e Buzzer

![Esquemático 4](https://github.com/user-attachments/assets/43aa148b-2284-468d-8aa9-e6ad8c879042)

Nesta seção, são apresentados o LED RGB e o Buzzer:

- **LED RGB**: Utiliza um **ânodo comum**, o que permite funcionar corretamente com a lógica de alimentação similar à dos LEDs de carga.
- **Buzzer**: Conectado de maneira similar para superar a limitação de corrente mencionada.

## Projeto da Placa de Circuito Impresso (PCB)

A seguir, temos a imagem do layout da PCB desenvolvida:

![PCB](https://github.com/user-attachments/assets/89205839-e326-4e48-b60f-48d302fe7555)

### Organização dos Componentes

- **MPU6050** e **PCF8575**: Posicionados próximos ao soquete para facilitar as conexões.
- **LEDs de carga**: Alinhados próximos ao Buzzer, na ordem em que serão acionados.
- **LED RGB**: Localizado no lado direito da placa, identificando o jogador.
- **Fios para os dedos**: Organizados para se alinhar corretamente à luva, facilitando a conexão.
- **Furos de fixação**: Incluídos para prender a placa na luva, garantindo estabilidade.

O design priorizou uma PCB de face simples, otimizando o posicionamento dos componentes e minimizando o uso de trilhas cruzadas.

## Conexões

A conexão da placa desenvolvida foi feita através 2 cabos de 4 vias com conector JST conectados entre si conectada na entrada I2C da BitDogLab.

Outra conexão importante foi realizada com o LCD, seguindo o esquema de ligação descrito no repositório [pico-1p54in-lcd-graphics](https://github.com/BitDogLab/BitDogLab/tree/main/softwares/pico-1p54in-lcd-graphics). 

Para facilitar e tornar mais estável essa conexão, o professor **Fabiano Fruett** desenvolveu um **shield** específico para o LCD, que foi utilizado na etapa final do projeto.


## Construção mecânica

A PCB foi impressa pela FEEC através do SATE.

![pcb](https://github.com/user-attachments/assets/804206d5-80b3-47bb-8815-6f790df91090)

Após obter a placa foi soldado os componentes.

![pcb2](https://github.com/user-attachments/assets/e844368f-72b0-4318-a5a5-f2a40bce1790)

Com a placa pronta, foi utilizada uma luva lã como suporte e para o jogador poder vestir e jogar, através dos furos colocados anteriormente foi conturado esta placa na luva.

![pcb3](https://github.com/user-attachments/assets/67755a42-4000-4264-a980-8e271769c4eb)

Para a conexão nos dedos e utilizados como botões foi soldado jumpers com esta finalidade em uma fita de cobre que se enrolava nas pontas dos dedos.

![pcb4](https://github.com/user-attachments/assets/035cc579-0863-47eb-96a3-bd226c6b0dc2)

Após ser montado duas luvas para dois jogadores, as luvas foram conectas as placa BitDogLab através de 2 cabos de 4 vias com conector JST conectados entre si, como dito anteriormente, com o intutio de ter maior mobilidade para o jogador, além disto a conexão com o LCD com a BitDogLab foi feita através de um shield desenvolvido pelo Professor Fabiano Fruett.

![Imagem do WhatsApp de 2024-11-22 à(s) 15 47 27_c108c282](https://github.com/user-attachments/assets/4a478f5f-6d01-4dd4-ae0f-56b5acd76491)


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

Os arquivos que compõe a memória da Raspberry Pi Pico, necessários para executar o jogo são os mostrados abaixo, e estão disponíveis nesta [pasta](/code).

1. Lógica principal do programa
    - *main.py*: Inicialização e execução da máquina de estados.

2. Lógica de jogo
    - *game_classes.py*: Classes da lógica de Jogo, como a classe de jogador, da bola e do escudo.
    - *game_constants.py*: Valores constantes como tamanhos dos jogadores, dimensões da tela e outros.
    - *game_routines.py*: Rotinas de execução de cada estado da máquina de estados. Responsável por orquestrar os objetos definidos a depender do estado corrente.

3. Periféricos
    - *mpu6050.py*: Biblioteca para interação com o MPU6050, sensor I2C acelerômetro e giroscópio de 6 eixos.
    - *pcf8575.py*: Biblioteca para interação com o PCF8575, extensor de I/O I2C com diversas portas GPIO.
    - *ssd1306.py*: Biblioteca para interação com o SSD1306, display OLED I2C 128x64px.
    - *tft_config.py*: Arquivo de configuração do display LCD SPI utilizado, definindo a equivalência das portas do display com as da Raspberry.
    - *glove.py*: Biblioteca criada para facilitar interação com os componentes presentes na luva, oferencendo acesso direto ao valor do ângulo em que a luva está posicionada e aos periféricos conectados ao extensor de I/O. Também executa uma rotina de testes na luva se executado diretamente.
    - *peripherals.py*: Classe de incialização de todos os periféricos controlados pelo projeto, também carrega uma referência a cada um deles para evitar a necessidade de passagem de muitos parâmetros para as rotinas do jogo.

4. Funções auxiliares
    - *util.py*

5. Fontes para escrita no display LCD
    - *vga1_16x32.py*
    - *vga1_8x8.py*
    - *vga1_bold_16x32.py*

## Resultados

O projeto foi concluído com sucesso e proporcionou um grande aprendizado para a equipe. Como o projeto é um jogo, nos divertimos muito durante o desenvolvimento, especialmente ao imaginar a dinâmica e a diversão que os jogadores teriam. Utilizamos nossa criatividade para projetar os comandos do controle, os poderes e as interações do jogo.

### Desafios Enfrentados

Durante o desenvolvimento, enfrentamos alguns desafios importantes que contribuíram para a melhoria contínua do projeto:

- **Substituição do Display**: No início, o display originalmente escolhido teve que ser substituído, o que exigiu ajustes significativos no código. Embora isso tenha demandado tempo, essa experiência nos ajudou a modularizar o código, facilitando futuras alterações e melhorias.
  
- **Atrasos na Produção da Placa**: O processo de impressão da placa sofreu atrasos, o que impediu a realização de testes e afetou o desenvolvimento de funcionalidades adicionais, como novas utilidades para o LED RGB e o buzzer.

### Melhorias Futuras

Identificamos diversas áreas para melhorar o projeto em versões futuras:

#### 1. **Hardware**
   - **Redução do Tamanho da Placa**: A placa pode ser compactada, eliminando o uso de módulos como o PCF8575 e o MPU6050 e substituindo-os por componentes individuais.
   - **Uso de Componentes SMD**: A utilização de componentes SMD (Surface-Mounted Device) ajudará a reduzir ainda mais o tamanho da placa.
   - **Conforto para o Jogador**: Melhorar o material e o método de fixação da luva, garantindo maior conforto ao jogador durante o uso.
   
#### 2. **Funcionalidades**
   - **Uso das Portas Disponíveis**: Aproveitar as portas restantes do PCF8575 para adicionar mais LEDs para indicar níveis de carga ou novos poderes.
   - **Otimização do Código**: Reescrever o código em C para melhorar a eficiência e tornar o jogo mais dinâmico.

Essas melhorias visam tornar o projeto mais eficiente, compacto e com maior interatividade para o usuário.

  
