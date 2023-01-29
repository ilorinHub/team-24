import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/config/routers/app_routes.dart';

import '../../constants/app_assets.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      physics: const BouncingScrollPhysics(),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          children: [
            const SizedBox(height: 25),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Row(
                children: [
                  Image.asset(AppAssets.image.logo, width: 100, height: 35),
                  const Spacer(),
                  IconButton(
                    onPressed: () => debugPrint('-> toNotifications()'),
                    icon: const Icon(Icons.notifications_rounded),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 25),
            const Divider(),
            const SizedBox(height: 40),
            Container(
              width: 180,
              height: 190,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(15),
                color: Colors.red,
              ),
              child: const Center(child: Text('ProfilePic goes here')),
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
            const SizedBox(height: 20),
            const SizedBox(width: double.infinity, child: Divider()),
            const SizedBox(height: 30),
            ListTile(
              onTap: () => Get.toNamed(AppRoutes.editProfile),
              leading: const Icon(Icons.person),
              title: const Text('Edit Profile'),
              contentPadding:
                  const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
            ),
            const SizedBox(width: double.infinity, child: Divider()),
            ListTile(
              onTap: () => Get.toNamed(AppRoutes.editCompanyInfo),
              leading: const Icon(Icons.house_outlined),
              title: const Text('Company Info'),
              contentPadding:
                  const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
            ),
            const SizedBox(width: double.infinity, child: Divider()),
            ListTile(
              onTap: () => Get.toNamed(AppRoutes.editBankInfo),
              leading: const Icon(Icons.credit_card),
              title: const Text('Bank'),
              contentPadding:
                  const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
            ),
            const SizedBox(width: double.infinity, child: Divider()),
          ],
        ),
      ),
    );
  }
}
