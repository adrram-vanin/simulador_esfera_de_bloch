SIMULADOR DIDÁTICO DA ESFERA DE BLOCH
======================================

Arquivo principal:
    simulador_esfera_bloch.py

Arquivo de documentação:
    LEIA-ME.txt

1. OBJETIVO
===========

Este aplicativo foi criado para estudar, de forma visual e interativa, a representação
de um qubit puro na esfera de Bloch.

O programa relaciona simultaneamente:

    • o estado quântico |psi> = a|0> + b|1>;
    • as amplitudes complexas a e b;
    • as probabilidades P(0) e P(1);
    • os ângulos theta e phi da esfera de Bloch;
    • a fase global gamma;
    • as coordenadas cartesianas (x, y, z);
    • os valores esperados <X>, <Y> e <Z>;
    • as probabilidades de medida nas bases X, Y e Z;
    • a ação de portas quânticas de um qubit.

Todos os resultados são atualizados automaticamente enquanto os controles deslizantes
são movidos.


2. REQUISITOS
=============

Requisitos obrigatórios:

    1. Python instalado no computador.
       Recomendado: Python 3.10 ou superior.

    2. Tkinter
       Biblioteca usada para a interface gráfica.

       No Windows e no macOS, normalmente acompanha a instalação padrão do Python.

       Ubuntu/Debian:
           sudo apt install python3-tk

       Fedora:
           sudo dnf install python3-tkinter

    3. NumPy
       Usado para cálculos vetoriais, números complexos e operadores.

    4. Matplotlib
       Usado para desenhar a esfera de Bloch em 3D.

Instalação manual das bibliotecas Python:

    python -m pip install numpy matplotlib

No Windows, também pode funcionar:

    py -m pip install numpy matplotlib


3. VERIFICAÇÃO AUTOMÁTICA DE DEPENDÊNCIAS
=========================================

Ao iniciar, o aplicativo verifica se NumPy e Matplotlib estão instalados.

Se alguma biblioteca estiver ausente, será aberta uma janela indicando quais
bibliotecas faltam e oferecendo a opção:

    "Instalar agora"

O programa tentará executar automaticamente a instalação usando o pip.

IMPORTANTE:
O Tkinter normalmente não é instalado pelo pip. Caso esteja ausente, o aplicativo
mostra instruções de instalação para o sistema operacional.


4. QISKIT É OBRIGATÓRIO?
========================

Não.

O aplicativo NÃO precisa do Qiskit para desenhar a esfera ou realizar os cálculos.
Essa foi uma escolha proposital para tornar o programa mais leve e simples de executar.

Entretanto, o aplicativo mostra, em tempo real, um trecho de código Qiskit equivalente
ao estado atualmente exibido.

Para executar esse trecho em outro ambiente, instale o Qiskit separadamente:

    python -m pip install qiskit

ou:

    pip install qiskit


5. COMO EXECUTAR
================

Método 1 - Duplo clique
-----------------------
No Windows, se arquivos .py estiverem associados ao Python, dê duplo clique em:

    simulador_esfera_bloch.py

Método 2 - Terminal
-------------------
Abra um terminal na pasta do arquivo e execute:

    python simulador_esfera_bloch.py

No Windows, também pode funcionar:

    py simulador_esfera_bloch.py

Se a janela abrir e fechar imediatamente, execute pelo terminal para visualizar
qualquer mensagem de erro.


6. TESTE DO TKINTER
===================

Para conferir se o Tkinter está instalado corretamente:

    python -m tkinter

Se estiver funcionando, uma pequena janela de teste será aberta.


7. MODELO FÍSICO REPRESENTADO
=============================

Um estado puro de um qubit pode ser escrito como:

    |psi> = a|0> + b|1>

com a condição de normalização:

    |a|^2 + |b|^2 = 1

Também pode ser parametrizado por:

    |psi> = exp(i gamma) [
                cos(theta/2)|0>
                + exp(i phi) sin(theta/2)|1>
            ]

onde:

    theta = ângulo polar na esfera de Bloch;
    phi   = fase relativa / ângulo azimutal;
    gamma = fase global.

A fase global gamma não altera resultados físicos observáveis e, portanto,
não altera a posição do vetor na esfera de Bloch.


8. COORDENADAS DA ESFERA DE BLOCH
=================================

A partir das amplitudes a e b:

    x = 2 Re(a* b)
    y = 2 Im(a* b)
    z = |a|^2 - |b|^2

onde a* representa o complexo conjugado de a.

Para um estado puro:

    x^2 + y^2 + z^2 = 1

As coordenadas também podem ser escritas como:

    x = sin(theta) cos(phi)
    y = sin(theta) sin(phi)
    z = cos(theta)


9. PROBABILIDADES
=================

Na base computacional:

    P(0) = |a|^2
    P(1) = |b|^2

com:

    P(0) + P(1) = 1

IMPORTANTE:
As probabilidades sozinhas não determinam completamente um estado quântico.
A fase relativa phi também é necessária.

Exemplo:

    |+>  = (|0> + |1>)/sqrt(2)
    |+i> = (|0> + i|1>)/sqrt(2)

Ambos possuem:

    P(0) = 0,5
    P(1) = 0,5

mas ocupam posições diferentes na esfera de Bloch.


10. ABAS DE CONTROLE
====================

Aba "theta, phi, gamma"
------------------------
Permite modificar diretamente:

    theta - ângulo polar;
    phi   - fase relativa;
    gamma - fase global.

Mover apenas gamma não deve mover o vetor da esfera.

Aba "Probabilidades"
---------------------
Permite modificar:

    P(0)
    fase relativa phi

O programa calcula automaticamente:

    P(1) = 1 - P(0)

Aba "Amplitudes"
-----------------
Permite trabalhar diretamente com:

    |a|
    arg(a)
    arg(b)

O módulo de b é calculado automaticamente para garantir:

    |a|^2 + |b|^2 = 1


11. POR QUE NÃO EXISTE UM CONTROLE "psi"?
===========================================

O símbolo |psi> é usado como nome do estado quântico.
Ele não é um parâmetro independente como theta ou phi.

Por isso, o aplicativo mostra |psi> como resultado da combinação dos parâmetros,
em vez de criar uma barra chamada "psi".


12. POR QUE NÃO EXISTE UM COEFICIENTE c?
========================================

Um qubit possui apenas dois estados de base:

    |0>
    |1>

Portanto:

    |psi> = a|0> + b|1>

Uma expressão com três amplitudes, por exemplo:

    a|0> + b|1> + c|2>

descreveria um sistema de três níveis, um qutrit, e não um qubit.


13. ESTADOS NOTÁVEIS
====================

O aplicativo possui botões para:

    |0>   direção +z
    |1>   direção -z

    |+>   direção +x
    |->   direção -x

    |+i>  direção +y
    |-i>  direção -y

Esses estados facilitam a identificação dos eixos X, Y e Z.


14. PORTAS QUÂNTICAS DISPONÍVEIS
================================

Portas discretas:

    X
    Y
    Z
    H
    S
    T

Rotações ajustáveis:

    Rx(alpha)
    Ry(alpha)
    Rz(alpha)

O ângulo alpha é controlado por uma barra deslizante.
Depois de aplicar qualquer porta, a esfera e todos os valores numéricos são
atualizados imediatamente.


15. INTERPRETAÇÃO DE ALGUMAS PORTAS
===================================

Porta X
-------
Rotação de 180 graus em torno do eixo x.

Exemplo:

    |0> -> |1>

Porta Y
-------
Rotação de 180 graus em torno do eixo y, a menos de fase global.

Porta Z
-------
Rotação de fase em torno do eixo z.

Exemplo:

    |+> -> |->

Hadamard H
----------
Relaciona os eixos x e z.

Exemplos:

    H|0> = |+>
    H|1> = |->

Portas S e T
------------
Introduzem fases relativas:

    S -> pi/2
    T -> pi/4


16. RESULTADOS EXIBIDOS
=======================

A lateral direita apresenta simultaneamente:

    • |psi> = a|0> + b|1>;
    • valores complexos de a e b;
    • verificação de |a|^2 + |b|^2 = 1;
    • P(0) e P(1);
    • theta, phi e gamma em radianos e graus;
    • x, y e z;
    • comprimento r = sqrt(x^2+y^2+z^2);
    • <X>, <Y> e <Z>;
    • probabilidades de medição nas bases X, Y e Z;
    • trecho Qiskit equivalente ao estado atual.

Para um qubit puro:

    <X> = x
    <Y> = y
    <Z> = z


17. PROBABILIDADES NAS BASES X, Y E Z
=====================================

Base X:

    P(+x) = (1 + x)/2
    P(-x) = (1 - x)/2

Base Y:

    P(+y) = (1 + y)/2
    P(-y) = (1 - y)/2

Base Z:

    P(0) = (1 + z)/2
    P(1) = (1 - z)/2


18. CÓDIGO QISKIT GERADO PELO APLICATIVO
========================================

O aplicativo mostra um circuito equivalente ao estado atual utilizando:

    Ry(theta)
    Rz(phi)

A preparação básica é:

    qc.ry(theta, 0)
    qc.rz(phi, 0)

Essa sequência reproduz o mesmo estado físico até uma fase global.
Para reproduzir exatamente a mesma representação vetorial usada na interface,
o programa também mostra um ajuste de:

    qc.global_phase


19. OBSERVAÇÃO SOBRE Rz
=======================

O aplicativo usa a convenção padrão de rotação empregada em circuitos quânticos:

    Rz(alpha) = diag(exp(-i alpha/2), exp(i alpha/2))

Essa matriz difere apenas por fase global da convenção:

    diag(1, exp(i alpha))

Como a fase global não altera o estado físico, ambas descrevem a mesma rotação na
esfera de Bloch.


20. LIMITAÇÕES DA VERSÃO ATUAL
==============================

    1. O aplicativo representa apenas um qubit.
    2. Representa apenas estados puros.
    3. Não representa estados mistos por matriz densidade.
    4. Não simula ruído ou decoerência.
    5. Não simula erros de hardware.
    6. Não executa um processador quântico real.
    7. O Qiskit não é usado internamente; apenas é mostrado um código equivalente.

Para estados mistos seria necessário trabalhar com uma matriz densidade rho.
Nesse caso, o vetor de Bloch poderia ter comprimento:

    0 <= r <= 1

e estados mistos apareceriam no interior da esfera.


21. SUGESTÕES DE EXPLORAÇÃO DIDÁTICA
====================================

Atividade 1 - Polos
-------------------
Clique em |0> e |1>.
Observe theta, z, P(0) e P(1).

Atividade 2 - Superposição
--------------------------
Clique em |+>.
Observe:

    P(0) = P(1) = 0,5
    x = 1

Atividade 3 - Mesmas probabilidades, estados diferentes
-------------------------------------------------------
Compare |+> e |+i>.
As probabilidades são iguais, mas a posição na esfera é diferente.

Atividade 4 - Fase relativa
---------------------------
Defina P(0) = P(1) = 0,5 e mova apenas phi.
O vetor deve percorrer o equador.

Atividade 5 - Fase global
-------------------------
Escolha qualquer estado e mova apenas gamma.
As amplitudes mudam de fase, mas x, y, z e as probabilidades não mudam.

Atividade 6 - Porta X
---------------------
Comece em |0> e aplique X.
O vetor deve ir de +z para -z.

Atividade 7 - Hadamard
----------------------
Comece em |0> e aplique H.
O resultado deve ser |+>, levando o vetor de +z para +x.

Atividade 8 - Rotação contínua
------------------------------
Comece em |0>, ajuste alpha e aplique Ry(alpha).
Observe a relação entre a operação unitária e o movimento geométrico na esfera.


22. SOLUÇÃO DE PROBLEMAS
========================

Erro: No module named numpy
----------------------------
Execute:

    python -m pip install numpy

Erro: No module named matplotlib
---------------------------------
Execute:

    python -m pip install matplotlib

Erro relacionado ao Tkinter
---------------------------
Windows/macOS:
    reinstale o Python e garanta que o suporte a Tcl/Tk esteja incluído.

Ubuntu/Debian:
    sudo apt install python3-tk

Fedora:
    sudo dnf install python3-tkinter

Mais de uma versão do Python instalada
--------------------------------------
Confira:

    python --version
    py --version

Windows:

    where python

Linux/macOS:

    which python


23. AMBIENTES RECOMENDADOS
==========================

O aplicativo foi projetado para execução local em:

    Windows
    Linux
    macOS

Ele não é indicado para execução direta no Google Colab, pois usa uma janela gráfica
Tkinter local.

Para o Colab, prefira códigos Qiskit e gráficos em células de notebook.


24. ARQUIVOS NECESSÁRIOS
========================

Necessário:

    simulador_esfera_bloch.py

Documentação:

    LEIA-ME.txt

O aplicativo não precisa de imagens externas, banco de dados ou outros arquivos auxiliares.


25. RESUMO RÁPIDO
=================

Executar:

    python simulador_esfera_bloch.py

Dependências:

    Python
    Tkinter
    NumPy
    Matplotlib

Instalar bibliotecas Python:

    python -m pip install numpy matplotlib

Qiskit:

    opcional

Instalação opcional do Qiskit:

    python -m pip install qiskit


26. FINALIDADE PEDAGÓGICA
=========================

O simulador foi pensado como ferramenta de visualização e conferência para relacionar:

    álgebra de estados
        |
        v
    amplitudes complexas
        |
        v
    probabilidades
        |
        v
    coordenadas de Bloch
        |
        v
    representação geométrica
        |
        v
    ação das portas quânticas

A visualização não substitui a resolução algébrica dos exercícios, mas ajuda a conferir
resultados e desenvolver intuição geométrica sobre o comportamento de um qubit.
