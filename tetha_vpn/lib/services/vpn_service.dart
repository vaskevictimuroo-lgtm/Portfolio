import '../database/models/server.dart';
import '../database/models/vless_config.dart';
import '../database/subscription_repository.dart';
import '../database/config_repository.dart';
import 'package:flutter_vless/flutter_vless.dart';
import '../services/source_parser.dart';


class VpnService {
  static final VpnService _instance = VpnService._internal();
  factory VpnService() => _instance;
  VpnService._internal();

  late final FlutterVless _flutterVless;
  bool _isConnected = false;
  String _status = "DISCONNECTED";
  String _ping = "0";

  // Репозитории
  final SubscriptionRepository _subRepo = SubscriptionRepository();
  final ConfigRepository _configRepo = ConfigRepository();

  // Источник по умолчанию
  final String _defaultSourceUrl = 'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt';

  bool get isConnected => _isConnected;
  String get status => _status;
  String get ping => _ping;

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

  Future<void> connect() async {
    // 1. Получаем или обновляем подписку
    final subscription = await _getOrUpdateSubscription();
    if (subscription == null) {
      print('Не удалось загрузить подписку');
      return;
    }

    // 2. Получаем конфиги (VPN-серверы) из БД или скачиваем новые
    List<VlessConfig> configs = _configRepo.getBySubscription(subscription.id);

    if (configs.isEmpty || _isDataStale(subscription.lastUpdate)) {
      print('Обновляю список серверов...');
      configs = await _fetchAndSaveConfigs(subscription);
      if (configs.isEmpty) {
        print('Нет доступных серверов');
        return;
      }
    } else {
      print('Использую сохраненные серверы (${configs.length})');
    }

    // 3. Находим лучший сервер по пингу
    final bestConfig = await _findBestConfig(configs);
    if (bestConfig == null) {
      print('Не удалось найти рабочий сервер');
      return;
    }

    // 4. Подключаемся
    await _connectToConfig(bestConfig);
  }

  Future<Subscription?> _getOrUpdateSubscription() async {
    // Проверяем существующую подписку
    List<Subscription> subs = _subRepo.getAll();
    Subscription? subscription;

    if (subs.isNotEmpty) {
      subscription = subs.first;
      print('Найдена сохраненная подписка: ${subscription.name}');
    } else {
      // Создаем новую подписку
      subscription = Subscription(
        id: Uri.parse(_defaultSourceUrl).host,
        url: _defaultSourceUrl,
        name: 'Черные списки VLESS',
        lastUpdate: DateTime.now().subtract(Duration(hours: 2)), // чтобы обновилось
      );
      _subRepo.add(subscription);
      print('Создана новая подписка');
    }

    return subscription;
  }

  Future<List<VlessConfig>> _fetchAndSaveConfigs(Subscription subscription) async {
    // Скачиваем ссылки
    final urls = await SourceParser.fetchVlessUrls(subscription.url);
    if (urls.isEmpty) return [];

    // Создаем конфиги
    final configs = urls.map((url) => VlessConfig(
      id: url.hashCode.toString(),
      url: url,
      subscriptionId: subscription.id,
      ping: 0,
      lastChecked: DateTime.now(),
    )).toList();

    // Очищаем старые и сохраняем новые
    _configRepo.clearBySubscription(subscription.id);
    _configRepo.addAll(configs);

    // Обновляем время последнего обновления подписки
    final updatedSub = Subscription(
      id: subscription.id,
      url: subscription.url,
      name: subscription.name,
      lastUpdate: DateTime.now(),
    );
    _subRepo.update(updatedSub);

    print('Сохранено конфигов: ${configs.length}');
    return configs;
  }

  Future<VlessConfig?> _findBestConfig(List<VlessConfig> configs) async {
    final results = <VlessConfig>[];

    for (final config in configs) {
      final ping = await _testPing(config.url);
      if (ping != null) {
        config.ping = ping;
        results.add(config);
        print('${config.url.substring(0, 50)}... - ${ping}ms');
      }
    }

    if (results.isEmpty) return null;

    // Сортируем по пингу
    results.sort((a, b) => a.ping.compareTo(b.ping));
    final best = results.first;

    // Сохраняем как активный
    _configRepo.setActive(best.url);
    _ping = best.ping.toString();

    print('Лучший сервер: ${best.url.substring(0, 50)}... (${best.ping}ms)');
    return best;
  }

  Future<int?> _testPing(String url) async {
    try {
      final parser = FlutterVless.parseFromURL(url);
      final config = parser.getFullConfiguration();

      final ping = await _flutterVless.getServerDelay(config: config)
          .timeout(const Duration(seconds: 5), onTimeout: () => -1);

      return ping == -1 ? null : ping;
    } catch (e) {
      return null;
    }
  }

  Future<void> _connectToConfig(VlessConfig config) async {
    final parser = FlutterVless.parseFromURL(config.url);
    final fullConfig = parser.getFullConfiguration();

    final allowed = await _flutterVless.requestPermission();
    if (!allowed) {
      print("VPN permission denied");
      return;
    }

    await _flutterVless.startVless(
      remark: parser.remark,
      config: fullConfig,
    );

    _isConnected = true;

    // Обновляем время проверки конфига
    config.lastChecked = DateTime.now();
    _configRepo.update(config);
  }

  Future<void> disconnect() async {
    await _flutterVless.stopVless();
    _isConnected = false;
    _ping = "0";
  }

  bool _isDataStale(DateTime lastUpdate) {
    return DateTime.now().difference(lastUpdate).inHours > 1;
  }
}