import 'package:hive/hive.dart';

part 'vless_config.g.dart';

@HiveType(typeId: 1)
class VlessConfig {
  @HiveField(0)
  final String url;

  @HiveField(1)
  final String subscriptionId;

  @HiveField(2)
  int ping;

  @HiveField(3)
  bool isActive;

  @HiveField(4)
  DateTime lastChecked;

  VlessConfig({
    required this.url,
    required this.subscriptionId,
    required this.ping,
    this.isActive = false,
    required this.lastChecked,
  });
}