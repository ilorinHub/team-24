import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/config/routers/app_routes.dart';
import 'package:kw_irs/constants/app_colors.dart';
import 'package:kw_irs/utils/ui/app_button.dart';
import 'package:kw_irs/utils/ui/app_textfield.dart';

import '../../constants/app_assets.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            children: [
              const SizedBox(height: 20),
              Image.asset(
                AppAssets.image.logo,
                height: 200,
                width: 200,
              ),
              const SizedBox(height: 50),
              const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Welcome back!',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 50),
              AppTextField(
                label: 'Email',
                hint: 'Enter email',
                prefixIcon: Icons.email,
                controller: TextEditingController(),
              ),
              const SizedBox(height: 20),
              AppTextField(
                label: 'Password',
                hint: '*********',
                prefixIcon: Icons.lock,
                controller: TextEditingController(),
              ),
              const SizedBox(height: 40),
              AppButton(
                label: 'Sign in',
                onTap: () => debugPrint('-> authenticateUser()'),
              ),
              const SizedBox(height: 30),
              const Text(
                'Dont\'t have an account?',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 30),
              Row(
                children: [
                  const Expanded(
                    child: Divider(),
                  ),
                  const SizedBox(width: 20),
                  TextButton(
                      onPressed: () => Get.toNamed(AppRoutes.signup),
                      child: const Text(
                        'Sign up',
                        style: TextStyle(color: AppColors.primary),
                      )),
                  const SizedBox(width: 20),
                  const Expanded(
                    child: Divider(),
                  ),
                ],
              ),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }
}
