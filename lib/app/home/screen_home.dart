import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:kw_irs/app/history/screen_history.dart';
import 'package:kw_irs/app/home/controller/home_controller.dart';
import 'package:kw_irs/app/payment/screen_page1.dart';
import 'package:kw_irs/app/profile/screen_profile.dart';

class HomeLayout extends StatelessWidget {
  const HomeLayout({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      bottomNavigationBar: Obx(() => BottomNavigationBar(
            currentIndex: homeController.currentPageIndex,
            onTap: (i) => homeController.updatePageIndex(i),
            items: const [
              BottomNavigationBarItem(
                icon: Icon(Icons.home_rounded),
                label: 'Home',
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.history),
                label: 'History',
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person),
                label: 'Profile',
              ),
            ],
          )),
      body: SafeArea(
        child: Obx(() => IndexedStack(
              index: homeController.currentPageIndex,
              children: const [
                PaymentProcess1Screen(),
                HistoryScreen(),
                ProfileScreen(),
              ],
            )),
      ),
    );
  }
}
