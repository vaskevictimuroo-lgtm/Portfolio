import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

class VpnApp extends StatelessWidget {
  const VpnApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFb31d09),
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFFb31d09),
      ),
      home: const VpnHomePage(),
    );
  }
}