import click
from pathlib import Path
from threecs import PDFAnalyzer, OOXMLExporter

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option(
    '--output-dir', '-o',
    type=click.Path(),
    default='output',
    help='Output directory for processed files'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Print detailed processing information'
)
def process_document(pdf_path, output_dir, verbose):
    """Process PDF document using the 3C's framework."""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Initialize and run analyzer with enhanced logging
        analyzer = PDFAnalyzer(pdf_path, output_dir, verbose)
        analyzer.analyze()
        
        # Export results
        xml_path = output_path / 'document_structure.xml'
        exporter = OOXMLExporter(analyzer.concept, analyzer.context, analyzer.content)
        exporter.export_xml(xml_path)
        
        # Enhanced summary output
        click.echo('\nDocument Analysis Summary:')
        click.echo('-' * 30)
        click.echo(f"Title: {analyzer.concept.title}")
        click.echo(f"Number of sections: {len(analyzer.context.sections)}")
        
        # Print detailed section information
        click.echo("\nSection Structure:")
        for section, info in analyzer.context.sections.items():
            click.echo(f"  - {section} (Page {info['page']}, Level {info['level']})")
        
        click.echo(f"\nOutput XML: {xml_path}")
        
    except Exception as e:
        click.echo(f"Error processing document: {str(e)}", err=True)
        raise click.Abort()
    
if __name__ == '__main__':
    process_document()