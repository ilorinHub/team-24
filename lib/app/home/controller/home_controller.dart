import 'package:get/get.dart';

class HomeController extends GetxController {
  static HomeController instance = Get.find();

  //
  final RxInt _currentPageIndex = 0.obs;

  // getters
  int get currentPageIndex => _currentPageIndex.value;

  // setters
  updatePageIndex(int index) => _currentPageIndex.value = index;
}

HomeController homeController = HomeController.instance;
