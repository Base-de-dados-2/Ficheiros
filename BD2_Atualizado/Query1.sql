-- Criação da Tabela Utilizador_BD2
CREATE TABLE Utilizador_BD2 (
    ID_Utilizador INT PRIMARY KEY IDENTITY(1,1),
    Nome NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Telefone NVARCHAR(20),
    Tipo_Utilizador NVARCHAR(50) NOT NULL, -- Ex.: 'Cliente', 'Vendedor', 'Administrador'
    Data_Criacao DATETIME DEFAULT GETDATE()
);

-- Criação da Tabela Stand_BD2
CREATE TABLE Stand_BD2 (
    ID_Stand INT PRIMARY KEY IDENTITY(1,1),
    Nome NVARCHAR(100) NOT NULL,
    Localizacao NVARCHAR(100) NOT NULL,
    Responsavel NVARCHAR(100)
);

-- Criação da Tabela Fornecedor_BD2
CREATE TABLE Fornecedor_BD2 (
    ID_Fornecedor INT PRIMARY KEY IDENTITY(1,1),
    Nome NVARCHAR(100) NOT NULL,
    Contato NVARCHAR(50),
    Veiculos_Fornecedor NVARCHAR(255) -- Informações gerais sobre os veículos fornecidos
);

-- Criação da Tabela Veiculo_BD2 com conexão ao Fornecedor
CREATE TABLE Veiculo_BD2 (
    ID_Veiculo INT PRIMARY KEY IDENTITY(1,1),
    Marca NVARCHAR(50) NOT NULL,
    Modelo NVARCHAR(50) NOT NULL,
    Ano INT NOT NULL,
    Preco DECIMAL(10, 2) NOT NULL,
    Quilometragem INT NOT NULL,
    Cor NVARCHAR(20),
    Tipo_Combustivel NVARCHAR(20),
    ID_Stand INT NOT NULL,
    ID_Fornecedor INT NOT NULL, -- Conexão com o fornecedor
    CONSTRAINT FK_Veiculo_Stand_BD2 FOREIGN KEY (ID_Stand) REFERENCES Stand_BD2(ID_Stand),
    CONSTRAINT FK_Veiculo_Fornecedor_BD2 FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedor_BD2(ID_Fornecedor)
);

-- Criação da Tabela Cliente_BD2
CREATE TABLE Cliente_BD2 (
    ID_Cliente INT PRIMARY KEY IDENTITY(1,1),
    ID_Utilizador INT NOT NULL,
    Historico_Compras NVARCHAR(255),
    Interesse_Veiculos INT, -- Agora é uma Foreign Key para ID_Veiculo
    CONSTRAINT FK_Cliente_Utilizador_BD2 FOREIGN KEY (ID_Utilizador) REFERENCES Utilizador_BD2(ID_Utilizador),
    CONSTRAINT FK_Cliente_Interesse_Veiculo_BD2 FOREIGN KEY (Interesse_Veiculos) REFERENCES Veiculo_BD2(ID_Veiculo)
);

-- Criação da Tabela Vendedor_BD2
CREATE TABLE Vendedor_BD2 (
    ID_Vendedor INT PRIMARY KEY IDENTITY(1,1),
    ID_Utilizador INT NOT NULL,
    Cargo NVARCHAR(50),
    Vendas_Realizadas INT DEFAULT 0,
    CONSTRAINT FK_Vendedor_Utilizador_BD2 FOREIGN KEY (ID_Utilizador) REFERENCES Utilizador_BD2(ID_Utilizador)
);

-- Criação da Tabela TransacaoVenda_BD2
CREATE TABLE TransacaoVenda_BD2 (
    ID_Transacao INT PRIMARY KEY IDENTITY(1,1),
    ID_Veiculo INT NOT NULL,
    ID_Cliente INT NOT NULL,
    ID_Vendedor INT NOT NULL,
    Data_Venda DATE NOT NULL,
    Valor_Venda DECIMAL(10, 2) NOT NULL,
    CONSTRAINT FK_Transacao_Veiculo_BD2 FOREIGN KEY (ID_Veiculo) REFERENCES Veiculo_BD2(ID_Veiculo),
    CONSTRAINT FK_Transacao_Cliente_BD2 FOREIGN KEY (ID_Cliente) REFERENCES Cliente_BD2(ID_Cliente),
    CONSTRAINT FK_Transacao_Vendedor_BD2 FOREIGN KEY (ID_Vendedor) REFERENCES Vendedor_BD2(ID_Vendedor)
);

-- Criação da Tabela HistoricoVeiculo_BD2
CREATE TABLE HistoricoVeiculo_BD2 (
    ID_Historico INT PRIMARY KEY IDENTITY(1,1),
    ID_Veiculo INT NOT NULL,
    Manutencoes NVARCHAR(255),
    Acidentes NVARCHAR(255),
    Donos_Anteriores NVARCHAR(255),
    CONSTRAINT FK_HistoricoVeiculo_Veiculo_BD2 FOREIGN KEY (ID_Veiculo) REFERENCES Veiculo_BD2(ID_Veiculo)
);

-- Criação da Tabela Manutencao_BD2
CREATE TABLE Manutencao_BD2 (
    ID_Manutencao INT PRIMARY KEY IDENTITY(1,1),
    ID_Veiculo INT NOT NULL,
    Data_Manutencao DATE NOT NULL,
    Tipo_Manutencao NVARCHAR(50) NOT NULL,
    Descricao NVARCHAR(255),
    Oficina_Responsavel NVARCHAR(100),
    CONSTRAINT FK_Manutencao_Veiculo_BD2 FOREIGN KEY (ID_Veiculo) REFERENCES Veiculo_BD2(ID_Veiculo)
);

-- Criação da Tabela TestDrive_BD2
CREATE TABLE TestDrive_BD2 (
    ID_TestDrive INT PRIMARY KEY IDENTITY(1,1),
    ID_Cliente INT NOT NULL,
    ID_Veiculo INT NOT NULL,
    Data_Hora_TestDrive DATETIME NOT NULL,
    Feedback_Cliente NVARCHAR(255), -- Mantido o feedback do cliente
    CONSTRAINT FK_TestDrive_Cliente_BD2 FOREIGN KEY (ID_Cliente) REFERENCES Cliente_BD2(ID_Cliente),
    CONSTRAINT FK_TestDrive_Veiculo_BD2 FOREIGN KEY (ID_Veiculo) REFERENCES Veiculo_BD2(ID_Veiculo)
);

-- Criação da Tabela Promocao_BD2
CREATE TABLE Promocao_BD2 (
    ID_Promocao INT PRIMARY KEY IDENTITY(1,1),
    Nome_Promocao NVARCHAR(100) NOT NULL,
    ID_Veiculo INT NULL,
    Categoria NVARCHAR(50) NULL,
    Data_Inicio DATE NOT NULL,
    Data_Termino DATE NOT NULL,
    Percentual_Desconto DECIMAL(5, 2) CHECK (Percentual_Desconto BETWEEN 0 AND 100),
    Descricao NVARCHAR(255),
    CONSTRAINT FK_Promocao_Veiculo_BD2 FOREIGN KEY (ID_Veiculo) REFERENCES Veiculo_BD2(ID_Veiculo)
);
