import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'database/models/server.dart';
import 'database/models/vless_config.dart';
import 'app.dart';
import 'services/vpn_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Hive.initFlutter();
  Hive.registerAdapter(SubscriptionAdapter());  // ← из server.g.dart
  Hive.registerAdapter(VlessConfigAdapter());  // ← из vless_config.g.dart

  await Hive.openBox<Subscription>('servers');
  await Hive.openBox<VlessConfig>('configs');
  await Hive.openBox('settings');
  // === ВРЕМЕННЫЙ ТЕСТ ===
  final testBox = Hive.box('settings');
  testBox.put('test_key', 'Hello Hive!');
  print('Сохранено: ${testBox.get('test_key')}');
  // === КОНЕЦ ТЕСТА ===
  await VpnService().init();
  runApp(const VpnApp());
}