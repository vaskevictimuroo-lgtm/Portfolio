import 'package:hive/hive.dart';

part 'server.g.dart';

@HiveType(typeId: 0)
class Subscription {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String url;

  @HiveField(2)
  final String name;

  @HiveField(3)
  final DateTime lastUpdate;

  Subscription({
    required this.id,
    required this.url,
    required this.name,
    required this.lastUpdate,
  });
}