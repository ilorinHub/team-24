import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/config/routers/app_routes.dart';
import 'package:kw_irs/constants/app_assets.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    _navigateToLoginAfterDelay();

    return Scaffold(
      body: SafeArea(
          child: Center(
        child: Image.asset(
          AppAssets.image.logo,
          height: 200,
          width: 200,
        ),
      )),
    );
  }

  Future<void> _navigateToLoginAfterDelay() async =>
      await Future.delayed(const Duration(seconds: 2))
          .then((value) => Get.toNamed(AppRoutes.login));
}
