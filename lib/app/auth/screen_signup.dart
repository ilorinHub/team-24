import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:kw_irs/config/routers/app_routes.dart';
import 'package:kw_irs/utils/ui/appbar.dart';

import '../../constants/app_assets.dart';
import '../../utils/ui/app_button.dart';
import '../../utils/ui/app_textfield.dart';

class SignupScreen extends StatelessWidget {
  const SignupScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context: context),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            children: [
              const SizedBox(height: 20),
              Image.asset(
                AppAssets.image.logo,
                width: 200,
              ),
              const SizedBox(height: 40),
              const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Let\'s create an account',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 50),
              AppTextField(
                label: 'Fullname',
                hint: 'Enter Fullname',
                prefixIcon: Icons.person,
                controller: TextEditingController(),
              ),
              const SizedBox(height: 20),
              AppTextField(
                label: 'Phone Number',
                hint: 'Enter Phone number',
                prefixIcon: Icons.phone,
                controller: TextEditingController(),
              ),
              const SizedBox(height: 20),
              AppTextField(
                label: 'Email',
                hint: 'Enter Email',
                prefixIcon: Icons.mail,
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
                label: 'Sign up',
                // onTap: () => debugPrint('-> createAccount()'),
                onTap: () => Get.toNamed(AppRoutes.home),
              ),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }
}
