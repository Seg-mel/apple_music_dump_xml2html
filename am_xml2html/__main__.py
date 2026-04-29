import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import argparse
from am_xml2html.converter import Xml2HtmlConverter


def _main(xml_path: str, html_path: str) -> None:
    converter = Xml2HtmlConverter(xml_path, html_path)
    converter.parse_xml()
    converter.generate_html()
    converter.save_html()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Apple Music xml2html',
        description='Convert XML dump of Apple Music library to pretty HTML',
    )
    parser.add_argument('-i', '--input-xml', help='Input XML file path')
    parser.add_argument('-o', '--output-html', help='Output HTML file path')
    args = parser.parse_args()

    _main(xml_path=args.input_xml, html_path=args.output_html)
