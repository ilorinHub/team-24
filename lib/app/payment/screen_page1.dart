import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/config/routers/app_routes.dart';
import 'package:kw_irs/constants/app_colors.dart';
import 'package:kw_irs/utils/ui/app_button.dart';
import 'package:kw_irs/utils/ui/app_dropdown.dart';
import 'package:kw_irs/utils/ui/app_textfield.dart';

import '../../constants/app_assets.dart';

class PaymentProcess1Screen extends StatelessWidget {
  const PaymentProcess1Screen({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      physics: const BouncingScrollPhysics(),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
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
            const Text(
              'Hi Yusuf!',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const Text(
              'Welcome back',
              style: TextStyle(fontSize: 14),
            ),
            const SizedBox(height: 35),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(5),
                border: Border.all(color: Colors.grey),
              ),
              child: Column(
                children: [
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Payment Due',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 15),
                  Row(
                    children: [
                      Expanded(
                        child: LinearProgressIndicator(
                          value: .1,
                          semanticsLabel: '10%',
                          minHeight: 10,
                          backgroundColor: AppColors.primary.withOpacity(.4),
                          color: AppColors.primary,
                        ),
                      ),
                      const SizedBox(width: 20),
                      const Text(
                        '25 Days',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 25),
            AppTextField(
              label: 'TIN',
              keyboardType: TextInputType.number,
              controller: TextEditingController(),
            ),
            const SizedBox(height: 25),
            AppTextField(
              label: 'Amount',
              keyboardType:
                  const TextInputType.numberWithOptions(decimal: true),
              controller: TextEditingController(),
            ),
            const SizedBox(height: 25),
            AppDropdown(),
            const SizedBox(height: 25),
            AppButton(
                label: 'Proceed',
                onTap: () => Get.toNamed(AppRoutes.selectPaymentMethod))
            //
          ],
        ),
      ),
    );
  }
}
