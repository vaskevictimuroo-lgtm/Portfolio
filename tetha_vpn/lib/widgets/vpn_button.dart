import 'package:flutter/material.dart';

class VpnButton extends StatelessWidget {
  final bool isConnected;
  final VoidCallback onPressed;

  const VpnButton({
    super.key,
    required this.isConnected,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: isConnected ? const Color(0xFF20FF00) : const Color(0xFFFFFFFF),
      ),
      child: Text(isConnected ? "Отключить" : "Подключить"),
    );
  }
}