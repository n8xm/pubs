from .. import repo
from .. import configs
from .helpers import (add_references_argument, parse_reference,
                      add_docfile_to_paper)


def parser(subparsers, config):
    parser = subparsers.add_parser('attach',
            help='attach a document to an existing paper')
    parser.add_argument('-c', '--copy', action='store_true', default=None,
            help="copy document files into library directory (default)")
    parser.add_argument('-C', '--nocopy', action='store_false', dest='copy',
            help="don't copy document files (opposite of -c)")
    add_references_argument(parser, single=True)
    parser.add_argument('document', help='pdf or ps file')
    return parser


def command(config, ui, copy, reference, document):
    """
    :param bibfile: bibtex file (in .bib, .bibml or .yaml format.
    :param docfile: path (no url yet) to a pdf or ps file
    """
    if copy is None:
        copy = config.get(configs.MAIN_SECTION, 'import-copy')
    rp = repo.Repository.from_directory(config)
    key = parse_reference(ui, rp, reference)
    paper = rp.get_paper(key)
    try:
        add_docfile_to_paper(rp, paper, docfile=document, copy=copy)
    except ValueError, v:
        ui.error(v.message)
        ui.exit(1)
# TODO handle case where citekey exists
