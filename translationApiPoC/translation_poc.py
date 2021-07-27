#!/usr/bin/env python3

import argparse
import os.path
import mimetypes
import json
from pathlib import Path
import lxml.etree as ET
import boto3


SUPPORTED_LANGS = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'bn', 'bs', 'bg', 'ca', 'zh', 'zh-TW', 'hr', 'cs', 'da', 'fa-AF',
                   'nl', 'en', 'et', 'fa', 'tl', 'fi', 'fr', 'fr-CA', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'he', 'hi',
                   'hu', 'is', 'id', 'it', 'ja', 'kn', 'kk', 'ko', 'lv', 'lt', 'mk', 'ms', 'ml', 'mt', 'mn', 'no', 'fa',
                   'ps', 'pl', 'pt', 'ro', 'ru', 'sr', 'si', 'sk', 'sl', 'so', 'es', 'es-MX', 'sw', 'sv', 'tl', 'ta',
                   'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'auto']

translate_client = boto3.client(service_name='translate', region_name='eu-central-1', use_ssl=True)


def parse_args():
    parser = argparse.ArgumentParser(description='Translate XML/JSON files. Output filename is the same as input with '
                                                 'country code prefix.')

    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='filename(s) to be translated')

    parser.add_argument('-s', '--source-lang', dest='source_language', action='store',
                        help='language to be translated from', default='auto')

    parser.add_argument('-t', '--target-lang', dest='target_language', action='store',
                        help='language to be translated to', required=True)

    return parser.parse_args()


def validate_args(args: dict):
    for file in args.files:
        if not os.path.isfile(file):
            raise RuntimeError("No such file: " + file)
    if args.source_language not in SUPPORTED_LANGS:
        raise RuntimeError("Source language not supported: " + args.source_language)
    if args.target_language not in SUPPORTED_LANGS:
        raise RuntimeError("Target language not supported: " + args.target_language)


def check_type(file_name: str) -> str:
    return mimetypes.guess_type(file_name)[0]


def translate(value, src_lang, dst_lang):
    result = translate_client.translate_text(Text=value, SourceLanguageCode=src_lang, TargetLanguageCode=dst_lang)
    return result.get('TranslatedText')


def translate_json(data, src_lang, dst_lang):
    for key, value in data.items():
        if isinstance(value, dict):
            translate_json(value, src_lang, dst_lang)
        elif isinstance(value, str):
            data[key] = translate(value, src_lang, dst_lang)
        elif isinstance(value, list):
            for idx, val in enumerate(value):
                value[idx] = translate(value[idx], src_lang, dst_lang)
    return data


def translate_xml(data, src_lang, dst_lang):
    if isinstance(data, str):
        return translate(data, src_lang, dst_lang)
    else:
        for child in data:
            if child.text is not None:
                child.text = translate_xml(child.text, src_lang, dst_lang)
            translate_xml(child, src_lang, dst_lang)


def translate_json_file(file_name, src_lang, dst_lang):
    data = Path(file_name).read_text()
    json_data = json.loads(data)
    translate_json(json_data, src_lang, dst_lang)
    print(json.dumps(json_data, indent=4))
    print(json.dumps(json_data, indent=4),  file=open(dst_lang + '_' + file_name, 'w'))


def translate_xml_file(file_name, src_lang, dst_lang):
    et = ET.parse(file_name)
    translate_xml(et.getroot(), src_lang, dst_lang)
    result = ET.tostring(et.getroot(), pretty_print=True).decode("utf-8")
    print(result)
    print(result, file=open(dst_lang + '_' + file_name, "w"))


if __name__ == "__main__":
    args = parse_args()
    validate_args(args)
    for file_name in args.files:
        fileType = check_type(file_name)
        if fileType == "application/json":
            translate_json_file(file_name, args.source_language, args.target_language)
        elif fileType == "application/xml":
            translate_xml_file(file_name, args.source_language, args.target_language)
        else:
            raise RuntimeError("Unsupported file type: " + fileType)
            


