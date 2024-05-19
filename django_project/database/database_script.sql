CREATE DATABASE IF NOT EXISTS escala_sgbd CHARACTER SET UTF8MB4;

USE escala_sgbd;

# Tabela com cada Colaborador e seus dados
CREATE TABLE IF NOT EXISTS colaborador (

id_colaborador INT AUTO_INCREMENT,
co_nome VARCHAR (200),
co_cpf VARCHAR(11),
co_telefone VARCHAR(15),
co_genero VARCHAR(15),
co_email VARCHAR(100),
co_privilegio INT,
co_status_colab INT,
co_senha VARCHAR(100),

PRIMARY KEY (id_colaborador)
);

# Tabela com cada Escala, nome, data de criação e status (0=SEM EVENTOS, 1=EM ANDAMENTO, 2=EVENTOS CONCLUÍDOS)
CREATE TABLE IF NOT EXISTS escala (

id_escala INT AUTO_INCREMENT,
es_nome VARCHAR(150),
es_data_criacao DATE,
es_status INT,

PRIMARY KEY (id_escala)
);

# Tabela com cada Evento de um Escala, com descrição, data, horários, status (0=RASCUNHO, 1=PUBLICADA, 2=EM ANDAMENTO, 3=CONCLUÍDA, 4=CANCELADA)
CREATE TABLE IF NOT EXISTS evento (

id_evento INT AUTO_INCREMENT,
ev_descricao VARCHAR(500),
ev_data DATE,
ev_horario TIMESTAMP,
ev_escala INT,
ev_status INT,

PRIMARY KEY (id_evento),
FOREIGN KEY (ev_escala) REFERENCES escala(id_escala)
);

# Tabela que relaciona um Evento com os seus líderes (Colaboradores). Os líderes podem editar detalhes pertinentes ao evento. São apontados pelo Responsável da escala.
CREATE TABLE IF NOT EXISTS eventos_lideres (

el_evento INT,
el_colaborador INT,

PRIMARY KEY (el_evento, el_colaborador),
FOREIGN KEY (el_evento) REFERENCES evento(id_evento),
FOREIGN KEY (el_colaborador) REFERENCES colaborador(id_colaborador)
);

# Tabela das Atividades pertinentes a um Evento, com a sua devida descrição e status (0=EM ANDAMENTO, 1=CONCLUÍDA, 2=CANCELADA)
CREATE TABLE IF NOT EXISTS atividade (

id_atividade INT AUTO_INCREMENT,
at_desc_atividade VARCHAR(500),
at_evento INT,
at_status INT,

PRIMARY KEY (id_atividade),
FOREIGN KEY (at_evento) REFERENCES evento(id_evento)
);

# Tabela que relaciona uma Atividade com o Colaborador Responsável.
CREATE TABLE IF NOT EXISTS atividade_colaborador (

ac_colaborador INT,
ac_atividade INT,

PRIMARY KEY (ac_colaborador, ac_atividade),
FOREIGN KEY (ac_colaborador) REFERENCES colaborador(id_colaborador),
FOREIGN KEY (ac_atividade) REFERENCES atividade(id_atividade)
);

# Tabela que relaciona uma Escala com o seu Colaborador Responsável. Eles podem editar detalhes pertinentes a sua escala. São apontadas pelos administradores do sistema.
CREATE TABLE IF NOT EXISTS resp_escala (

re_escala INT,
re_colaborador INT,

PRIMARY KEY (re_escala, re_colaborador),
FOREIGN KEY (re_escala) REFERENCES escala(id_escala),
FOREIGN KEY (re_colaborador) REFERENCES colaborador(id_colaborador)
);

# Tabela das Solicitações que um Colaborador podem fazer no sistema. Essas solicitações servem pros Administradores do Sistema poderem avaliar e, se inspirando nelas, criando atividades ou escalas pertinentes.
# Seus status são (0=EM RASCUNHO, 1=PUBLICADA, 2=LIDA, 3=EXCLUÍDA)
CREATE TABLE IF NOT EXISTS solicitacao (

id_solicitacao INT,
so_colaborador INT,
so_descricao VARCHAR(500),
so_data_inicio DATE,
so_data_fim DATE,
so_categoria VARCHAR(100),
so_status VARCHAR(100),

PRIMARY KEY (id_solicitacao),
FOREIGN KEY (so_colaborador) REFERENCES colaborador(id_colaborador)
);
