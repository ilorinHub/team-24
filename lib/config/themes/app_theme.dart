import 'package:flutter/material.dart';

import '../../constants/app_colors.dart';

class AppTheme {
  static ThemeData get light => ThemeData.light().copyWith(
        primaryColor: AppColors.primary,
        progressIndicatorTheme:
            const ProgressIndicatorThemeData(color: AppColors.primary),
        checkboxTheme: CheckboxThemeData(
            fillColor:
                MaterialStateColor.resolveWith((states) => AppColors.primary),
            checkColor:
                MaterialStateColor.resolveWith((states) => AppColors.white),
            shape: const CircleBorder(
                side: BorderSide(width: 1, color: AppColors.gray))),
        brightness: Brightness.light,
        cardColor: AppColors.cardColorLight,
        splashColor: AppColors.primary.withOpacity(.4),
        hintColor: AppColors.fontLight2,
        dividerColor: AppColors.fontLight2,
        backgroundColor: AppColors.backgroundLight,
        scaffoldBackgroundColor: AppColors.backgroundLight,
        colorScheme:
            ColorScheme.fromSwatch().copyWith(secondary: AppColors.primary),
      );
  static ThemeData get dark => ThemeData.dark().copyWith(
        primaryColor: AppColors.primary,
        progressIndicatorTheme:
            const ProgressIndicatorThemeData(color: AppColors.primary),
        checkboxTheme: CheckboxThemeData(
            fillColor:
                MaterialStateColor.resolveWith((states) => AppColors.primary),
            checkColor:
                MaterialStateColor.resolveWith((states) => AppColors.white),
            shape: const CircleBorder(
                side: BorderSide(width: 1, color: AppColors.gray))),
        brightness: Brightness.dark,
        cardColor: AppColors.cardColorLight,
        splashColor: AppColors.primary.withOpacity(.4),
        hintColor: AppColors.fontLight2,
        dividerColor: AppColors.fontLight2,
        backgroundColor: AppColors.backgroundDark,
        scaffoldBackgroundColor: AppColors.backgroundDark,
        iconTheme: const IconThemeData(
          color: AppColors.fontDark,
        ),
      );
}
