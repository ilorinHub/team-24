import 'package:flutter/material.dart';
import 'package:kw_irs/constants/app_colors.dart';

class PayWithListitem extends StatelessWidget {
  const PayWithListitem({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            height: 32,
            width: 46,
            color: Colors.black,
          ),
          const SizedBox(width: 20),
          Expanded(
              child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: const [
                  Text(
                    'Visa',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                  SizedBox(width: 10),
                  Text(
                    '(ending in 1234)',
                    style: TextStyle(fontSize: 12),
                  ),
                ],
              ),
              const Text('Expiry: 06/24'),
              const SizedBox(height: 15),
              Row(
                children: const [
                  Text(
                    'Set as default',
                    style: TextStyle(fontSize: 12),
                  ),
                  SizedBox(width: 10),
                  Text(
                    'Edit',
                    style: TextStyle(fontSize: 14, color: AppColors.primary),
                  ),
                ],
              ),
            ],
          )),
          Checkbox(
            value: false,
            onChanged: (s) => debugPrint('-> changeState()'),
          )
        ],
      ),
    );
  }
}
