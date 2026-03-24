import 'package:flutter/material.dart';
import 'app.dart';
import 'services/source_parser.dart';

void main() async {
  final urls = await SourceParser.fetchVlessUrls(
      'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt'
  );
  print('Найдено ссылок: ${urls.length}');
  if (urls.isNotEmpty) {
    print('Первая ссылка: ${urls[0]}');
  }
  runApp(VpnApp());
}
