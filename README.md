PyngPong
========

Pequeno projeto de remake do antigo jogo Pong em Python. O maior objetivo do projeto é o aprendizado de algumas bilbiotecas 
do Python com a colaboração no GitHub

Inicialmente possuímos os arquivos de imagem da bola e de background.
O jogo até agora possui um modo multijogador em que o P1 controla através das setas do teclado e o P2 através do 'W' e 'S'.
Possui também modo Multiplayer pela rede onde primeiramente deve ser aberto o PongMPServer (que servirá como o P1) e 
aguradará conexão na porta 8765. 
O codigo PongMPClient deve ser aberto para se conectar ao servidor que aguarda. Após a conexão o Client controla o P2 e o 
Server o P1.

Algumas coisas devem ser feitas a priori:
-Corrigir opções do menu.
-Melhorar o Menu.
-Exibir mensagem "Aperte ESPAÇO para começãr" no inicio do jogo.
-Corrigir bug da bola que fica presa nas extremidades as vezes.
-Incluir pontuação.
-Incluir/determinar o fim do jogo. (Atualmente o jogo é fechado quando a bola passa por um dos players).
-Alterar código MP para possibilitar ao client digitar o IP do P1.
-Alterar códigos do MP para possibilitar a conexão a ips fora localhost.
-Criar outros modos de jogo.
-Melhorar movimentação/animação da bola.
-etc.

É isso até aqui.
Aloha!
