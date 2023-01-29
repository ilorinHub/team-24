import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/constants/app_colors.dart';
import 'package:kw_irs/utils/ui/app_textfield.dart';
import 'package:kw_irs/utils/ui/appbar.dart';

import '../../utils/ui/app_button.dart';

class EditProfileScreen extends StatelessWidget {
  const EditProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context: context, title: 'Edit Profile'),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),
              Container(
                width: 180,
                height: 190,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(15),
                  color: Colors.red,
                ),
                child: Align(
                  alignment: Alignment.bottomRight,
                  child: MaterialButton(
                    onPressed: () => debugPrint('Upload PFP'),
                    shape: const CircleBorder(),
                    color: AppColors.primary,
                    child: const Icon(
                      Icons.camera_alt_rounded,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 30),
              const Text(
                'James Moses',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const Text(
                'TIN: 123456789',
                style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey),
              ),
              const SizedBox(height: 30),
              AppTextField(
                label: 'Email',
                hint: 'Enter Email',
                prefixIcon: Icons.mail,
                controller: TextEditingController(text: 'test@mail.com'),
              ),
              const SizedBox(height: 20),
              AppTextField(
                label: 'Password',
                hint: '*********',
                prefixIcon: Icons.lock,
                controller: TextEditingController(text: 'password'),
              ),
              const SizedBox(height: 40),
              AppButton(
                label: 'Update profile',
                // onTap: () => debugPrint('-> createAccount()'),
                onTap: () => Get.back(),
              ),
              const SizedBox(height: 50),
            ],
          ),
        ),
      ),
    );
  }
}
