import 'package:http/http.dart' as http;

class SourceParser {
  static Future<List<String>> fetchVlessUrls(String url) async {
    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode != 200) {
        throw Exception('Failed to load: ${response.statusCode}');
      }

      final lines = response.body.split('\n');
      final vlessUrls = lines
        .where((line) => line.trim().startsWith('vless://'))
        .map((line) => line.trim())
        .toList();

      return vlessUrls;
    } catch (e) {
      print('Ошибка при парсинге: $e');
      return [];
    }
  }
}