import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:kw_irs/utils/ui/app_dropdown.dart';

import '../../utils/ui/app_button.dart';
import '../../utils/ui/app_textfield.dart';
import '../../utils/ui/appbar.dart';

class EditBankScreen extends StatelessWidget {
  const EditBankScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(context: context, title: 'Bank Details'),
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
                  label: 'Account Number',
                  hint: '123456789',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(),
                ),
                const SizedBox(height: 20),
                AppTextField(
                  label: 'Account Name',
                  hint: '10',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(),
                ),
                const SizedBox(height: 20),
                AppDropdown(
                  items: const [
                    'Select Bank',
                    'Bank 1',
                    'Bank 2',
                    'Bank 3',
                    'Bank 4',
                  ],
                ),
                const SizedBox(height: 20),
                AppTextField(
                  label: 'BVN',
                  hint: '1,000,000',
                  keyboardType: TextInputType.number,
                  controller: TextEditingController(text: '************221'),
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
