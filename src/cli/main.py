"""
Command-line interface for the Personal Digital Library.
"""

import click
from datetime import date
from models import User, Book, Magazine, Report
from data import repository

@click.group()
@click.pass_context
def cli(ctx):
    """Sistema de Biblioteca Pessoal Digital"""
    user = User(name="Usuário", email="temporario@email.com")

    user.collection = repository.load_collection()

    ctx.obj = user

@cli.command()
def init():
    """Inicializa o banco de dados"""
    click.echo("Inicializando banco de dados...")
    pass

@cli.command()
@click.argument('titulo')
@click.argument('autor')
@click.argument('editora')
@click.argument('ano', type=int)
@click.argument('genero')
@click.argument('numero-Paginas', type=int)
@click.option('--tipo', type=click.Choice(['livro', 'revista']), default='livro')
@click.option('--isbn', default="")
@click.option('--issn', default="")
@click.option('--edicao', type=int, default=1)
@click.option('--numero', type=int, default=1)
@click.pass_obj
def cadastrar(user: User, titulo, autor, editora, ano, genero, numero_paginas, tipo, isbn, issn, edicao, numero):
    """Cadastra uma nova publicação"""
    try:
        pub_id = len(user.collection.list_publications()) + 1

        if tipo == "livro":
            pub = Book(
                pub_id=pub_id,
                title=titulo,
                author=autor,
                publisher=editora,
                year=ano,
                genre=genero,
                number_of_pages=numero_paginas,
                isbn=isbn,
                edition=edicao
            )
        else:
            pub = Magazine(
                pub_id=pub_id,
                title=titulo,
                author=autor,
                publisher=editora,
                year=ano,
                genre=genero,
                number_of_pages=numero_paginas,
                issn=issn,
                issue_number=numero
            )

        user.collection.register_publication(pub)
        repository.save_collection(user.collection)
        click.echo(f"{tipo.capitalize()} '{titulo}' cadastrado com sucesso! (ID: {pub_id})")

    except ValueError as e:
        click.echo(f"Erro: {e}", err=True)
    except Exception as e:
        click.echo(f"Erro inesperado: {e}", err=True)



@cli.command()
@click.pass_obj
def listar(user: User):
    """Lista todas as publicações"""
    pubs = user.collection.list_publications()

    if not pubs:
        click.echo("Nenhuma publicação encontrada")
        return
    
    click.echo(f"Total: {len(pubs)} publicações\n")
    for pub in pubs:
        click.echo(f"   [{pub.id}] {pub.title} - {pub.author}")
        click.echo(f"       Status: {pub.status} | Ano: {pub.year}")
        click.echo("")

@cli.command()
@click.argument('pub_id', type=int)
@click.pass_obj
def iniciar_leitura(user: User, pub_id):
    """Inicia a leitura de uma publicação"""
    try:
        user.start_reading(pub_id)
        repository.save_collection(user.collection)
        click.echo(f"Leitura iniciada!")
    except ValueError as e:
        click.echo(f"Erro: {e}", err=True)

@cli.command()
@click.argument('pub_id', type=int)
@click.pass_obj
def finalizar(user: User, pub_id):
    """Finaliza a leitura de uma publicação"""
    try:
        pubs = user.collection.list_publications()
        pub = next((p for p in pubs if p.id == pub_id), None)

        if not pub:
            click.echo(f"Publicação com o ID {pub_id} não encontrada.", err=True)
            return
        
        pub.finish_reading()
        repository.save_collection(user.collection)

        click.echo(f"Leitura de '{pub.title}' finalizada!")
        click.echo(f"   Data de término: {pub.end_read_date}")
            
    except ValueError as e:
        click.echo(f"Erro: {e}", err=True)

@cli.command()
@click.argument('pub_id', type=int)
@click.argument('nota', type=float)
@click.pass_obj
def avaliar(user: User, pub_id, nota):
    """Avalia uma publicação (0-10)"""
    try:
        pubs = user.collection.list_publications()
        pub = next((p for p in pubs if p.id == pub_id), None)

        if not pub:
            click.echo(f"Publicação com o ID {pub_id} não encontrada.", err=True)
            return
        
        pub.rate_publication(nota)
        repository.save_collection(user.collection)

        stars = "✦" * int(nota/2)
        click.echo(f"'{pub.title}' avaliado com {nota}/10 {stars}")
    except (ValueError, TypeError) as e:
        click.echo(f"Erro: {e}", err=True)

@cli.command()
@click.pass_obj
def relatorio(user: User):
    """Exibe relatório da biblioteca"""
    Report.print_full_report(user.collection)

if __name__ == '__main__':
    cli()