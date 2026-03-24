import 'package:flutter_vless/flutter_vless.dart';

class ServerTester {
  /// Проверяет список ссылок, возвращает лучшую по пингу
  static Future<String?> findBestServer(
      FlutterVless vless,
      List<String> urls,
      ) async {
    final results = <Map<String, dynamic>>[];

    for (final url in urls) {
      final ping = await _testPing(vless, url);
      if (ping != null) {
        results.add({
          'url': url,
          'ping': ping,
        });
        print('$url - ${ping}ms');
      }
    }

    if (results.isEmpty) return null;

    results.sort((a, b) => (a['ping'] as int).compareTo(b['ping'] as int));

    final bestUrl = results.first['url'] as String;
    print('Лучший сервер: $bestUrl (${results.first['ping']}ms)');
    return bestUrl;
  }

  static Future<int?> _testPing(FlutterVless vless, String vlessUrl) async {
    try {
      final parser = FlutterVless.parseFromURL(vlessUrl);
      final config = parser.getFullConfiguration();

      final ping = await vless.getServerDelay(config: config)
          .timeout(const Duration(seconds: 5), onTimeout: () => -1);

      return ping == -1 ? null : ping;
    } catch (e) {
      print('Ошибка пинга: $e');
      return null;
    }
  }
}