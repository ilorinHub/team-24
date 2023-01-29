import 'package:flutter/material.dart';
import 'package:kw_irs/constants/app_colors.dart';

class HistoryListItem extends StatelessWidget {
  const HistoryListItem({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      child: Column(
        children: [
          const Align(
            alignment: Alignment.centerRight,
            child: Text(
              '5/Jan/2022 - 02:20pm ',
              style: TextStyle(fontSize: 12),
            ),
          ),
          const SizedBox(height: 5),
          Container(
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(8),
                bottomLeft: Radius.circular(8),
                bottomRight: Radius.circular(8),
              ),
            ),
            padding: const EdgeInsets.all(20),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Theme.of(context).scaffoldBackgroundColor,
                    border: Border.all(
                      width: 3,
                      strokeAlign: StrokeAlign.outside,
                      color: Colors.grey.withOpacity(.2),
                    ),
                  ),
                  child: const Icon(
                    Icons
                        .arrow_downward_rounded, //TODO: Change icon to be dynamic
                    color: AppColors.primaryLight,
                  ),
                ),
                const SizedBox(width: 20),
                Expanded(
                    child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text(
                      'Tech design requirements.pdf',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text('200 KB'),
                  ],
                )),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
