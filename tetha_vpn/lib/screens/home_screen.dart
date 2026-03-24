import 'package:flutter/material.dart';
import '../widgets/vpn_button.dart';
import '../services/vpn_service.dart';

class VpnHomePage extends StatefulWidget {
  const VpnHomePage({super.key});

  @override
  State<VpnHomePage> createState() => _VpnHomePageState();
}

class _VpnHomePageState extends State<VpnHomePage> {
  final VpnService _vpnService = VpnService();

  bool _isConnected = false;
  String _status = "Off";
  String _ping = "0";

  void _toggleVpn() async {
    if (_isConnected) {
      await _vpnService.disconnect();
    } else {
      await _vpnService.connect();
    }

    setState(() {
      _isConnected = _vpnService.isConnected;
      _status = _isConnected ? "On" : "Off";
      _ping = _vpnService.ping;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Align(
            alignment: const Alignment(0, -0.5),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                VpnButton(
                  isConnected: _isConnected,
                  onPressed: _toggleVpn,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}