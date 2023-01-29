import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/utils/ui/app_button.dart';
import 'package:kw_irs/utils/ui/appbar.dart';

import '../../utils/ui/app_textfield.dart';

class EditCompanyProfileScreen extends StatelessWidget {
  const EditCompanyProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context: context, title: 'Company Info'),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                AppTextField(
                  label: 'TIN',
                  hint: '123456789',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(),
                ),
                const SizedBox(height: 20),
                AppTextField(
                  label: 'Total Employees',
                  hint: '10',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(),
                ),
                const SizedBox(height: 20),
                AppTextField(
                  label: 'Annual income (NGN)',
                  hint: '1,000,000',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(),
                ),
                const SizedBox(height: 20),
                Container(
                  height: 145,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: const [
                      Icon(Icons.cloud_upload_rounded),
                      SizedBox(height: 20),
                      Text(
                        'Upload CAC Certificate',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                AppButton(label: 'Update info', onTap: () => Get.back()),
                const SizedBox(height: 30),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
