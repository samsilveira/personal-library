"""
Command-line interface for the Personal Digital Library.
"""

import click
from datetime import date
from src.models import User, Book, Magazine, Report
from src.data import repository

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
        pubs = user.collection.list_publications()
        pub = next((p for p in pubs if p.id == pub_id), None)

        user.start_reading(pub_id)
        repository.save_collection(user.collection)
        click.echo(f" [{pub.id}] {pub.title} - Leitura iniciada!")
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

@cli.command()
@click.argument('termo')
@click.option('--por', type=click.Choice(['titulo', 'autor']), default='titulo')
@click.pass_obj
def buscar(user: User, termo, por):
    """Busca publicações por autor ou título"""
    if por == "autor":
        results = user.collection.search_by_author(termo)                
    else:
        results = user.collection.search_by_title(termo)

    if not results:
        click.echo(f"Nenhuma publicação encontrada para: {termo}")
        return
    
    click.echo(f"Encontradas {len(results)} publicações:\n")
    for pub in results:
        click.echo(f"   [{pub.id}] {pub.title} - {pub.author}")
        click.echo(f"       {pub.status}")

@cli.command
@click.argument('pub_id', type=int)
@click.pass_obj
def detalhes(user: User, pub_id):
    """Mostra detalhes completos de uma publicação"""
    pubs = user.collection.list_publications()
    pub = next((p for p in pubs if p.id == pub_id), None)

    if not pub:
        click.echo(f"Publicação com o ID {pub_id} não encontrada.", err=True)
        return
    
    click.echo(f"\n{'='*60}")
    click.echo(f"{pub.title}")
    click.echo(f"{'='*60}")
    click.echo(f"Autor: {pub.author}")
    click.echo(f"Editora: {pub.publisher}")
    click.echo(f"Ano: {pub.year}")
    click.echo(f"Gênero: {pub.genre}")
    click.echo(f"Páginas: {pub.number_of_pages}")
    click.echo(f"Status: {pub.status}")

    if pub.start_read_date:
        click.echo(f"Início da leitura: {pub.start_read_date}")
    if pub.end_read_date:
        click.echo(f"Fim da leitura: {pub.end_read_date}")
    if pub.rating:
        click.echo(f"Avaliação: {pub.rating}/10")

    click.echo(f"{'='*60}\n")

@cli.command
@click.argument('meta', type=int)
@click.option('--limite-simultaneo', type=int)
@click.pass_obj
def definir_meta(user: User, meta, limite_simultaneo):
    """Atualiza a meta anual de leituras e limite de leituras simultâneas"""
    try:
        if meta is None and limite_simultaneo is None:
            click.echo("Forneça pelo menos uma opção (--meta ou --limite-simultaneo)", err=True)
            return
        
        if meta is not None:
            if meta <= 0:
                click.echo(f"A meta deve ser maior que 0", err=True)
                return
            else:
                user.configuration.annual_goal = meta

        if limite_simultaneo is not None:
            if limite_simultaneo <= 0:
                click.echo(f"O limite de leitura simultânea deve ser maior que 0", err=True)
                return
            else:
                user.configuration.simultaneous_reading_limit = limite_simultaneo

        user.configuration.save_settings()
        if meta is not None:
            click.echo(f"Meta anual: {user.configuration.annual_goal} livros")
        if limite_simultaneo is not None:
            click.echo(f"Limite de leituras simultâneas: {user.configuration.simultaneous_reading_limit} livros")
    except Exception as e:
        click.echo(f"Erro: {e}")


@cli.command
@click.pass_obj
def progresso_meta(user: User):
    """Mostra progresso da meta anual de leitura"""
    result = Report.check_annual_goal_progress(user.collection, user.configuration)

    goal = result["goal"]
    completed = result["completed"]
    remaining = result["remaining"]
    percentage = result["percentage"]
    on_track = result["on_track"]

    click.echo(f"Meta anual: {goal} livros")
    click.echo(f"Concluídos: {completed}")
    click.echo(f"Progresso: {percentage}%")

    if on_track:
        click.echo("No ritmo esperado!")
    else:
        click.echo("Em atraso!")


@cli.command('relatorio-avaliacoes')
@click.pass_obj
def evaluation_report(user: User):
    """Exibe relatório detalhado de avaliações."""
    from src.strategies import EvaluationReportStrategy
    
    publications = user.collection.list_publications()
    
    if not publications:
        click.echo("📚 Nenhuma publicação cadastrada ainda.")
        return
    
    strategy = EvaluationReportStrategy()
    report_data = strategy.generate(publications)
    output = strategy.format_output(report_data)
    
    click.echo(output)


@cli.command('top-rated')
@click.option('--limit', '-l', default=5, help='Número de publicações a exibir')
@click.pass_obj
def top_rated_report(user: User, limit):
    """Exibe as publicações melhor avaliadas."""
    from src.strategies import TopRatedReportStrategy
    
    publications = user.collection.list_publications()
    
    if not publications:
        click.echo("📚 Nenhuma publicação cadastrada ainda.")
        return
    
    strategy = TopRatedReportStrategy()
    report_data = strategy.generate(publications, limit=limit)
    output = strategy.format_output(report_data)
    
    click.echo(output)


@cli.command('progresso-detalhado')
@click.pass_obj
def detailed_progress(user: User):
    """Exibe relatório detalhado de progresso anual."""
    from src.strategies import ProgressReportStrategy
    
    publications = user.collection.list_publications()
    
    if not publications:
        click.echo("📚 Nenhuma publicação cadastrada ainda.")
        return
    
    strategy = ProgressReportStrategy()
    report_data = strategy.generate(publications, config=user.configuration)
    output = strategy.format_output(report_data)
    
    click.echo(output)


if __name__ == '__main__':
    cli()