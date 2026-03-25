import 'package:hive/hive.dart';
import 'models/vless_config.dart';

class ConfigRepository {
  Box<VlessConfig> get _box => Hive.box<VlessConfig>('configs');

  List<VlessConfig> getAll() => _box.values.toList();

  List<VlessConfig> getBySubscription(String subscriptionId) {
    return _box.values.where((c) => c.subscriptionId == subscriptionId).toList();
  }

  void add(VlessConfig config) {
    _box.put(config.id, config);
  }

  void addAll(List<VlessConfig> configs) {
    for (final config in configs) {
      _box.put(config.id, config);
    }
  }

  void update(VlessConfig config) {
    _box.put(config.url, config);
  }

  void delete(String url) {
    _box.delete(url);
  }

  void clearBySubscription(String subscriptionId) {
    final toDelete = getBySubscription(subscriptionId);
    for (final config in toDelete) {
      _box.delete(config.url);
    }
  }

  VlessConfig? getActive() {
    try {
      return _box.values.firstWhere((c) => c.isActive);
    } catch (_) {
      return null;
    }
  }

  void setActive(String url) {
    for (final config in _box.values) {
      config.isActive = (config.url == url);
      _box.put(config.url, config);
    }
  }
}