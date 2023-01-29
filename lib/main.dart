import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:kw_irs/app/home/controller/home_controller.dart';

import 'app.dart';

void main() {
  Get.put(HomeController());
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}
