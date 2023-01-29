import 'package:flutter/material.dart';
import 'package:kw_irs/app/history/widgets/list_item_history.dart';

import '../../constants/app_assets.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

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
            const TextField(
              decoration: InputDecoration(
                hintText: 'Search',
                contentPadding: EdgeInsets.symmetric(horizontal: 15),
              ),
              style: TextStyle(fontSize: 13),
            ),
            const SizedBox(height: 20),
            ListView.separated(
              physics: const NeverScrollableScrollPhysics(),
              shrinkWrap: true,
              itemBuilder: (_, index) => const HistoryListItem(),
              separatorBuilder: (_, index) => const SizedBox(
                height: 20,
              ),
              itemCount: 10,
            ),
          ],
        ),
      ),
    );
  }
}
