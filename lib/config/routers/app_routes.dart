import 'package:get/get.dart';
import 'package:kw_irs/app/auth/screen_login.dart';
import 'package:kw_irs/app/auth/screen_signup.dart';
import 'package:kw_irs/app/home/screen_home.dart';
import 'package:kw_irs/app/payment/screen_select_payment.dart';
import 'package:kw_irs/app/profile/screen_edit_bank.dart';
import 'package:kw_irs/app/profile/screen_edit_company_profile.dart';
import 'package:kw_irs/app/profile/screen_edit_profile.dart';

import '../../app/auth/screen_splash.dart';

class AppPages {
  //
  static final routes = [
    GetPage(
      name: AppRoutes.splash,
      page: () => const SplashScreen(),
    ),
    GetPage(
      name: AppRoutes.login,
      page: () => const LoginScreen(),
    ),
    GetPage(
      name: AppRoutes.signup,
      page: () => const SignupScreen(),
    ),
    //
    GetPage(
      name: AppRoutes.home,
      page: () => const HomeLayout(),
    ),
    //
    GetPage(
      name: AppRoutes.selectPaymentMethod,
      page: () => const SelectPaymentMethodScreen(),
    ),
    GetPage(
      name: AppRoutes.editProfile,
      page: () => const EditProfileScreen(),
    ),
    //
    GetPage(
      name: AppRoutes.editCompanyInfo,
      page: () => const EditCompanyProfileScreen(),
    ),
    //
    GetPage(
      name: AppRoutes.editBankInfo,
      page: () => const EditBankScreen(),
    ),
  ];
}

class AppRoutes {
  static String get splash => '/auth/splash';
  static String get login => '/auth/login';
  static String get signup => '/auth/create-account';

  //
  static String get home => '/';

  // payments
  static String get selectPaymentMethod => '/pay/select-payment-method';

  // profile
  static String get editProfile => '/profile/edit';

  // company
  static String get editCompanyInfo => '/company/edit';

  // bank
  static String get editBankInfo => '/bank/edit';
}
