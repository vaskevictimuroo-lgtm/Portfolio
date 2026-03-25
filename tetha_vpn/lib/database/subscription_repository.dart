import 'package:hive/hive.dart';
import 'models/server.dart';

class SubscriptionRepository {
  Box<Subscription> get _box => Hive.box<Subscription>('servers');

  List<Subscription> getAll() => _box.values.toList();

  void add(Subscription subscription) {
    _box.put(subscription.id, subscription);
  }

  void update(Subscription subscription) {
    _box.put(subscription.id, subscription);
  }

  void delete(String id) {
    _box.delete(id);
  }

  Subscription? getById(String id) {
    return _box.get(id);
  }
}