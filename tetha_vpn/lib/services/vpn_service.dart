import 'package:flutter_vless/flutter_vless.dart';
import '../services/source_parser.dart';
import '../services/server_tester.dart';

class VpnService {
  static final VpnService _instance = VpnService._internal();
  factory VpnService() => _instance;
  VpnService._internal();

  late final FlutterVless _flutterVless;
  bool _isConnected = false;
  // ignore: prefer_final_fields
  String _status = "DISCONNECTED";
  String _ping = "0";
  //String? _bestServerUrl;

  bool get isConnected => _isConnected;
  String get status => _status;
  String get ping => _ping;

  /// Инициализация — вызывать один раз при старте приложения
  Future<void> init() async {
    _flutterVless = FlutterVless(
      onStatusChanged: (status) {
        final statusStr = status.toString();
        _isConnected = statusStr.contains('connected') && !statusStr.contains('disconnected');
        _status = statusStr.split('.').last;
        print("VLESS status: $statusStr");
      },
    );

    await _flutterVless.initializeVless(
      providerBundleIdentifier: 'com.example.tetha_vpn.VPNProvider',
      groupIdentifier: 'group.com.example.tetha_vpn',
    );
  }

  /// Подключиться к лучшему серверу
  Future<void> connect() async {
    // 1. Скачиваем ссылки
    final urls = await SourceParser.fetchVlessUrls(
        'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt'
    );
    print('Найдено ссылок: ${urls.length}');
    if (urls.isEmpty) {
      print('Нет доступных серверов');
      return;
    }

    // 2. Ищем лучший по пингу
    final bestUrl = await ServerTester.findBestServer(_flutterVless, urls);
    if (bestUrl == null) {
      print('Не удалось найти рабочий сервер');
      return;
    }

    //_bestServerUrl = bestUrl;

    // 3. Парсим URL и получаем конфиг
    final parser = FlutterVless.parseFromURL(bestUrl);
    final config = parser.getFullConfiguration();

    // 4. Запрашиваем разрешение VPN (обязательно!)
    final allowed = await _flutterVless.requestPermission();
    if (!allowed) {
      print("VPN permission denied");
      return;
    }

    // 5. Запускаем VPN
    await _flutterVless.startVless(
      remark: parser.remark,
      config: config,
    );

    try {
      final realPing = await _flutterVless.getServerDelay(config: config);
      _ping = realPing.toString();
    } catch (e) {
      print('Не удалось получить пинг: $e');
      _ping = "0";
    }
    _isConnected = true;
  }

  /// Отключиться
  Future<void> disconnect() async {
    await _flutterVless.stopVless();
    _isConnected = false;
    _ping = "0";
    //_bestServerUrl = null;
  }
}