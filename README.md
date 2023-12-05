# Uni Recognition

- [x] Codificou classes	
    Camera: Serve para capturar a imagem da camera e verificar possiveis erros de conexão.\

    CapturaFaces: Classe que utiliza a Camera para capturar imagens de um novo aluno e salva-las na pasta 'fotos' junto ao seu RA.\

    TreinadorReconhecimentoFacial: Treinador que utiliza as fotos capturadas pela classe anterior.\

    ReconhecimentoFacial: Classe que realiza o reconhecimento, utilizando o arquivo de treinamento, em tempo real.

- [x] Codificou atributos
    Camera: _camera -> responsável por ler as informações da câmera.\

    CapturaFaces: classificador -> Armazena o classificador que reconhece rostos.\
    camera -> Armazena a Classe Camera\
    amostra -> Contador da quantidade de fotos tiradas.\
    numeroAmostras -> Quantidade total de fotos a serem tiradas.\
    ra -> RA do aluno a ser incluido.\

    TreinadorReconhecimentoFacial: alunos -> Carrega arquivos com nomes dos alunos.\
    _classificador -> Carrega classificador de rostos (arq. de treinamento da IA)\
    reconhecedor -> Criar reconhecedor de faces LBPH.\
    camera -> Armazena a Classe Camera.\

    ReconhecimentoFacial: alunos -> Carrega arquivos com nomes dos alunos.\
    _classificador -> Carrega classificador de rostos (arq. de treinamento da IA)\
    reconhecedor -> Criar reconhecedor de faces LBPH.\
    camera -> Armazena a Classe Camera.

- [x] Codificou métodos
    Camera: read (self)\

    CapturaFaces: capturar (self)\

    TreinadorReconhecimentoFacial: getImagemComId(self) e treinarReconhecimentoFacial(self)\
    
    ReconhecimentoFacial: run e carregar_alunos com o parametro aluno_data_file -> Este parâmetro representa o caminho para o arquivo de dados dos alunos.\
    
- [x] Codificou atributos estáticos
    Camera: VIDEO_SCR -> É um atributo estático, pois é definido diretamente na classe Camera e não dentro de um método específico. Ele representa a fonte de vídeo e é compartilhado por todas as instâncias da classe.\

    Captura: VIDEO_SCR -> É um atributo estático, pois é definido diretamente na classe Camera e não dentro de um método específico. Ele representa a fonte de vídeo e é compartilhado por todas as instâncias da classe.\
    cascade_file -> É outro atributo que representa o arquivo do classificador Haar Cascade. Da mesma forma que VIDEO_SRC, ela é compartilhada por todas as instâncias da classe CapturaFaces.\

    ReconhecimentoFacial: carregar_alunos -> É um atributo estático, até porque ele não depende de nenhum atributo de instância específica da classe 'ReconhecimentoFacial'.\
    
- [x] Codificou métodos estáticos
    Captura: capturar -> É realizada a captura da imagem ou, em outras palavras, a foto é tirada.\

    Reconhecimento: carregar_alunos -> Faz o carregamento das imagens do banco de dados para comparação.\
    run -> Executa o reconhecimento, a comparação da imagem da câmera com o banco de dados.\
                 
- [x] Codificou métodos construtores
    Camera, CapturaFaces, TreinadorReconhecimentoFacial e ReconhecimentoFacial.

- [x] Codificou métodos destrutores
    Camera, CapturaFaces, TreinadorReconhecimentoFacial e ReconhecimentoFacial.

- [x] Codificou atributos protegidos e/ou privados
    Camera: Camera -> _camera se trata de um atributo protegido pois não deve ser alterada.\
    Reconhecimento: ReconhecimentoFacial -> _classificador contém o arquivo de treinamento da IA, portanto não deve ser mexido.
- [x] Codificou métodos protegidos e/ou privados.
    Colocamos os métodos construtores e destrutores, que são privados em todas as classes.

- [x] Instanciou objetos
    Camera, CapturaFaces, ReconhecimentoFacial e TreinadorReconhecimentoFacial

- [x] Instalou e usou bibliotecas de terceiros
    opencv-python e opencv-contrib-python: Biblioteca de visão de computador, utilizada para reconhecimento de rostos, visualização da inteligência artificial e acesso a câmera.
- [x] Codificou propriedades.
    ReconhecimentoFacial em Reconhecimento: verAlunos() -> Retorna lista de alunos carregadas do json.

- [x] Identificou e codificou classes de dados.
    No banco de dados com o cadastro de Aluno

- [x] Usou polimorfismo.
    Utilizamos a classe Câmera em 3 diferentes arquivos, Captura.py, Reconhecimento.py e Treinamento.py
    Em cada arquivo ela tem uma ação diferente, a mesma utiliza a câmera de 3 formas diferentes

- [x] Codificou padrões de projeto
    No código da câmera (Camera class), há um uso de um padrão singleton, onde a instância da câmera é criada apenas uma vez durante a execução do programa. Isso é alcançado com a ajuda do método init e del, garantindo que a instância da câmera seja única;
    No código do Reconhecimento Facial (ReconhecimentoFacial class), há um método run que é um ponto de entrada para iniciar a execução do reconhecimento facial. Isso pode ser considerado um padrão de método de fábrica, onde o método run cria e coordena os objetos necessários para realizar o reconhecimento facial;
    O método treinar na classe TreinadorReconhecimentoFacial usa um algoritmo específico para treinar o reconhecedor facial. Isso pode ser visto como um padrão de estratégia, onde diferentes algoritmos (classificadores e reconhecedores) podem ser usados intercambiavelmente.

- [x] Usou conceitos de SOLID
    A classe Camera e a classe CameraFeed estão alinhadas com o SRP, cada uma lidando com a funcionalidade;
    As classes ReconhecimentoFacial e CapturaFaces podem ser estendidas para adicionar novos comportamentos sem modificar o código existente
    A dependência da classe Camera dentro da classe ReconhecimentoFacial poderia ser injetada por meio de injeção de dependência ou passagem de instância. Isso permitiria uma maior flexibilidade na escolha da implementação da câmera.

- [x] Usou conceitos de código limpo.
    Nomes Descritivos, Funções Curtas, Comentários, Organização do Código, Manipulação de Exceções

- [x] Ocultou informações usando atributos e ou métodos protected/private 1 2
    Ocultamos as informações sobre o URL da câmera no arquivo .env

- [x] Identificou e codificou classes de comportamento
    Utilizamos herança na classe Camera, ela herda as funcionalidades do metodo read, da biblioteca cv2.

- [x] Contribuiu com o material da disciplina criando PRs/MRs (Kauê)
    https://gitlab.com/ettoreleandrotognoli/unimar-object-oriented-programming-i/-/merge_requests/2