# Projeto - Biblioteca Pessoal Digital

[![Python CI - Testes Pytest](https://github.com/samsilveira/personal-library/actions/workflows/python-tests.yml/badge.svg)](https://github.com/samsilveira/personal-library/actions/workflows/python-tests.yml)

Atividade prática da disciplina de Programação Orientada à Objetos (ES0008) para composição parcial de nota.

## 📖 Descrição

Sistema de gerenciamento de biblioteca digital pessoal com interface de linha de comando (CLI), desenvolvido aplicando conceitos avançados de Programação Orientada a Objetos, incluindo herança múltipla, encapsulamento, padrões de projeto e persistência de dados.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório (ou descompacte o arquivo):**

```bash
   cd biblioteca-digital
```

2. **Crie um ambiente virtual (recomendado):**

```bash
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
```

3. **Instale as dependências:**

```bash
   pip install -r requirements.txt
```

### Execução

**Comandos disponíveis:**

```bash
# Ver todos os comandos
python -m src.cli.main --help

# Cadastrar um livro
python -m src.cli.main cadastrar "1984" "George Orwell" "Secker" 1949 "Ficção" 328 --isbn "978-0452284234"

# Listar todas as publicações
python -m src.cli.main listar

# Iniciar leitura de uma publicação
python -m src.cli.main iniciar-leitura 1

# Finalizar leitura
python -m src.cli.main finalizar 1

# Avaliar publicação (0-10)
python -m src.cli.main avaliar 1 9.5

# Buscar publicações
python -m src.cli.main buscar "Orwell" --por autor

# Exibir relatório completo
python -m src.cli.main relatorio

# Relatórios com Strategy Pattern
python -m src.cli.main relatorio-avaliacoes
python -m src.cli.main top-rated --limit 5
python -m src.cli.main progresso-detalhado

# Definir metas
python -m src.cli.main definir-meta 20 --limite-simultaneo 3
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/
pytest tests/strategies/
```

---

## 📁 Estrutura do Projeto

```text
biblioteca_pessoal_digital/
├── docs/                          # Documentação complementar
│   └── uml.md                     # Diagramas UML detalhados
├── src/                           # Código fonte principal
│   ├── cli/                       # Interface de linha de comando
│   │   └── main.py                # Comandos CLI
│   ├── data/                      # Camada de persistência
│   │   └── repository.py          # Persistência JSON
│   ├── models/                    # Modelos de domínio
│   │   ├── annotation.py          # Anotações
│   │   ├── collection.py          # Gerenciador de publicações
│   │   ├── configuration.py       # Configurações do usuário
│   │   ├── mixins.py              # DigitalAsset mixin
│   │   ├── publication.py         # Publication, Book, Magazine
│   │   ├── report.py              # Relatórios básicos
│   │   └── user.py                # Usuário
│   └── strategies/                # Strategy Pattern para relatórios
│       ├── report_strategy.py     # Interface abstrata
│       ├── evaluation_report.py   # Relatório de avaliações
│       ├── top_rated_report.py    # Top publicações
│       └── progress_report.py     # Progresso anual
├── tests/                         # Testes unitários
├── library.json                   # Dados persistidos
├── settings.json                  # Configurações do usuário
└── requirements.txt               # Dependências
```

---

## 🎯 Decisões de Design e Padrões Implementados

### 1. **Herança Múltipla com Mixin**

**Decisão:** `Book` e `Magazine` herdam de `Publication` (funcionalidades core) e `DigitalAsset` (capacidades de arquivo digital).

**Justificativa:**

- Permite adicionar funcionalidade de arquivo digital sem duplicação de código
- Publicações podem existir sem arquivo digital (opcional)
- Segue o princípio DRY (Don't Repeat Yourself)

```python
class Book(Publication, DigitalAsset):
    # Herda comportamentos de leitura + capacidades digitais
```

### 2. **Strategy Pattern para Relatórios**

**Decisão:** Diferentes algoritmos de geração de relatórios implementados como estratégias intercambiáveis.

**Justificativa:**

- Permite adicionar novos tipos de relatórios sem modificar código existente (Open/Closed Principle)
- Facilita testes unitários de cada estratégia independentemente
- Cliente (CLI) pode escolher qual estratégia usar em tempo de execução

**Classes Implementadas:**

- `ReportStrategy` (abstrata)
- `EvaluationReportStrategy` - Estatísticas de avaliações
- `TopRatedReportStrategy` - Rankings personalizáveis
- `ProgressReportStrategy` - Análise de metas anuais

### 3. **Encapsulamento com @property**

**Decisão:** Atributos críticos protegidos com validação via properties.

**Exemplos:**

```python
@property
def title(self):
    return self._title

@title.setter
def title(self, value: str):
    if not value or not value.strip():
        raise ValueError("Title cannot be empty")
    self._title = value.strip()
```

**Justificativa:**

- Previne estados inválidos
- Validação centralizada
- Permite futuras modificações sem quebrar interface pública

### 4. **Separação de Responsabilidades**

**Publication:** Gerencia estado interno (leitura, avaliação)
**Collection:** Gerencia conjunto de publicações e regras de negócio coletivas
**Report/Strategies:** Análise e formatação de dados

**Justificativa:** Cada classe tem uma única responsabilidade bem definida (Single Responsibility Principle)

### 5. **Persistência Desacoplada**

**Decisão:** Camada de persistência (`repository.py`) separada dos modelos de domínio.

**Justificativa:**

- Modelos não conhecem como são salvos
- Facilita trocar de JSON para SQLite futuramente
- Testes podem usar objetos sem persistência

### 6. **Métodos Especiais Python**

Implementados para comportamento idiomático:

- `__str__`: Representação legível para usuários
- `__repr__`: Representação para debug
- `__eq__`: Comparação por título e autor
- `__lt__`: Ordenação por ano

---

## 🏗️ Arquitetura e Organização

### Camadas da Aplicação

1. **Interface (CLI):** Interação com usuário
2. **Domínio (Models):** Regras de negócio
3. **Estratégias:** Algoritmos intercambiáveis
4. **Persistência (Data):** Salvamento/carregamento

### Fluxo de Dados

```text
Usuário → CLI → Models → Repository → JSON
                  ↓
              Strategies (para relatórios)
```

---

## 📊 Cobertura de Testes

- **Coverage:** 60% (foco em lógica de negócio)
- **Testes unitários:** 100% dos models
- **Testes de estratégias:** Completo
- **CLI:** Testado manualmente

---

## 🎓 Conceitos de POO Aplicados

| Conceito | Implementação |
|----------|---------------|
| **Herança Simples** | `Publication` → `Book`, `Magazine` |
| **Herança Múltipla** | `Book(Publication, DigitalAsset)` |
| **Classe Abstrata** | `Publication(ABC)`, `ReportStrategy(ABC)` |
| **Encapsulamento** | Properties com validação (`@property`) |
| **Polimorfismo** | Estratégias intercambiáveis |
| **Composição** | `Publication` contém `Annotation` |
| **Agregação** | `Collection` gerencia `Publication` |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**
- **Click** - Framework para CLI
- **Pytest** - Testes unitários
- **JSON** - Persistência de dados

---

## 📝 Melhorias Futuras

- [ ] Migração para SQLite
- [ ] API REST com FastAPI
- [ ] Interface gráfica (GUI)
- [ ] Importação de dados de Goodreads/Skoob
- [ ] Gráficos de progresso de leitura
- [ ] Sincronização em nuvem

---

## 👨‍💻 Autor

**Samuel Wagner Tiburi Silveira**  
Disciplina: Programação Orientada à Objetos (ES0008)  
Universidade Federal do Cariri

---

## 📄 Licença

Este projeto é acadêmico e foi desenvolvido para fins educacionais.
