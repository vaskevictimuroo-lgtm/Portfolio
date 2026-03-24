class VpnService {
  bool _isConnected = false;
  String _ping = "0";

  bool get isConnected => _isConnected;
  String get ping => _ping;

  Future<void> connect() async {
    // TODO: реальное подключение через flutter_vless
    _isConnected = true;
    _ping = "124";
  }

  Future<void> disconnect() async {
    // TODO: реальное отключение
    _isConnected = false;
    _ping = "0";
  }
}