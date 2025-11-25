# Projeto - Biblioteca Pessoal Digital

Atividade prática da disciplina de Programação Orientada à Objetos (ES0008) para composição parcial de nota.

## Descrição

Este projeto visa desenvolver um sistema de biblioteca digital que funcione a partir de linha de comando ou através de uma API simples, de forma a aprender e praticar a Programação Orientada à Objetos.

## Estrutura de Classes

Inicialmente, o projeto está dividido nas seguintes classes:

### User

Representa o dono da biblioteca. É a classe raiz que possui `Collection`, de forma pessoal, e `Configuration`, de forma individual, por composição.
Apresenta como atributos `name` e `email`.

### Collection

Gerencia o acervo completo de publicações do usuário. É responsável por adicionar, remover e buscar publicações em sua lista.
Apresenta como atributo `publications`, como dicionário.
Possui como métodos principais `register_publication()`, `list_publications()`, `remove_publication()`, `search_by_author()`, `search_by_title()`, entre outros.
Apresenta relação de composição com a classe `Publication` e é possuída por `User`.

### Publication

Contém todas as informações e regras de negócio pertinentes à cada obra. É responsável por gerenciar seu próprio estado interno.
Tem como atributos `title`, `author`, `year`, `genre`, `status`, `start_reading_date`, `rating`, dentre outros.
Seus métodos principais são `start_reading()`, `finish_reading()`, `rate_publication()`, `add_annotation()`, entre outros.
Possui relação de composição com a classe `Annotation` e é possuída por `Collection`.

#### Book

É especialização de Publication.
Apresenta como atributo o `ISBN`.

#### DigitalMagazine

É especialização de Publication.
Apresenta como atributo o `ISSN`.

### Annotation

Representa um registro de texto associado a uma publicação. Seu ciclo de vida depende 100% da publicação que está associada.
Seus atributos são `annotation_date`, `reference_excerpt` e `text`.
É possuída por `Publication`.

### Configuration

Armazena as preferências e metas do usuário, facilitando o carregamento e salvamento a partir de um `settings.json`.
Tem como atributos `annual_goal`, `simultaneous_reading_limit` e `favorite_genre`.
Seus métodos são `load_configurations()` e `save_configurations()`.
É possuído por `User`.

### Report

Classe de serviço stateless responsável por processar dados e gerar métricas.
Seus métodos são `check_total_publications()`, `check_publications_by_status()`, dentre outros.
Depende de `Collection` para receber os dados, mas não a armazena.

## Diagrama UML

```mermaid
---
title: Diagrama UML - Biblioteca Pessoal Digital
---
classDiagram
	direction LR
	
	`Collection` *-- "N" `Publication` : contains
	`Publication` <|-- Book
	`Publication` <|-- Magazine
	`Publication` *-- "N" `Annotation` : contains
	`User` *-- "1" `Collection` : owns
	`User` *-- "1" `Configuration` : owns
	`Report` ..> `Collection` : uses

	class `Collection`{
		publications: dict
		register_publication(publication: Publication) bool
		list_publications()
		remove_publication(id: str) bool
		search_by_author(author: str) list
		search_by_title()
		search_by_status()
		filter_by_reading_period()
	    start_publication_reading(id, configuration) bool
	}
	
	class `Publication` {
		<<Abstract>>
		id
		title
		author
		publisher
		year
		genre
		number_of_pages
		type
		file_path
		status
		start_reading_date
		end_reading_date
		rating
		rating_inclusion_date
	       annotations: list
		start_reading()
		finish_reading()
		rate_publication(score: int) void
		add_annotation(annotation: Annotation) void
		list_annotations()
		remove_annotation()
	}
	
	class Book{
		ISBN
	}
	
	class Magazine{
		ISSN
	}
	
	class `Annotation`{
		annotation_id
		annotation_date
		reference_excerpt
		text
	}
	
	class `Report` {
		<<Service>>
		check_total_publications(collection: Collection) int
		check_publications_by_status(collection: Collection) dict
		calculate_average_ratings()
		check_top_5_publications()
	       check_goal_progress(collection, configuration) float
	}
	
	class `User` {
		name
		email
	}
	
	class `Configuration` {
		annual_goal
		simultaneous_reading_limit
		favorite_genre
		load_configurations()
		save_configurations()
	}

```
