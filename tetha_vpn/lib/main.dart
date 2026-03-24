import 'package:flutter/material.dart';
import 'app.dart';
import 'services/vpn_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await VpnService().init();
  runApp(const VpnApp());
}