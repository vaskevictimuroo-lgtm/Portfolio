import 'package:hive/hive.dart';

part 'vless_config.g.dart';

@HiveType(typeId: 1)
class VlessConfig {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String url;

  @HiveField(2)
  final String subscriptionId;

  @HiveField(3)
  int ping;

  @HiveField(4)
  bool isActive;

  @HiveField(5)
  DateTime lastChecked;

  VlessConfig({
    required this.id,
    required this.url,
    required this.subscriptionId,
    required this.ping,
    this.isActive = false,
    required this.lastChecked,
  });
}