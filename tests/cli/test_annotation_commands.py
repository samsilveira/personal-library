"""
Tests for annotation-related CLI commands.
"""

import pytest
from click.testing import CliRunner
from src.cli.main import cli
from src.models import Collection, Book, Annotation
from src.data import repository


class TestAnnotationCommands:
    """Test annotation CLI commands."""
    
    def test_adicionar_anotacao_success(self, setup_test_environment):
        """Test adding annotation successfully."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, [
            'adicionar-anotacao', '1', 'Ótimo livro!'
        ])
        
        assert result.exit_code == 0
        assert "Anotação adicionada" in result.output
        assert "ann_1_1" in result.output
    
    def test_adicionar_anotacao_with_excerpt(self, setup_test_environment):
        """Test adding annotation with reference excerpt."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, [
            'adicionar-anotacao', '1', 'Passagem interessante',
            '--trecho', 'Era uma vez...'
        ])
        
        assert result.exit_code == 0
        assert "Era uma vez" in result.output
    
    def test_adicionar_anotacao_Editoralicacao_nao_encontrada(self, setup_test_environment):
        """Test adding annotation to non-existent Editoralication."""
        runner = CliRunner()
        
        collection = Collection()
        repository.save_collection(collection)
        
        result = runner.invoke(cli, [
            'adicionar-anotacao', '999', 'Teste'
        ])
        
        assert result.exit_code == 0
        assert "não encontrada" in result.output
    
    def test_listar_anotacoes_empty(self, setup_test_environment):
        """Test listing annotations when none exist."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['listar-anotacoes', '1'])
        
        assert result.exit_code == 0
        assert "Nenhuma anotação encontrada" in result.output
    
    def test_listar_anotacoes_with_data(self, setup_test_environment):
        """Test listing annotations with existing data."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        
        ann1 = Annotation("ann_1_1", "Primeira anotação")
        ann2 = Annotation("ann_1_2", "Segunda anotação", "Trecho de teste")
        book.add_annotation(ann1)
        book.add_annotation(ann2)
        
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['listar-anotacoes', '1'])
        
        assert result.exit_code == 0
        assert "Primeira anotação" in result.output
        assert "Segunda anotação" in result.output
        assert "Total: 2" in result.output
    
    def test_remover_anotacao_success(self, setup_test_environment):
        """Test removing annotation successfully."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        ann = Annotation("ann_1_1", "Teste")
        book.add_annotation(ann)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['remover-anotacao', '1', 'ann_1_1'])
        
        assert result.exit_code == 0
        assert "removida com sucesso" in result.output
    
    def test_remover_anotacao_nao_encontrada(self, setup_test_environment):
        """Test removing non-existent annotation."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['remover-anotacao', '1', 'ann_999'])
        
        assert result.exit_code == 0
        assert "não encontrada" in result.output
    
    def test_ver_anotacao_success(self, setup_test_environment):
        """Test viewing annotation details."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        ann = Annotation("ann_1_1", "Anotação de teste", "Trecho de referência")
        book.add_annotation(ann)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['ver-anotacao', '1', 'ann_1_1'])
        
        assert result.exit_code == 0
        assert "DETALHES DA ANOTAÇÃO" in result.output
        assert "Anotação de teste" in result.output
        assert "Trecho de referência" in result.output
    
    def test_listar_todas_anotacoes_empty(self, setup_test_environment):
        """Test listing all annotations when none exist."""
        runner = CliRunner()
        
        collection = Collection()
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['listar-todas-anotacoes'])
        
        assert result.exit_code == 0
        assert "Nenhuma publicação encontrada" in result.output
    
    def test_listar_todas_anotacoes_with_data(self, setup_test_environment):
        """Test listing all annotations across Editoralications."""
        runner = CliRunner()
        
        collection = Collection()
        
        book1 = Book(1, "Livro 1", "Autor 1", "Editora", 2024, "Ficção", 200)
        ann1 = Annotation("ann_1_1", "Anotação livro 1")
        book1.add_annotation(ann1)
        
        book2 = Book(2, "Livro 2", "Autor 2", "Editora", 2025, "Ficção", 150)
        ann2 = Annotation("ann_2_1", "Anotação livro 2")
        book2.add_annotation(ann2)
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['listar-todas-anotacoes'])
        
        assert result.exit_code == 0
        assert "Livro 1" in result.output
        assert "Livro 2" in result.output
        assert "Anotação livro 1" in result.output
        assert "Anotação livro 2" in result.output
    
    def test_buscar_anotacoes_found(self, setup_test_environment):
        """Test searching annotations with results."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        ann1 = Annotation("ann_1_1", "Personagem principal muito bom")
        ann2 = Annotation("ann_1_2", "Final surpreendente")
        book.add_annotation(ann1)
        book.add_annotation(ann2)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['buscar-anotacoes', 'personagem'])
        
        assert result.exit_code == 0
        assert "Personagem principal" in result.output
        assert "Final surpreendente" not in result.output
    
    def test_buscar_anotacoes_not_found(self, setup_test_environment):
        """Test searching annotations with no results."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        ann = Annotation("ann_1_1", "Teste")
        book.add_annotation(ann)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['buscar-anotacoes', 'inexistente'])
        
        assert result.exit_code == 0
        assert "Nenhuma anotação encontrada" in result.output
    
    def test_buscar_anotacoes_in_excerpt(self, setup_test_environment):
        """Test searching annotations in reference excerpt."""
        runner = CliRunner()
        
        collection = Collection()
        book = Book(1, "Livro Teste", "Autor", "Editora", 2025, "Ficção", 200)
        ann = Annotation("ann_1_1", "Comentário", "Era uma vez...")
        book.add_annotation(ann)
        collection.register_publication(book)
        repository.save_collection(collection)
        
        result = runner.invoke(cli, ['buscar-anotacoes', 'era uma'])
        
        assert result.exit_code == 0
        assert "Era uma vez" in result.output